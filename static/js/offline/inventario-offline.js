(function(){
  function initMermaForm(){
    const form = document.getElementById('form-merma');
    if (!form) return;

    form.addEventListener('submit', async function(event){
      if (navigator.onLine) return;
      event.preventDefault();

      await window.OfflineQueue.enqueueOperation({
        url: '/inventario/api/sync/mermas/',
        body: window.OfflineQueue.serializeForm(form)
      });

      alert('Merma guardada en modo offline. Se sincronizará en cuanto vuelvas a conectarte.');
      form.reset();
    });
  }

  window.addEventListener('load', initMermaForm);
})();
