// This file contains the functionality of the allocation page,
// including setting up the angular.js application and sending
// data to the server process.

var app = angular.module('allocator', []);

// A filter to sanitize HTML output before it is
// added to the DOM
app.filter('to_trusted', ['$sce', function($sce) {
    return function(data) {
        return $sce.trustAsHtml(data); 
    };
}]);

// The DataHolder factory manages the student 
// information and makes it accessible to other
// components.
app.factory('DataHolder', function($rootScope) {

    var studentData = '{"44781573": {"name": "OPAL MAYER", "age": 22, "preferences": ["gameplay"]}, "49972059": {"name": "OWEN POWERS", "age": 26, "preferences": []}, "43210058": {"name": "LEANNA HOOPER", "age": 22, "preferences": ["graphics"]}, "49218373": {"name": "CANDRA KNAPP", "age": 20, "preferences": ["gameplay"]}, "41434186": {"name": "ARTIE MERCADO", "age": 20, "preferences": ["gameplay"]}, "41919562": {"name": "MISTIE DECKER", "age": 17, "preferences": ["gameplay"]}, "41733160": {"name": "JENEE HAWKINS", "age": 21, "preferences": ["networking", "gameplay"]}, "47912042": {"name": "GALEN STEVENS", "age": 18, "preferences": ["gameplay"]}, "43077121": {"name": "VEDA DUKE", "age": 26, "preferences": ["ui", "gameplay"]}, "44284944": {"name": "ALYSON SANTOS", "age": 21, "preferences": ["graphics"]}, "49801186": {"name": "NOVELLA HEWITT", "age": 19, "preferences": ["gameplay"]}, "44930399": {"name": "LEONE STRONG", "age": 27, "preferences": ["networking", "graphics"]}, "49435228": {"name": "DANN BARRY", "age": 24, "preferences": ["gameplay"]}, "42000636": {"name": "PERRY WARE", "age": 23, "preferences": ["networking"]}, "46211757": {"name": "EDDIE CRAWFORD", "age": 22, "preferences": ["gameplay"]}, "49845902": {"name": "MITCHELL KIRK", "age": 17, "preferences": ["gameplay"]}}';
    var studentParams = '{"age" : "integer" , "preferences" : "multi-select"}';

    // var constraintData = '[{"constr_type": "IntegerCountConstraint", "name": "age constraint", "field": "age", "priority": 1, "should_bool": true, "count_bxy": [2, 2], "with_bool": true, "value_bxy": [20, 30]}, {"constr_type": "SubsetSimilarityConstraint", "name": "preference constraint", "field": "preferences", "priority": 1, "similar_bool": true, "candidates": ["ui", "networking", "graphics", "gameplay"]}]'; 

    function notify() {
        console.log("emitting data holder event");
        $rootScope.$emit('data-holder-event');
    }

    return {
        setStudentData : function(dataString) {
            studentData = dataString;
            notify();
        },

        getStudentData : function() {
            return studentData;
        },

        setStudentParams : function(dataString) {
            studentParams = dataString;
            notify();
        },

        getStudentParams : function() {
            return studentParams;
        },

        subscribe : function(scope, callback) {
            var handler = $rootScope.$on('data-holder-event', callback);
            scope.$on('$destroy', handler);
        }
    }
});

// The ConstraintHolder factory is responsible
// for managing the list of constraints which
// have been specified by the user. This also
// includes the group size constraints.
app.factory('ConstraintHolder', function($rootScope){

    var constraintList = [];
    var minSize = 3;
    var idealSize = 4;
    var maxSize = 5;
    
    function notify() {
        console.log("emitting constraint holder event");
        $rootScope.$emit('constraint-holder-event');
    }

    return {
        addConstraint : function(constraint) {
            constraintList.push({val : constraint, enabled: false});
            notify();
        },

        toggleConstraint : function(index) {
            var enabled = constraintList[index].enabled;
            constraintList[index].enabled = !enabled;
            notify();
        },

        removeConstraint : function(index) {
            constraintList.splice(index, 1);
            notify();
        },

        getConstraintDetails : function() {
            return [...constraintList];
        },

        getEnabledConstraints : function() {
            result = [];

            constraintList.forEach(function(entry) {
                if (entry.enabled) {
                    result.push(entry.val);
                }
            });

            return result;
        },

        setMinSize : function(size) {
            minSize = size;
            notify();
        },

        setIdealSize : function(size) {
            idealSize = size;
            notify();
        },

        setMaxSize : function(size) {
            maxSize = size;
            notify();
        },

        getMinSize : function() {
            return minSize;
        },

        getIdealSize : function() {
            return idealSize;
        },

        getMaxSize : function() {
            return maxSize;
        },

        subscribe : function(scope, callback) {
            var handler = $rootScope.$on('constraint-holder-event', callback);
            scope.$on('$destroy', handler);
        }
    }
});

// The root controller is responsible for delegating
// the work between the factories
app.controller('rootController', ['$scope', 'DataHolder', 'ConstraintHolder', 
    function($scope, DataHolder, ConstraintHolder) {
        // Initialise the student data and set it to update
        // whenever the input is changed
        $scope.studentData = DataHolder.getStudentData();
        $scope.studentParams = DataHolder.getStudentParams();
        $scope.minSize = ConstraintHolder.getMinSize();
        $scope.idealSize = ConstraintHolder.getIdealSize();
        $scope.maxSize = ConstraintHolder.getMaxSize();

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

        //ConstraintHolder.addConstraint(IntegerCountConstraint(true, 3, 3, true, "age", 20, 30));
        //ConstraintHolder.addConstraint(SubsetSimilarityConstraint(true, "preferences"));
}]);

// The controls controller handles sending allocation
// requests to the server and exporting allocations
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

app.directive('constraintformatselect', function() {
    return {
        template: '<select ng-change="updateConstraintType()" ng-model="constraintType" ng-options="constraint.val as formatMsg(constraint.msg) for constraint in getConstraintForms(selectedParam)"></select>',
        restrict: 'E',
        scope: false
    };
});

app.directive('integercountform', function() {
    return {
        restrict: 'E',
        templateUrl: '/static/html/integerCount.html'
    }
});

app.directive('subsetsimilarityform', function() {
    return {
        restrict: 'E',
        templateUrl: '/static/html/subsetSimilarity.html'
    }
});

app.controller('constraintEntryController', ['$rootScope', '$scope', '$compile', 'ConstraintHolder', 'DataHolder',
    function($rootScope, $scope, $compile, ConstraintHolder, DataHolder){

        $scope.paramData = JSON.parse(DataHolder.getStudentParams())
        $scope.availableParams = Object.keys($scope.paramData);
        $scope.selectedParam = "";
        $scope.constraintType = "";

        var integerConstraintForms = [{msg: "Each team <should/shouldn't> have between <min> and <max> members <with/without> <param> between <min> and <max>", val: "integerCount"}];
        var subsetSimilarityConstraintForms = [{msg: "Each team <should/shouldn't> have similar <param>", val: "subsetSimilarity"}];

        DataHolder.subscribe($scope, function(){
            $scope.availableParams = Object.keys(JSON.parse(DataHolder.getStudentParams()));
        })

        $scope.formatMsg = function(message) {
            return message.replace("<param>", $scope.selectedParam);
        }

        $scope.getConstraintForms = function(param) {
            if ($scope.paramData[param] === "integer") {
                //var integerCount = "Each team <should/shouldn't> have between <min> and <max> members <with/without> " + param + " between <min> and <max>";
                //return [{msg: integerCount, val: "integerCount"}];
                return integerConstraintForms;
            } else if ($scope.paramData[param] === "multi-select") {
                //var subsetSimilarity = "Each team <should/shouldn't> have similar " + param;
                //return [{msg: subsetSimilarity, val: "subsetSimilarity"}];
                return subsetSimilarityConstraintForms;
            }
            return ["???"];
        }

        $scope.updateSelectedParam = function() {
            console.log("selected param changed");
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
                var newParagraph = document.createElement("p");
                newParagraph.innerHTML = "Step 2: Select the form of constraint to apply";
                var newNode = document.createElement("constraintformatselect");
            
                selectContainer.appendChild(newParagraph);
                selectContainer.appendChild(newNode);
            
                // Once it's added, we re-compile it
                $compile(newNode)($scope);
            }
        }

        $scope.updateConstraintType = function() {
            console.log("constraint type changed");
            var inputContainer = document.getElementById('entryConstraintInput');
            if (inputContainer) {
                while (inputContainer.firstChild) {
                    inputContainer.removeChild(inputContainer.firstChild);
                }
                console.log($scope.constraintType);
                var newNode = document.createElement($scope.constraintType + "Form");
                inputContainer.appendChild(newNode);
                $compile(inputContainer)($scope);   
            }
        };

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
            } else if ($scope.constraintType == "subsetSimilarity") {
                var shouldBool = $scope.constr.shouldBool;
                var field = $scope.selectedParam;
                var constraint = SubsetSimilarityConstraint(shouldBool, field);
                ConstraintHolder.addConstraint(constraint);
            }
        }
}]);

// (function(){
//     'use strict';
    
//     // CONSTRAINT INPUTS -------------------------------------------
//     function getConstraintMessage(type, fieldname) {
//         if (type === "integerCount") {
//             return "Each team <should/shouldn't> have between <min> and <max> members <with/without> " + fieldname + " between <min> and <max>.";
//         } else if (type === "subsetSimilarity") {
//             return "Each team <should/shouldn't> have similar " + fieldname + ".";
//         }
//         return "";
//     }

//     function getConstraintMarkup(type, fieldname) {
//         if (type === "integerCount") {
//             return "Each team " 
//                 + "<select ng-model='constr.shouldBool'><option value='true'>SHOULD</option><option value='false'>SHOULDN'T</option></select>"
//                 + "have between " 
//                 + "<input type='number' ng-model='constr.countMin'>" 
//                 + " and " 
//                 + "<input type='number' ng-model='constr.countMax'>" 
//                 + " members " 
//                 + "<select ng-model='constr.withBool'><option value='true'>WITH</option><option value='false'>WITHOUT</option></select>"
//                 + " " + fieldname + " between " 
//                 + "<input type='number' ng-model='constr.fieldMin'>" + " and " 
//                 + "<input type='number' ng-model='constr.fieldMax'>";  
//         } else if (type === "subsetSimilarity") {
//             return "Each team " 
//                 + "<select ng-model='constr.shouldBool'><option value='true'>SHOULD</option><option value='false'>SHOULDN'T</option></select>"
//                 + " have similar " + fieldname;
//         }
//         return "";
//     }    

//     // APPLICATION SETUP -------------------------------------------
//     var app = angular.module('allocator', ['ngSanitize']);

//     // Set up a filter to allow HTML element creation
//     app.filter('trustAsHtml', function($sce) {
//         return function(html) {
//             return $sce.trustAsHtml(html);
//         };
//     });

//     // Set up the angular controller
//     app.controller("allocationController", function($scope, $http, $sce, $compile){

//         // Controller State
//         $scope.minSize = 3;
//         $scope.idealSize = 4;
//         $scope.maxSize = 5;
//         $scope.studentParams = "age,preferences";
//         $scope.studentData = '{"44781573": {"name": "OPAL MAYER", "age": 22, "preferences": ["gameplay"]}, "49972059": {"name": "OWEN POWERS", "age": 26, "preferences": []}, "43210058": {"name": "LEANNA HOOPER", "age": 22, "preferences": ["graphics"]}, "49218373": {"name": "CANDRA KNAPP", "age": 20, "preferences": ["gameplay"]}, "41434186": {"name": "ARTIE MERCADO", "age": 20, "preferences": ["gameplay"]}, "41919562": {"name": "MISTIE DECKER", "age": 17, "preferences": ["gameplay"]}, "41733160": {"name": "JENEE HAWKINS", "age": 21, "preferences": ["networking", "gameplay"]}, "47912042": {"name": "GALEN STEVENS", "age": 18, "preferences": ["gameplay"]}, "43077121": {"name": "VEDA DUKE", "age": 26, "preferences": ["ui", "gameplay"]}, "44284944": {"name": "ALYSON SANTOS", "age": 21, "preferences": ["graphics"]}, "49801186": {"name": "NOVELLA HEWITT", "age": 19, "preferences": ["gameplay"]}, "44930399": {"name": "LEONE STRONG", "age": 27, "preferences": ["networking", "graphics"]}, "49435228": {"name": "DANN BARRY", "age": 24, "preferences": ["gameplay"]}, "42000636": {"name": "PERRY WARE", "age": 23, "preferences": ["networking"]}, "46211757": {"name": "EDDIE CRAWFORD", "age": 22, "preferences": ["gameplay"]}, "49845902": {"name": "MITCHELL KIRK", "age": 17, "preferences": ["gameplay"]}}'
//         $scope.constraintData = '[{"constr_type": "IntegerCountConstraint", "name": "age constraint", "field": "age", "priority": 1, "should_bool": true, "count_bxy": [2, 2], "with_bool": true, "value_bxy": [20, 30]}, {"constr_type": "SubsetSimilarityConstraint", "name": "preference constraint", "field": "preferences", "priority": 1, "similar_bool": true, "candidates": ["ui", "networking", "graphics", "gameplay"]}]'        
//         $scope.constraintList = [];
//         $scope.availableFields = {"age" : "integer", "preferences" : "multi-select"};
        
//         // Returns the dictionary of possible constraint types which can
//         // be created for the given attribute
//         $scope.getConstraintTypes = function(attribute) {
//             var result = {};
//             if (!(attribute in $scope.availableFields)) {
//                 return {};
//             }
//             if ($scope.availableFields[attribute] === "integer") {
//                 result["integerCount"] = getConstraintMessage("integerCount", attribute);
//                 return result;
//             }
//             if ($scope.availableFields[attribute] === "multi-select") {
//                 result["subsetSimilarity"] = getConstraintMessage("subsetSimilarity", attribute);
//                 return result;
//             }
//             return result;
//         }
        
//         $scope.openConstraintModal = function() {
//             var modalHTML = "<div id='constraint-modal'></div>";
//             // modalHTML += "<h2>Add Constraint</h2>"
//             // modalHTML += "<p><strong>Step 1:</strong> Select the parameter to use:</p>";
//             // modalHTML += "<select ng-model='selectedParam' ng-options='x for x in studentParams.split(',')'></select>";
//             // modalHTML += "</div>";

//             var template = angular.element(modalHTML);
//             var linkFn = $compile(template);
//             var result = linkFn($scope);
//             $scope.$apply();

//             console.log(template.html());
//         }

//         // Returns the HTML markup for the form in which users 
//         // will specify the constraint details.
//         $scope.getConstraintHTML = function(constraintType, attribute) {
//             var markup = getConstraintMarkup(constraintType, attribute);
//             //markup += "<button ng-click='works()'>Click Me!</button>";
//             //var compiled = $compile(angular.element(markup))($scope);

//             return markup;
//         }

//         // Adds a new constraint into the constraint list
//         $scope.addConstraint = function(constraint) {
//             var isConstraint = true;
        
//             if (constraint instanceof IntegerCountConstraint) {
//                 // TODO: Add other checks if necessary
//             } else if (constraint instanceof SubsetSimilarityConstraint) {
//                 // TODO: Add other checks if necessary
//             } else {
//                 isConstraint = false;
//             }
//             if (!isConstraint || !(constraint.getField() in $scope.availableFields)) {
//                 return;
//             }
            
//             $scope.constraintList.push(constraint);
//         }

//         // Removes an added constraint from the constraint list
//         $scope.removeConstraint = function(index) {
//             if (index > 0 && index < $scope.constraintList.length) {
//                 $scope.constraintList.splice(index, 1);
//             }
//         }

//         // Set the action to run when the 'Run allocation' button is clicked.
//         $scope.runAllocation = function() {

//             // We need to populate the subset similarity constraints' candidates
//             $scope.constraintList.forEach(function(constraint){
//                 if (constraint instanceof SubsetSimilarityConstraint) {
//                     var field = constraint.getField();
//                     var candidates = new Set();
//                     var students = JSON.parse($scope.studentData);
//                     for (var student in students) {
//                         students[student][field].forEach(item => candidates.add(item));
//                     }
//                     constraint.setCandidates(Array.from(candidates));
//                 }
//             });
            
//             var request = $http({
//                 method: "post",
//                 url: "/allocator",
//                 data: {
//                     min_size: parseInt($scope.minSize, 10),
//                     ideal_size: parseInt($scope.idealSize, 10),
//                     max_size: parseInt($scope.maxSize, 10),
//                     students: JSON.parse($scope.studentData),   // This will be come from the database
//                     constraints: JSON.parse(JSON.stringify($scope.constraintList))//JSON.parse($scope.constraints) // This will be a call to the constraint container
//                 }
//             }).then(function success(response) {
//                 $scope.teams = response.data['teams'];
//                 console.log(response.data);
//                 console.log(response.data['teams']);
//             }, function error(response) {
//                 console.log("ERROR");
//             });
//         }

//         //$scope.addConstraint(IntegerCountConstraint(true, 3, 3, true, "age", 20, 30));
//         $scope.constraintList.push(SubsetSimilarityConstraint(true, "preferences"));
//     });
// })();