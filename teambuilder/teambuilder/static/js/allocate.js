// This file contains the functionality of the allocation page,
// including setting up the angular.js application and sending
// data to the server process.
(function(){

var app = angular.module('allocator', []);

// CONSTRAINT MESSAGE FORMATS -------------------------------------------------

var constraintFormats = {
    "integer" : [
        {val: "integerCount", msg: "Each group <should/shouldn't> have between <min> and <max> members <with/without> <param> between <min> and <max>"},
        {val: "integerAvg", msg: "Each group <should/shouldn't> have an average <param> betweem <min> and <max>"},
        {val: "integerSim", msg: "Each group should have <similar/diverse> <param>"},
        {val: "integerSimGlob", msg: "All groups should have similar <param>"}
    ],
    "multi-select" : [
        {val: "subsetSimilarity", msg: "Each group <should/shouldn't> have similar <param>"},
        {val: "subsetRange", msg: "Each group <should/shouldn't> have between <min> and <max> members <with/without> <param> equal to <value>"}
    ],
    "bool" : [
        {val: "boolRange", msg: "Each group <should/shouldn’t> have between <min> and <max> members <with/without> <param>"}
    ],
    "option" : [
        {val: "optRange", msg: "Each group <should/shouldn’t> have between <min> and <max> members <with/without> <param> equal to <value>"},
        {val: "optSimilarity", msg: "Each group <should/shouldn't> have similar <param>"}
    ]
};

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
        scope: false,
        link: function($scope, elem, attrs) {
            elem.ready(function() {
                $('select').formSelect();
            });
        }
    };
});

// The form input for specifying an integer count constraint
app.directive('integercountform', function() {
    return {
        restrict: 'E',
        templateUrl: '/static/html/integerCount.html',
        link: function($scope, elem, attrs) {
            elem.ready(function() {
                $('select').formSelect();
            });
        }
    }
});

// The form input for specifying an integer average constraint
app.directive('integeravgform', function() {
    return {
        restrict: 'E',
        templateUrl: '/static/html/integerAvg.html',
        link: function($scope, elem, attrs) {
            elem.ready(function() {
                $('select').formSelect();
            });
        }
    }
});

// The form input for specifying an integer similarity constraint
app.directive('integersimform', function() {
    return {
        restrict: 'E',
        templateUrl: '/static/html/integerSim.html',
        link: function($scope, elem, attrs) {
            elem.ready(function() {
                $('select').formSelect();
            });
        }
    }
});

// The form input for specifying a global similarity constraint
app.directive('integersimglobform', function() {
    return {
        restrict: 'E',
        templateUrl: '/static/html/integerSimGlob.html',
        link: function($scope, elem, attrs) {
            elem.ready(function() {
                $('select').formSelect();
            });
        }
    }
});

// The form input for specifying an option count constraint
app.directive('optrangeform', function() {
    return {
        restrict: 'E',
        templateUrl: '/static/html/optRange.html',
        link: function($scope, elem, attrs) {
            elem.ready(function() {
                $('select').formSelect();
            });
        }
    }
});

// The form input for specifying an option similarity constraint
app.directive('optsimilarityform', function() {
    return {
        restrict: 'E',
        templateUrl: '/static/html/optSimilarity.html',
        link: function($scope, elem, attrs) {
            elem.ready(function() {
                $('select').formSelect();
            });
        }
    }
});

// The form input for specifying a subset count constraint
app.directive('subsetrangeform', function() {
    return {
        restrict: 'E',
        templateUrl: '/static/html/subsetCount.html',
        link: function($scope, elem, attrs) {
            elem.ready(function() {
                $('select').formSelect();
            });
        }
    }
});

// The form input for specifying a subset simlarity constraint
app.directive('subsetsimilarityform', function() {
    return {
        restrict: 'E',
        templateUrl: '/static/html/subsetSimilarity.html',
        link: function($scope, elem, attrs) {
            elem.ready(function() {
                $('select').formSelect();
            });
        }
    }
});

// The form input for specifying a boolean count constraint
app.directive('boolrangeform', function() {
    return {
        restrict: 'E',
        templateUrl: '/static/html/boolCount.html',
        link: function($scope, elem, attrs) {
            elem.ready(function() {
                $('select').formSelect();
            });
        }
    }
});

app.directive('constraintmodal', function() {
    console.log("Running");
    return {
        restrict: 'E',
        templateUrl: '/static/html/constraint-modal.html',
        link: function($scope, elem, attrs) {
            elem.ready(function() {
                $('select').formSelect();
            });
        }
    }
});


// FACTORIES ------------------------------------------------------------------

// The DataHolder factory manages the student information and makes it
// accessible to other components. 
//
// Note:Initially this data will be statically specified and retrieved, 
// but later this will come from the database
app.factory('DataHolder', function($rootScope) {

    var studentData = '{"44781573": {"name": "OPAL MAYER", "age": 22, "preferences": ["gameplay"], "degree" : ["IT"], "postgraduate" : true}, "49972059": {"name": "OWEN POWERS", "age": 26, "preferences": [], "degree" : ["IT"], "postgraduate" : true}, "43210058": {"name": "LEANNA HOOPER", "age": 22, "preferences": ["graphics"], "degree" : ["CS"], "postgraduate" : false}, "49218373": {"name": "CANDRA KNAPP", "age": 20, "preferences": ["gameplay"], "degree" : ["SE"], "postgraduate" : true}, "41434186": {"name": "ARTIE MERCADO", "age": 20, "preferences": ["gameplay"], "degree" : ["IT"], "postgraduate" : false}, "41919562": {"name": "MISTIE DECKER", "age": 17, "preferences": ["gameplay"], "degree" : ["IT"], "postgraduate" : true}, "41733160": {"name": "JENEE HAWKINS", "age": 21, "preferences": ["networking", "gameplay"], "degree" : ["CS"], "postgraduate" : true}, "47912042": {"name": "GALEN STEVENS", "age": 18, "preferences": ["gameplay"], "degree" : ["SE"], "postgraduate" : false}, "43077121": {"name": "VEDA DUKE", "age": 26, "preferences": ["ui", "gameplay"], "degree" : ["CS"], "postgraduate" : true}, "44284944": {"name": "ALYSON SANTOS", "age": 21, "preferences": ["graphics"], "degree" : ["SE"], "postgraduate" : false}, "49801186": {"name": "NOVELLA HEWITT", "age": 19, "preferences": ["gameplay"], "degree" : ["IT"], "postgraduate" : true}, "44930399": {"name": "LEONE STRONG", "age": 27, "preferences": ["networking", "graphics"], "degree" : ["IT"], "postgraduate" : true}, "49435228": {"name": "DANN BARRY", "age": 24, "preferences": ["gameplay"], "degree" : ["IT"], "postgraduate" : false}, "42000636": {"name": "PERRY WARE", "age": 23, "preferences": ["networking"], "degree" : ["SE"], "postgraduate" : true}, "46211757": {"name": "EDDIE CRAWFORD", "age": 22, "preferences": ["gameplay"], "degree" : ["CS"], "postgraduate" : true}, "49845902": {"name": "MITCHELL KIRK", "age": 17, "preferences": ["gameplay"], "degree" : ["IT"], "postgraduate" : true}}';
    var studentParams = '{"age" : "integer" , "preferences" : "multi-select", "degree" : "option", "postgraduate" : "bool"}';
    var paramOptions = '{"preferences" : ["graphics", "gameplay", "networking", "ui"], "degree" : ["IT", "CS", "SE"]}';

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

        // Sets the parameter values that can be specified in option
        // constraints. This will be removed later since this should 
        // come from the database
        setParamOptions : function(dataString) {
            paramOptions = dataString;
            notify();
        },

        // Returns the option values which can be selected in option
        // constraints
        getParamOptions : function() {
            return paramOptions;
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
            constraintList.push({val : constraint, enabled: true});
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

// FILTERS --------------------------------------------------------------------

// Sanitizes the given HTML output before it is added to the DOM
app.filter('to_trusted', ['$sce', function($sce) {
    return function(data) {
        return $sce.trustAsHtml(data); 
    };
}]);

// Retrieves the student data associated with the given entry
app.filter('student_name', ['DataHolder', function(DataHolder) {
    return function(data) {
        var entry = JSON.parse(DataHolder.getStudentData())[data]
        return entry["name"];
    };
}]);


// CONTROLLERS ----------------------------------------------------------------

// Initialises the scope to constain the initial data values
function initialiseData($scope, DataHolder, ConstraintHolder) {
    $scope.studentData = DataHolder.getStudentData();
    $scope.studentParams = DataHolder.getStudentParams();
    $scope.paramOptions = DataHolder.getParamOptions();
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
    $scope.$watch('paramOptions', function(newValue, oldValue) {
        if (newValue != oldValue) {
            DataHolder.setParamOptions(newValue);
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
app.controller('rootController', ['$scope', '$compile', '$timeout', 'DataHolder', 'ConstraintHolder', 
    function($scope, $compile, $timeout, DataHolder, ConstraintHolder) {

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
            
            
            // var selectElms = body.getElementsByTagName('select');
            // console.log(selectElms);
            // console.log(selectElms.length);
            // for (var i = 0; i < selectElms.length; i++) {
            //     console.log(i);
            //     console.log(selectElms[i].id);
            // }
            // console.log(selectElms);
            // console.log(selectList);
            // selectList.forEach(function(value, index, array){
            //     console.log(value);//.material_select();
            // })
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
                if (constraint instanceof SubsetSimilarityConstraint ||
                    constraint instanceof OptionCountConstraint ||
                    constraint instanceof OptionSimilarityConstraint ||
                    constraint instanceof SubsetCountConstraint) {
                    var field = constraint.getField();
                    var candidates = JSON.parse(DataHolder.getParamOptions())
                    constraint.setCandidates(candidates[field]);
                }
            });

            // Make the loader appear
            document.getElementsByClassName("loader-container")[0].classList.remove("loader-container--hidden");
            // Once we've populated everything, we are ready to send the request
            $http({
                method : "post",
                url : "/allocate",
                data : {
                    cid : window.$cid,
                    min_size : parseInt(ConstraintHolder.getMinSize(), 10),
                    ideal_size : parseInt(ConstraintHolder.getIdealSize(), 10),
                    max_size : parseInt(ConstraintHolder.getMaxSize(), 10),
                    students : JSON.parse(DataHolder.getStudentData()),
                    constraints: JSON.parse(JSON.stringify(ConstraintHolder.getEnabledConstraints()))
                }
            }).then(function success(response) {
                $rootScope.teams = response.data['teams'];
                console.log(response.data);
                document.getElementsByClassName("loader-container")[0].classList.add("loader-container--hidden");
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
        $scope.optionData = JSON.parse(DataHolder.getParamOptions())
        $scope.availableParams = Object.keys($scope.paramData);
        $scope.selectedParam = "";
        $scope.constraintType = "";
        $scope.form = {};

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

        $scope.getParamOptions = function(param) {
            return $scope.optionData[param];
        }

        $scope.invalidCountMinSize = function() {
            return $scope.countMin > $scope.countMax;
        }

        $scope.invalidFieldMinSize = function() {
            return $scope.fieldMin > $scope.fieldMax;
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
                if (!$scope.form.integerCountForm.$valid || $scope.invalidFieldMinSize() || 
                        $scope.invalidCountMinSize()) {
                    return;
                }
                var shouldBool = $scope.shouldBool;
                var countMin = parseInt($scope.countMin, 10);
                var countMax = parseInt($scope.countMax, 10);
                var withBool = $scope.withBool;
                var field = $scope.selectedParam;
                var fieldMin = parseInt($scope.fieldMin, 10);
                var fieldMax = parseInt($scope.fieldMax, 10);
                var constraint = IntegerCountConstraint(shouldBool, countMin, countMax, withBool, field, fieldMin, fieldMax);
                ConstraintHolder.addConstraint(constraint);
                $scope.closeConstraintModal();
            } else if ($scope.constraintType == "integerAvg") {
                if (!$scope.form.integerAvgForm.$valid || $scope.invalidFieldMinSize()) {
                    return;
                }
                var shouldBool = $scope.shouldBool;
                var field = $scope.selectedParam;
                var fieldMin = parseInt($scope.fieldMin, 10);
                var fieldMax = parseInt($scope.fieldMax, 10);
                var constraint = IntegerAverageConstraint(shouldBool, field, fieldMin, fieldMax);
                ConstraintHolder.addConstraint(constraint);
                $scope.closeConstraintModal();
            } else if ($scope.constraintType == "integerSim") {
                if (!$scope.form.integerSimForm.$valid) {
                    return;
                }
                var shouldBool = $scope.shouldBool;
                var field = $scope.selectedParam;
                var constraint = IntegerSimilarityConstraint(shouldBool, field);
                ConstraintHolder.addConstraint(constraint);
                $scope.closeConstraintModal();
            } else if ($scope.constraintType == "integerSimGlob") {
                var field = $scope.selectedParam;
                var constraint = IntegerGlobalAverageConstraint(field);
                ConstraintHolder.addConstraint(constraint);
                $scope.closeConstraintModal();
            } else if ($scope.constraintType == "optRange") {
                if (!$scope.form.optRangeForm.$valid || $scope.invalidCountMinSize() || 
                        $scope.invalidCountMinSize()) {
                    return;
                }
                var shouldBool = $scope.shouldBool;
                var countMin = parseInt($scope.countMin, 10);
                var countMax = parseInt($scope.countMax, 10);
                var withBool = $scope.withBool;
                var field = $scope.selectedParam;
                var optVal = $scope.optVal;
                var constraint = OptionCountConstraint(shouldBool, countMin, countMax, withBool, field, optVal);
                ConstraintHolder.addConstraint(constraint);
                $scope.closeConstraintModal();
            } else if ($scope.constraintType == "optSimilarity") {
                if (!$scope.form.optSimilarityForm.$valid) {
                    return;
                }
                var shouldBool = $scope.shouldBool;
                var field = $scope.selectedParam;
                var constraint = OptionSimilarityConstraint(shouldBool, field);
                ConstraintHolder.addConstraint(constraint);
                $scope.closeConstraintModal();
            } else if ($scope.constraintType == "subsetRange") {
                if (!$scope.form.subsetCountForm.$valid || $scope.invalidCountMinSize()) {
                    return;
                }
                var shouldBool = $scope.shouldBool;
                var countMin = parseInt($scope.countMin, 10);
                var countMax = parseInt($scope.countMax, 10);
                var withBool = $scope.withBool;
                var field = $scope.selectedParam;
                var optVal = $scope.optVal;
                var constraint = SubsetCountConstraint(shouldBool, countMin, countMax, withBool, field, optVal);
                ConstraintHolder.addConstraint(constraint);
                $scope.closeConstraintModal();
            } else if ($scope.constraintType == "subsetSimilarity") {
                if (!$scope.form.subsetSimForm.$valid) {
                    return;
                }
                var shouldBool = $scope.shouldBool;
                var field = $scope.selectedParam;
                var constraint = SubsetSimilarityConstraint(shouldBool, field);
                ConstraintHolder.addConstraint(constraint);
                $scope.closeConstraintModal();
            } else if ($scope.constraintType == "boolRange") {
                if (!$scope.form.boolCountForm.$valid || $scope.invalidCountMinSize()) {
                    return;
                }
                var shouldBool = $scope.shouldBool;
                var countMin = parseInt($scope.countMin, 10);
                var countMax = parseInt($scope.countMax, 10);
                var withBool = $scope.withBool;
                var field = $scope.selectedParam;
                var constraint = BooleanCountConstraint(shouldBool, countMin, countMax, withBool, field);
                ConstraintHolder.addConstraint(constraint);
                $scope.closeConstraintModal();
            } 
        }
}]);

})();