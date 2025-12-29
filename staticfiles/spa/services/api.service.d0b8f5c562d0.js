(function () {
  'use strict';

  angular
    .module('invoiceApp')
    .factory('ApiService', ['$http', function ($http) {
      const base = '/api';

      function listInvoices(params) {
        return $http.get(base + '/invoices/', { params: params || {} });
      }

      function getInvoice(id) {
        return $http.get(base + '/invoices/' + id + '/');
      }

      function listCustomers(params) {
        return $http.get(base + '/customers/', { params: params || {} });
      }

      function getCustomer(id) {
        return $http.get(base + '/customers/' + id + '/');
      }

      return {
        listInvoices,
        getInvoice,
        listCustomers,
        getCustomer
      };
    }]);
})();
