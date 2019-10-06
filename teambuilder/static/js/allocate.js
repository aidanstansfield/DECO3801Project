// This file contains the functionality of the allocation page,
// including setting up the angular.js application and sending
// data to the server process.

(function(){

var app = angular.module('allocator', []);

// CONSTRAINT MESSAGE FORMATS -------------------------------------------------

var constraintFormats = {
    "integer" : [
        {val: "integerCount", msg: "Each team <should/shouldn't> have between <min> and <max> members <with/without> <param> between <min> and <max>"},
        //{val: "integerAvg", msg: "Each team <should/shouldn't> have an average <param> betweem <min> and <max>"},
        //{val: "integerSim", msg: "Each team should have <similar/diverse> <param>"},
        //{val: "integerSimGlob", msg: "All teams should have similar <param>"}
    ],
    "multi-select" : [
        {val: "subsetSimilarity", msg: "Each team <should/shouldn't> have similar <param>"},
        //{val: "subsetRange", msg: "Each team <should/shouldn't> have between <min> and <max> members <with/without> <param> equal to <value>"}
    ],
    "bool" : [
        {val: "boolRange", msg: "Each team <should/shouldn’t> have between <min> and <max> members <with/without> <param>"}
    ],
    "option" : [
        {val: "optRange", msg: "Each team <should/shouldn’t> have between <min> and <max> members <with/without> <param> equal to <value>"},
        {val: "optSimilarity", msg: "Each team <should/shouldn't> have <similar/diverse> <param>"}
    ]
};

// FILTERS --------------------------------------------------------------------

// Sanitizes thr given HTML output before it is added to the DOM
app.filter('to_trusted', ['$sce', function($sce) {
    return function(data) {
        return $sce.trustAsHtml(data); 
    };
}]);

// DIRECTIVES -----------------------------------------------------------------

// A constraint that in the constraint list
app.directive('constraint', function() {
    return {
        templateUrl: '/static/html/constraint.html',
        restrict: 'E'
    }
});

// A group in the list of results
app.directive('group', function() {
    return {
        templateUrl: '/static/html/alloc-group.html',
        restrict: 'E'
    }
});

// The select input for selecting a constraint format
app.directive('constraintformatselect', function() {
    return {
        templateUrl: '/static/html/constraintSelect.html', 
        restrict: 'E',
        scope: false
    };
});

// The form input for specifying an integer count constraint
app.directive('integercountform', function() {
    return {
        restrict: 'E',
        templateUrl: '/static/html/integerCount.html'
    }
});

// The form input for specifying a subset simlarity constraint
app.directive('subsetsimilarityform', function() {
    return {
        restrict: 'E',
        templateUrl: '/static/html/subsetSimilarity.html'
    }
});

app.directive('constraintmodal', function() {
    console.log("Running");
    return {
        restrict: 'E',
        templateUrl: '/static/html/constraint-modal.html'
    }
});


// FACTORIES ------------------------------------------------------------------

// The DataHolder factory manages the student information and makes it
// accessible to other components. 
//
// Note:Initially this data will be statically specified and retrieved, 
// but later this will come from the database
app.factory('DataHolder', function($rootScope) {

    var studentData = '{"44781573": {"name": "OPAL MAYER", "age": 22, "preferences": ["gameplay"]}, "49972059": {"name": "OWEN POWERS", "age": 26, "preferences": []}, "43210058": {"name": "LEANNA HOOPER", "age": 22, "preferences": ["graphics"]}, "49218373": {"name": "CANDRA KNAPP", "age": 20, "preferences": ["gameplay"]}, "41434186": {"name": "ARTIE MERCADO", "age": 20, "preferences": ["gameplay"]}, "41919562": {"name": "MISTIE DECKER", "age": 17, "preferences": ["gameplay"]}, "41733160": {"name": "JENEE HAWKINS", "age": 21, "preferences": ["networking", "gameplay"]}, "47912042": {"name": "GALEN STEVENS", "age": 18, "preferences": ["gameplay"]}, "43077121": {"name": "VEDA DUKE", "age": 26, "preferences": ["ui", "gameplay"]}, "44284944": {"name": "ALYSON SANTOS", "age": 21, "preferences": ["graphics"]}, "49801186": {"name": "NOVELLA HEWITT", "age": 19, "preferences": ["gameplay"]}, "44930399": {"name": "LEONE STRONG", "age": 27, "preferences": ["networking", "graphics"]}, "49435228": {"name": "DANN BARRY", "age": 24, "preferences": ["gameplay"]}, "42000636": {"name": "PERRY WARE", "age": 23, "preferences": ["networking"]}, "46211757": {"name": "EDDIE CRAWFORD", "age": 22, "preferences": ["gameplay"]}, "49845902": {"name": "MITCHELL KIRK", "age": 17, "preferences": ["gameplay"]}}';
    var studentParams = '{"age" : "integer" , "preferences" : "multi-select"}';

    // Emits an event to tell listening parties that the internal state
    // has changed.
    function notify() {
        $rootScope.$emit('data-holder-event');
    }

    return {
        // Updates the student data stored in the factory
        // This should be removed later once database access is complete
        setStudentData : function(dataString) {
            studentData = dataString;
            notify();
        },

        // Returns the student data which is stored
        getStudentData : function() {
            return studentData;
        },

        // Sets the parameters that can be specified in constraints
        // This will be removed later since this should come from the 
        // database
        setStudentParams : function(dataString) {
            studentParams = dataString;
            notify();
        },

        // Returns the parameters which can be specified in constraints
        getStudentParams : function() {
            return studentParams;
        },

        // Allows the provided callback to be run when the notify()
        // method is invoked - this allows changes to be detected and
        // acted on
        subscribe : function(scope, callback) {
            var handler = $rootScope.$on('data-holder-event', callback);
            scope.$on('$destroy', handler);
        }
    }
});

// The ConstraintHolder factory is responsible for managing the list
// of constraints which have been specified by the user. This also
// includes the group size constraints.
app.factory('ConstraintHolder', function($rootScope){

    var constraintList = [];
    var minSize = 3;
    var idealSize = 4;
    var maxSize = 5;
    
    // Emits an event to tell listening parties that the internal state
    // has changed.
    function notify() {
        $rootScope.$emit('constraint-holder-event');
    }

    return {

        // Adds a new constraint into the constraint list
        // Note that no validation is done here
        addConstraint : function(constraint) {
            constraintList.push({val : constraint, enabled: false});
            notify();
        },

        // Enables/Disables the constraint at the given index
        // in the constraint list
        toggleConstraint : function(index) {
            var enabled = constraintList[index].enabled;
            constraintList[index].enabled = !enabled;
            notify();
        },

        // Removes the constraint at the given index in the
        // constraint list
        removeConstraint : function(index) {
            constraintList.splice(index, 1);
            notify();
        },

        // Returns a copy of the constraint list
        getConstraintDetails : function() {
            return [...constraintList];
        },

        // Returns a list of enabled constraints 
        getEnabledConstraints : function() {
            result = [];

            constraintList.forEach(function(entry) {
                if (entry.enabled) {
                    result.push(entry.val);
                }
            });

            return result;
        },

        // Sets the minimum group size constraint
        setMinSize : function(size) {
            minSize = size;
            notify();
        },

        // Sets the ideal group size constraint
        setIdealSize : function(size) {
            idealSize = size;
            notify();
        },

        // Sets the maximum group size constraint
        setMaxSize : function(size) {
            maxSize = size;
            notify();
        },

        // Returns the currently set minimum group size
        getMinSize : function() {
            return minSize;
        },

        // Returns the currently set ideal group size
        getIdealSize : function() {
            return idealSize;
        },

        // Returns the currently set maximum group size
        getMaxSize : function() {
            return maxSize;
        },

        // Allows the provided callback to be run when the notify()
        // method is invoked - this allows changes to be detected and
        // acted on
        subscribe : function(scope, callback) {
            var handler = $rootScope.$on('constraint-holder-event', callback);
            scope.$on('$destroy', handler);
        }
    }
});

// CONTROLLERS ----------------------------------------------------------------

// Initialises the scope to constain the initial data values
function initialiseData($scope, DataHolder, ConstraintHolder) {
    $scope.studentData = DataHolder.getStudentData();
    $scope.studentParams = DataHolder.getStudentParams();
    $scope.minSize = ConstraintHolder.getMinSize();
    $scope.idealSize = ConstraintHolder.getIdealSize();
    $scope.maxSize = ConstraintHolder.getMaxSize();
} 

// Initialises watchers in order to update the data holder
// as the UI is updated via user input 
function initialiseWatchers($scope, DataHolder, ConstraintHolder) {
    $scope.$watch('studentData', function(newValue, oldValue) {
        if (newValue != oldValue) {
            DataHolder.setStudentData(newValue);
        }
    });
    $scope.$watch('studentParams', function(newValue, oldValue) {
        if (newValue != oldValue) {
            DataHolder.setStudentParams(newValue);
        }
    });
    $scope.$watch('minSize', function(newValue, oldValue) {
        if (newValue != oldValue) {
            ConstraintHolder.setMinSize(newValue);
        }
    });
    $scope.$watch('idealSize', function(newValue, oldValue) {
        if (newValue != oldValue) {
            ConstraintHolder.setIdealSize(newValue);
        }
    });
    $scope.$watch('maxSize', function(newValue, oldValue) {
        if (newValue != oldValue) {
            ConstraintHolder.setMaxSize(newValue);
        }
    });
}

// The root controller is responsible for controlling data changes
// between the factories
app.controller('rootController', ['$scope', '$compile', 'DataHolder', 'ConstraintHolder', 
    function($scope, $compile, DataHolder, ConstraintHolder) {

        var modalOpen = false;
        initialiseData($scope, DataHolder, ConstraintHolder);
        initialiseWatchers($scope, DataHolder, ConstraintHolder);

        // Initialise the constraint list and set it to update
        // whenever the constraint list changes.
        $scope.constraintList = ConstraintHolder.getConstraintDetails();
        ConstraintHolder.subscribe($scope, function(){
            $scope.constraintList = ConstraintHolder.getConstraintDetails();
        });

        // Make the constaint holder methods accessible to the 
        // outer scope.
        $scope.removeConstraint = function(index) {
            ConstraintHolder.removeConstraint(index);
        }
        $scope.toggleConstraint = function(index) {
            ConstraintHolder.toggleConstraint(index);
        }

        $scope.openConstraintModal = function() {
            if (modalOpen) {
                return;
            }

            var modal = document.createElement('constraintmodal');
            var body = document.getElementsByTagName('body')[0];
            body.appendChild(modal);
            $compile(modal)($scope);
            modalOpen = true;
        }

        $scope.closeConstraintModal = function() {
            if (!modalOpen) {
                return;
            }
            var modal = document.getElementsByTagName('constraintmodal')[0];
            var body = document.getElementsByTagName('body')[0];
            
            body.removeChild(modal);
            modalOpen = false;
        }
}]);

// The controls controller handles sending allocation requests to the server
// and exporting allocations
app.controller('controlsController', ['$rootScope', '$scope', '$http', 'ConstraintHolder', 'DataHolder',
    function($rootScope, $scope, $http, ConstraintHolder, DataHolder) {

        $scope.runAllocation = function() {
            // We need to populate the candidates for the subset similarty constraints
            ConstraintHolder.getEnabledConstraints().forEach(function(constraint){
                if (constraint instanceof SubsetSimilarityConstraint) {
                    var field = constraint.getField();
                    var candidates = new Set();
                    var students = JSON.parse(DataHolder.getStudentData());
                    
                    for (var student in students) {
                        students[student][field].forEach(item => candidates.add(item));
                    }
                    constraint.setCandidates(Array.from(candidates));
                }
            });

            // Once we've populated everything, we are ready to send the request
            $http({
                method : "post",
                url : "/allocator",
                data : {
                    min_size : parseInt(ConstraintHolder.getMinSize(), 10),
                    ideal_size : parseInt(ConstraintHolder.getIdealSize(), 10),
                    max_size : parseInt(ConstraintHolder.getMaxSize(), 10),
                    students : JSON.parse(DataHolder.getStudentData()),
                    constraints: JSON.parse(JSON.stringify(ConstraintHolder.getEnabledConstraints()))
                }
            }).then(function success(response) {
                $rootScope.teams = response.data['teams'];
                console.log(response.data);
            }, function error(response) {
                console.log("Error with response");
            });
        }
}]);

// The constraint entry controller is responsible for handling
// input pertaining to creating constraints.
app.controller('constraintEntryController', ['$rootScope', '$scope', '$compile', 'ConstraintHolder', 'DataHolder',
    function($rootScope, $scope, $compile, ConstraintHolder, DataHolder){

        $scope.paramData = JSON.parse(DataHolder.getStudentParams())
        $scope.availableParams = Object.keys($scope.paramData);
        $scope.selectedParam = "";
        $scope.constraintType = "";
        var addConstraintBtnVisible = false;

        // We need to update the parameters whenever the input field changes
        // This will be removed once the data comes from the database
        DataHolder.subscribe($scope, function(){
            $scope.availableParams = Object.keys(JSON.parse(DataHolder.getStudentParams()));
        })

        // This method is used to correctly format the constraint format values.
        // We need to do this to prevent infinite loops when generating the
        // input fields dynamically.
        $scope.formatMsg = function(message) {
            return message.replace("<param>", $scope.selectedParam);
        }

        // Returns the list of constraint formats which can be used for
        // the given parameter. 
        $scope.getConstraintForms = function(param) {
            return constraintFormats[$scope.paramData[param]]
        }

        $scope.updateSelectedParam = function() {
            var selectContainer = document.getElementById('entryConstraintSelect');
            var inputContainer = document.getElementById('entryConstraintInput');

            if (selectContainer) {
                // We need to remove any previous select elements and
                // subsequent form inputs
                while (selectContainer.firstChild) {
                    selectContainer.removeChild(selectContainer.firstChild);
                }
                if (inputContainer) {
                    while (inputContainer.firstChild) {
                        inputContainer.removeChild(inputContainer.firstChild);
                    }
                }
            
                // Then we create a new select element
                var newHeading = document.createElement("h3");
                newHeading.innerHTML = "Step 2: Select the form of constraint to apply";
                var newNode = document.createElement("constraintformatselect");
            
                selectContainer.appendChild(newHeading);
                selectContainer.appendChild(newNode);
            
                // Once it's added, we re-compile it
                $compile(newNode)($scope);
                addConstraintBtnVisible = false;
            }
        }

        $scope.updateConstraintType = function() {
            var inputContainer = document.getElementById('entryConstraintInput');
            if (inputContainer) {
                while (inputContainer.firstChild) {
                    inputContainer.removeChild(inputContainer.firstChild);
                }
                var newNode = document.createElement($scope.constraintType + "Form");
                inputContainer.appendChild(newNode);
                $compile(inputContainer)($scope);   
                addConstraintBtnVisible = true;
            }
        };

        $scope.addConstraintVisible = function() {
            return addConstraintBtnVisible;
        }

        $scope.submitConstraint = function() {
            if ($scope.constraintType == "integerCount") {
                var shouldBool = $scope.constr.shouldBool;
                var countMin = parseInt($scope.constr.countMin, 10);
                var countMax = parseInt($scope.constr.countMax, 10);
                var withBool = $scope.constr.withBool;
                var field = $scope.selectedParam;
                var fieldMin = parseInt($scope.constr.fieldMin, 10);
                var fieldMax = parseInt($scope.constr.fieldMax, 10);
                var constraint = IntegerCountConstraint(shouldBool, countMin, countMax, withBool, field, fieldMin, fieldMax);
                ConstraintHolder.addConstraint(constraint);
                $scope.closeConstraintModal();
            } else if ($scope.constraintType == "subsetSimilarity") {
                var shouldBool = $scope.constr.shouldBool;
                var field = $scope.selectedParam;
                var constraint = SubsetSimilarityConstraint(shouldBool, field);
                ConstraintHolder.addConstraint(constraint);
                $scope.closeConstraintModal();
            }
        }
}]);

})();