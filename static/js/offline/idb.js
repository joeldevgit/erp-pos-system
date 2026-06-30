(function(window){
  const DB_NAME = 'pos-offline';
  const DB_VERSION = 1;

  function openDB(){
    return new Promise((resolve, reject) => {
      const req = indexedDB.open(DB_NAME, DB_VERSION);
      req.onupgradeneeded = e => {
        const db = e.target.result;
        if(!db.objectStoreNames.contains('outbox')){
          db.createObjectStore('outbox', { keyPath: 'id' });
        }
      };
      req.onsuccess = e => resolve(e.target.result);
      req.onerror = e => reject(e.target.error);
    });
  }

  function addOutboxItem(item){
    return openDB().then(db => new Promise((res, rej) => {
      const tx = db.transaction('outbox', 'readwrite');
      tx.objectStore('outbox').put(item);
      tx.oncomplete = () => res();
      tx.onerror = e => rej(e.target.error);
    }));
  }

  function getAllOutbox(){
    return openDB().then(db => new Promise((res, rej) => {
      const tx = db.transaction('outbox', 'readonly');
      const req = tx.objectStore('outbox').getAll();
      req.onsuccess = () => res(req.result);
      req.onerror = e => rej(e.target.error);
    }));
  }

  function removeOutboxItem(id){
    return openDB().then(db => new Promise((res, rej) => {
      const tx = db.transaction('outbox', 'readwrite');
      tx.objectStore('outbox').delete(id);
      tx.oncomplete = () => res();
      tx.onerror = e => rej(e.target.error);
    }));
  }

  window.OfflineDB = {
    addOutboxItem,
    getAllOutbox,
    removeOutboxItem
  };

})(window);
