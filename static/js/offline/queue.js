(function(window){
  function uuid(){
    if (crypto && crypto.randomUUID) return crypto.randomUUID();
    return 'id-' + Date.now() + '-' + Math.random().toString(36).slice(2,9);
  }

  function getCookie(name){
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
  }

  function serializeForm(form){
    const data = {};
    const formData = new FormData(form);

    for (const [key, value] of formData.entries()){
      if (key === 'csrfmiddlewaretoken') continue;
      if (value instanceof File){
        if (!value.name) continue;
        continue;
      }
      data[key] = value;
    }

    return data;
  }

  async function getPendingCount(){
    return window.OfflineDB.getAllOutbox().then(items => items.length).catch(() => 0);
  }

  function getStatusElement(){
    if (!window.__offlineStatusElement){
      window.__offlineStatusElement = document.getElementById('offline-status-indicator');
    }
    return window.__offlineStatusElement;
  }

  function updateBadge(text, bgClass){
    const el = getStatusElement();
    if (!el) return;
    el.textContent = text;
    el.className = `badge ${bgClass} text-white me-2`;
  }

  async function refreshStatus(){
    const pending = await getPendingCount();
    if (!navigator.onLine){
      const label = pending > 0 ? `Offline · ${pending} pendiente(s)` : 'Offline';
      updateBadge(label, 'bg-danger');
      return;
    }

    if (pending > 0){
      updateBadge(`Sincronizando · ${pending}`, 'bg-warning');
      return;
    }

    updateBadge('En línea', 'bg-success');
  }

  async function processOutbox(){
    const items = await window.OfflineDB.getAllOutbox();
    if (!items || items.length === 0){
      await refreshStatus();
      return;
    }

    updateBadge(`Sincronizando · ${items.length}`, 'bg-warning');

    for (const it of items){
      try{
        const resp = await fetch(it.url, {
          method: it.method,
          headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken') || ''
          },
          body: JSON.stringify(it.body),
          credentials: 'include'
        });

        if (resp.ok){
          await window.OfflineDB.removeOutboxItem(it.id);
          const remaining = await getPendingCount();
          updateBadge(`Sincronizando · ${remaining}`, 'bg-warning');
        } else {
          console.warn('Offline sync failed:', resp.status, it);
          await refreshStatus();
          return;
        }
      } catch (err){
        console.error('Offline sync network error:', err);
        await refreshStatus();
        return;
      }
    }

    await refreshStatus();
  }

  async function enqueueOperation({url, method='POST', body={}, client_id=null}){
    if (!client_id) client_id = body.codigo || uuid();
    const op = {
      id: uuid(),
      client_id,
      method,
      url,
      body,
      ts: Date.now()
    };
    await window.OfflineDB.addOutboxItem(op);
    await refreshStatus();
    return op;
  }

  function registerFormInterceptor({formId, url}){
    const form = document.getElementById(formId);
    if (!form) return;

    form.addEventListener('submit', async function(event){
      if (navigator.onLine) return;
      event.preventDefault();
      const body = serializeForm(form);
      await enqueueOperation({url, body});
      alert('Guardado en modo offline. Se sincronizará cuando haya conexión.');
      form.reset();
    });
  }

  window.OfflineQueue = {
    uuid,
    enqueueOperation,
    processOutbox,
    registerFormInterceptor,
    serializeForm
  };

  window.addEventListener('online', () => {
    console.log('Reconectado. Iniciando sincronización offline.');
    processOutbox();
  });

  window.addEventListener('offline', () => {
    refreshStatus();
  });

  window.addEventListener('load', () => {
    refreshStatus();
    if (navigator.onLine) processOutbox();
  });

})(window);
