var app = angular.module("myApp", []);

app.controller("myCtrl", function ($scope) {
    var ctrl = this;
    ctrl.amount = 1;
    ctrl.init = function (price) {
        console.log(price, ctrl.amount);
        ctrl.price = price;
    };
    console.log(ctrl.amount);
    ctrl.totalCost = function () {
      return ctrl.price * ctrl.amount;
    };
    return ctrl;
});

app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});