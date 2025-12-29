/* Modern Invoice System - JavaScript */

document.addEventListener('DOMContentLoaded', function() {
  
  // Search functionality
  const searchInput = document.getElementById('search');
  if (searchInput) {
    searchInput.addEventListener('keyup', function() {
      const searchTerm = this.value.toLowerCase();
      const tableRows = document.querySelectorAll('#myTable tr');
      
      tableRows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(searchTerm) ? '' : 'none';
      });
    });
  }

  // Modify Invoice Modal
  const modifyButtons = document.querySelectorAll('.btn-invoice-mod');
  modifyButtons.forEach(btn => {
    btn.addEventListener('click', function() {
      const invoiceId = this.dataset.id;
      const invoiceIdInput = document.getElementById('invoice_id');
      if (invoiceIdInput) {
        invoiceIdInput.value = invoiceId;
      }
    });
  });

  // Delete Invoice Modal
  const deleteButtons = document.querySelectorAll('.btn-invoice-del');
  deleteButtons.forEach(btn => {
    btn.addEventListener('click', function() {
      const invoiceId = this.dataset.id;
      const form = document.querySelector('#deleteModal form');
      if (form) {
        form.action = `/invoices/${invoiceId}/delete/`;
      }
    });
  });

  // Invoice form - Dynamic calculations
  const wrapper = document.getElementById('wrapper');
  const btnAdd = document.getElementById('btn-add');
  const btnRemove = document.getElementById('btn-remove');

  if (wrapper && btnAdd && btnRemove) {
    function updateTotals() {
      let subtotal = 0;
      document.querySelectorAll('.article-row').forEach(row => {
        const qty = parseFloat(row.querySelector('input[name$="quantity"]').value) || 0;
        const price = parseFloat(row.querySelector('input[name$="unit_price"]').value) || 0;
        const lineTotal = qty * price;
        const lineTotalInput = row.querySelector('.line-total');
        if (lineTotalInput) {
          lineTotalInput.value = lineTotal.toFixed(2);
        }
        subtotal += lineTotal;
      });
      
      const tax = subtotal * 0.19;
      const total = subtotal + tax;
      
      const subtotalEl = document.getElementById('subtotal');
      const taxEl = document.getElementById('tax');
      const totalEl = document.getElementById('total');
      
      if (subtotalEl) subtotalEl.textContent = subtotal.toFixed(2) + ' FCFA';
      if (taxEl) taxEl.textContent = tax.toFixed(2) + ' FCFA';
      if (totalEl) totalEl.textContent = total.toFixed(2) + ' FCFA';
    }

    btnAdd.addEventListener('click', function(e) {
      e.preventDefault();
      const firstRow = wrapper.querySelector('.article-row');
      if (firstRow) {
        const clone = firstRow.cloneNode(true);
        clone.querySelectorAll('input').forEach(input => input.value = '');
        wrapper.appendChild(clone);
        attachInputListeners();
        updateTotals();
      }
    });

    btnRemove.addEventListener('click', function(e) {
      e.preventDefault();
      if (wrapper.children.length > 1) {
        wrapper.lastElementChild.remove();
        updateTotals();
      }
    });

    function attachInputListeners() {
      document.querySelectorAll('input[name$="quantity"], input[name$="unit_price"]').forEach(input => {
        input.removeEventListener('change', updateTotals);
        input.removeEventListener('keyup', updateTotals);
        input.addEventListener('change', updateTotals);
        input.addEventListener('keyup', updateTotals);
      });
    }

    attachInputListeners();
    updateTotals();
  }

  // Alert auto-dismiss
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(alert => {
    setTimeout(() => {
      const bsAlert = new bootstrap.Alert(alert);
      bsAlert.close();
    }, 5000);
  });

  // Print functionality
  const printButtons = document.querySelectorAll('[data-action="print"]');
  printButtons.forEach(btn => {
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      window.print();
    });
  });

});
