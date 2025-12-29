(function () {
  'use strict';

  angular
    .module('invoiceApp', ['ngRoute'])
    .config(['$interpolateProvider', '$httpProvider', function ($interpolateProvider, $httpProvider) {
      // Avoid conflict with Django templates
      $interpolateProvider.startSymbol('{$');
      $interpolateProvider.endSymbol('$}');

      // CSRF support for Django
      $httpProvider.defaults.xsrfCookieName = 'csrftoken';
      $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

      // Identify AJAX requests
      $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    }]);
})();
