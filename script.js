(function () {
  'use strict';

  const WORKING_DAYS_PER_MONTH = 22;

  function formatPounds(value) {
    return '£' + Math.round(value).toLocaleString('en-GB');
  }

  function updateROI() {
    var missedInput = document.getElementById('missed-calls');
    var jobValueInput = document.getElementById('job-value');
    var monthlyEl = document.getElementById('monthly-loss');
    var annualEl = document.getElementById('annual-loss');

    if (!missedInput || !jobValueInput || !monthlyEl || !annualEl) return;

    var missed = parseInt(missedInput.value, 10) || 0;
    var jobValue = parseFloat(jobValueInput.value) || 0;

    var monthly = missed * jobValue * WORKING_DAYS_PER_MONTH;
    var annual = monthly * 12;

    monthlyEl.textContent = formatPounds(monthly);
    annualEl.textContent = formatPounds(annual);
  }

  function initCalculator() {
    var missedInput = document.getElementById('missed-calls');
    var jobValueInput = document.getElementById('job-value');

    if (missedInput) missedInput.addEventListener('input', updateROI);
    if (missedInput) missedInput.addEventListener('change', updateROI);
    if (jobValueInput) jobValueInput.addEventListener('input', updateROI);
    if (jobValueInput) jobValueInput.addEventListener('change', updateROI);

    updateROI();
  }

  function initContactForm() {
    var form = document.querySelector('.contact-form');
    var successEl = document.getElementById('form-success');
    var errorEl = document.getElementById('form-error');

    if (!form || !successEl || !errorEl) return;

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      errorEl.hidden = true;
      successEl.hidden = true;

      var formData = new FormData(form);
      var action = form.getAttribute('action') || window.location.href;

      fetch(action, {
        method: 'POST',
        body: formData,
        headers: { Accept: 'application/json' }
      })
        .then(function (response) {
          if (response.ok) {
            form.reset();
            form.style.display = 'none';
            successEl.hidden = false;
          } else {
            errorEl.hidden = false;
          }
        })
        .catch(function () {
          errorEl.hidden = false;
        });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      initCalculator();
      initContactForm();
    });
  } else {
    initCalculator();
    initContactForm();
  }
})();
