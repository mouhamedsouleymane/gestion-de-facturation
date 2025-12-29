// Small admin JS enhancements for Invoice System
(function () {
    'use strict';

    // Log for debugging in dev
    if (window && window.console) {
        console.info('Invoice System admin custom script loaded');
    }

    // Add a small helper to mark paid/unpaid status fields visually
    function decorateStatusBadges() {
        document.querySelectorAll('.field-paid, .field-paid_status').forEach(function (el) {
            var text = el.textContent || el.innerText || '';
            if (/true|yes|✓|Paid/i.test(text)) {
                el.classList.add('status-badge', 'status-paid');
            } else if (/false|no|✗|Unpaid/i.test(text)) {
                el.classList.add('status-badge', 'status-unpaid');
            }
        });
    }

    document.addEventListener('DOMContentLoaded', function () {
        try {
            decorateStatusBadges();
        } catch (e) {
            console.debug('admin_custom: decorateStatusBadges failed', e);
        }
    });
})();
