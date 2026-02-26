(function () {
  'use strict';

  var STORAGE_KEY = 'londonplumberai_outreach';

  function loadProspects() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      return raw ? JSON.parse(raw) : [];
    } catch (e) {
      return [];
    }
  }

  function saveProspects(prospects) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(prospects));
  }

  function generateId() {
    return 'id_' + Date.now() + '_' + Math.random().toString(36).slice(2, 9);
  }

  var dialog = document.getElementById('prospect-dialog');
  var form = document.getElementById('prospect-form');
  var listEl = document.getElementById('outreach-list');
  var emptyEl = document.getElementById('outreach-empty');
  var filterStatus = document.getElementById('filter-status');
  var btnAdd = document.getElementById('btn-add');
  var btnExport = document.getElementById('btn-export');
  var dialogCancel = document.getElementById('dialog-cancel');

  function getFormData() {
    return {
      id: document.getElementById('prospect-id').value || generateId(),
      name: document.getElementById('prospect-name').value.trim(),
      business: document.getElementById('prospect-business').value.trim(),
      phone: document.getElementById('prospect-phone').value.trim(),
      email: document.getElementById('prospect-email').value.trim(),
      source: document.getElementById('prospect-source').value.trim(),
      status: document.getElementById('prospect-status').value,
      lastContact: document.getElementById('prospect-last-contact').value || '',
      notes: document.getElementById('prospect-notes').value.trim()
    };
  }

  function setFormData(p) {
    document.getElementById('prospect-id').value = p.id || '';
    document.getElementById('prospect-name').value = p.name || '';
    document.getElementById('prospect-business').value = p.business || '';
    document.getElementById('prospect-phone').value = p.phone || '';
    document.getElementById('prospect-email').value = p.email || '';
    document.getElementById('prospect-source').value = p.source || '';
    document.getElementById('prospect-status').value = p.status || 'Not contacted';
    document.getElementById('prospect-last-contact').value = p.lastContact || '';
    document.getElementById('prospect-notes').value = p.notes || '';
  }

  function renderList() {
    var prospects = loadProspects();
    var statusFilter = filterStatus ? filterStatus.value : '';
    var filtered = statusFilter
      ? prospects.filter(function (p) { return p.status === statusFilter; })
      : prospects;

    listEl.innerHTML = '';
    if (filtered.length === 0) {
      emptyEl.hidden = false;
      return;
    }
    emptyEl.hidden = true;

    filtered.forEach(function (p) {
      var card = document.createElement('div');
      card.className = 'outreach-card';
      card.innerHTML =
        '<div class="outreach-card-header">' +
          '<span class="outreach-card-name">' + escapeHtml(p.name || 'Unnamed') + '</span>' +
          '<div class="outreach-card-badges">' +
            '<span class="badge-status">' + escapeHtml(p.status) + '</span>' +
            (p.business ? '<span>' + escapeHtml(p.business) + '</span>' : '') +
          '</div>' +
        '</div>' +
        '<div class="outreach-card-details">' +
          (p.phone ? '<p>Phone: ' + escapeHtml(p.phone) + '</p>' : '') +
          (p.email ? '<p>Email: ' + escapeHtml(p.email) + '</p>' : '') +
          (p.source ? '<p>Source: ' + escapeHtml(p.source) + '</p>' : '') +
          (p.lastContact ? '<p>Last contact: ' + escapeHtml(p.lastContact) + '</p>' : '') +
          (p.notes ? '<p>Notes: ' + escapeHtml(p.notes) + '</p>' : '') +
        '</div>' +
        '<div class="outreach-card-actions">' +
          '<button type="button" class="btn btn-secondary btn-edit" data-id="' + escapeHtml(p.id) + '">Edit</button>' +
          '<button type="button" class="btn btn-secondary btn-delete" data-id="' + escapeHtml(p.id) + '">Delete</button>' +
        '</div>';
      listEl.appendChild(card);
    });

    listEl.querySelectorAll('.btn-edit').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var id = btn.getAttribute('data-id');
        var prospects = loadProspects();
        var found = prospects.find(function (p) { return p.id === id; });
        if (found) {
          document.getElementById('dialog-title').textContent = 'Edit prospect';
          setFormData(found);
          dialog.showModal();
        }
      });
    });

    listEl.querySelectorAll('.btn-delete').forEach(function (btn) {
      btn.addEventListener('click', function () {
        if (!confirm('Delete this prospect?')) return;
        var id = btn.getAttribute('data-id');
        var prospects = loadProspects().filter(function (p) { return p.id !== id; });
        saveProspects(prospects);
        renderList();
      });
    });
  }

  function escapeHtml(s) {
    if (!s) return '';
    var div = document.createElement('div');
    div.textContent = s;
    return div.innerHTML;
  }

  function openAdd() {
    document.getElementById('dialog-title').textContent = 'Add prospect';
    setFormData({ status: 'Not contacted' });
    dialog.showModal();
  }

  form.addEventListener('submit', function () {
    var data = getFormData();
    var prospects = loadProspects();
    var idx = prospects.findIndex(function (p) { return p.id === data.id; });
    if (idx >= 0) {
      prospects[idx] = data;
    } else {
      prospects.push(data);
    }
    saveProspects(prospects);
    dialog.close();
    renderList();
  });

  if (dialogCancel) {
    dialogCancel.addEventListener('click', function () { dialog.close(); });
  }

  if (filterStatus) {
    filterStatus.addEventListener('change', renderList);
  }

  if (btnAdd) {
    btnAdd.addEventListener('click', openAdd);
  }

  if (btnExport) {
    btnExport.addEventListener('click', function () {
      var prospects = loadProspects();
      if (prospects.length === 0) {
        alert('No prospects to export.');
        return;
      }
      var headers = ['Name', 'Business', 'Phone', 'Email', 'Source', 'Status', 'Last contact', 'Notes'];
      var rows = prospects.map(function (p) {
        return [
          p.name || '',
          p.business || '',
          p.phone || '',
          p.email || '',
          p.source || '',
          p.status || '',
          p.lastContact || '',
          (p.notes || '').replace(/"/g, '""')
        ].map(function (cell) { return '"' + cell + '"'; }).join(',');
      });
      var csv = [headers.join(','), rows.join('\n')].join('\n');
      var blob = new Blob([csv], { type: 'text/csv;charset=utf-8' });
      var a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = 'londonplumberai-outreach-' + new Date().toISOString().slice(0, 10) + '.csv';
      a.click();
      URL.revokeObjectURL(a.href);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', renderList);
  } else {
    renderList();
  }
})();
