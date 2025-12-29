(function () {
  'use strict';

  angular
    .module('invoiceApp')
    .controller('DashboardController', ['ApiService', function (ApiService) {
      const vm = this;

      vm.loading = true;
      vm.stats = {
        totalInvoices: 0,
        paidInvoices: 0,
        pendingInvoices: 0
      };

      vm.recentInvoices = [];

      function computeStats(invoices) {
        vm.stats.totalInvoices = invoices.length;
        vm.stats.paidInvoices = invoices.filter(i => i.paid).length;
        vm.stats.pendingInvoices = vm.stats.totalInvoices - vm.stats.paidInvoices;
      }

      vm.refresh = function () {
        vm.loading = true;
        ApiService.listInvoices({ page_size: 10 }).then(function (res) {
          vm.recentInvoices = res.data.results || res.data;
          computeStats(vm.recentInvoices);
        }).finally(function () {
          vm.loading = false;
        });
      };

      vm.refresh();
    }]);
})();
