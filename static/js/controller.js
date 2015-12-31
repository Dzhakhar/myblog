var postDetailQuant = angular.module('qApp', []);

angular.module('qApp').config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});