(function(){
  function initProductForm(){
    window.OfflineQueue.registerFormInterceptor({
      formId: 'form-item',
      url: '/productos/api/sync/productos/'
    });
  }

  window.addEventListener('load', initProductForm);
})();
