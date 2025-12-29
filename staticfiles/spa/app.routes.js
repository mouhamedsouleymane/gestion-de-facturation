(function () {
  'use strict';

  angular
    .module('invoiceApp')
    .config(['$routeProvider', '$locationProvider', function ($routeProvider, $locationProvider) {
      $routeProvider
        .when('/', {
          templateUrl: '/static/spa/views/dashboard.html',
          controller: 'DashboardController',
          controllerAs: 'vm'
        })
        .when('/invoices', {
          templateUrl: '/static/spa/views/invoices.html',
          controller: 'InvoicesController',
          controllerAs: 'vm'
        })
        .when('/customers', {
          templateUrl: '/static/spa/views/customers.html',
          controller: 'CustomersController',
          controllerAs: 'vm'
        })
        .otherwise({ redirectTo: '/' });

      // Hash-based routing (#/...) works without server rewrite.
      // Keep default to minimize Django URL changes.
      // $locationProvider.html5Mode(true);
    }]);
})();
