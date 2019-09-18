// This file contains the functionality of the
// allocation page, including setting up the
// angular.js application and sending data to
// the server process.

var app = angular.module('allocator', []);

app.controller("allocationController", function($scope, $http) {
    // set the default values of the inputs
    $scope.minSize = 3;
    $scope.idealSize = 4;
    $scope.maxSize = 5;
    $scope.studentData = '{"44781573": {"name": "OPAL MAYER", "age": 22, "preferences": ["gameplay"]}, "49972059": {"name": "OWEN POWERS", "age": 26, "preferences": []}, "43210058": {"name": "LEANNA HOOPER", "age": 22, "preferences": ["graphics"]}, "49218373": {"name": "CANDRA KNAPP", "age": 20, "preferences": ["gameplay"]}, "41434186": {"name": "ARTIE MERCADO", "age": 20, "preferences": ["gameplay"]}, "41919562": {"name": "MISTIE DECKER", "age": 17, "preferences": ["gameplay"]}, "41733160": {"name": "JENEE HAWKINS", "age": 21, "preferences": ["networking", "gameplay"]}, "47912042": {"name": "GALEN STEVENS", "age": 18, "preferences": ["gameplay"]}, "43077121": {"name": "VEDA DUKE", "age": 26, "preferences": ["ui", "gameplay"]}, "44284944": {"name": "ALYSON SANTOS", "age": 21, "preferences": ["graphics"]}, "49801186": {"name": "NOVELLA HEWITT", "age": 19, "preferences": ["gameplay"]}, "44930399": {"name": "LEONE STRONG", "age": 27, "preferences": ["networking", "graphics"]}, "49435228": {"name": "DANN BARRY", "age": 24, "preferences": ["gameplay"]}, "42000636": {"name": "PERRY WARE", "age": 23, "preferences": ["networking"]}, "46211757": {"name": "EDDIE CRAWFORD", "age": 22, "preferences": ["gameplay"]}, "49845902": {"name": "MITCHELL KIRK", "age": 17, "preferences": ["gameplay"]}}'
    $scope.constraints = '[{"constr_type": "IntegerCountConstraint", "name": "age constraint", "field": "age", "priority": 1, "should_bool": true, "count_bxy": [2, 2], "with_bool": true, "value_bxy": [20, 30]}, {"constr_type": "SubsetSimilarityConstraint", "name": "preference constraint", "field": "preferences", "priority": 1, "similar_bool": true, "candidates": ["ui", "networking", "graphics", "gameplay"]}]'
    
    // Add functionality to the 'Run Allocation' button
    $scope.submit = function() {
        // send form input data as JSON to the server for allocation
        var request = $http({
            method: "post",
            url: "/allocator",
            data: {
                min_size: parseInt($scope.minSize, 10),
                ideal_size: parseInt($scope.idealSize, 10),
                max_size: parseInt($scope.maxSize, 10),
                students: JSON.parse($scope.studentData),
                constraints: JSON.parse($scope.constraints)
            }
        }).then(function success(response) {
            // get the response and populate the variable. Note Angular
            // will automagically load this into the HTML specified
            $scope.teams = response.data['teams'];
            console.log(response.data);
            console.log(response.data['teams']);
        }, function error(response) {
            console.log("ERROR");
        });
    }
});