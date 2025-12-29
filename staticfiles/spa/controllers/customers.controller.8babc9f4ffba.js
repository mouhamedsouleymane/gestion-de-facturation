(function () {
  'use strict';

  angular
    .module('invoiceApp')
    .controller('CustomersController', ['ApiService', function (ApiService) {
      const vm = this;

      vm.loading = true;
      vm.q = '';
      vm.customers = [];

      vm.load = function () {
        vm.loading = true;
        ApiService.listCustomers({ q: vm.q }).then(function (res) {
          vm.customers = res.data.results || res.data;
        }).finally(function () {
          vm.loading = false;
        });
      };

      vm.onSearch = function () {
        vm.load();
      };

      vm.load();
    }]);
})();
