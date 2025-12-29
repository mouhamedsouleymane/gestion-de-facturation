(function () {
  'use strict';

  angular
    .module('invoiceApp')
    .controller('InvoicesController', ['ApiService', function (ApiService) {
      const vm = this;

      vm.loading = true;
      vm.q = '';
      vm.invoices = [];

      vm.load = function () {
        vm.loading = true;
        ApiService.listInvoices({ q: vm.q }).then(function (res) {
          vm.invoices = res.data.results || res.data;
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
