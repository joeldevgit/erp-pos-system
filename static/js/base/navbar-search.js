document.addEventListener('DOMContentLoaded', function () {

    const searchForm = document.getElementById('searchForm');
    const btnSearch = document.getElementById('btnSearch');
    const btnCloseSearch = document.getElementById('btnCloseSearch');
    const topbarTitle = document.getElementById('topbarTitle');
    const topbar = document.querySelector('.topbar');
    const searchInput = searchForm?.querySelector('input[name="q"]');
    const inventoryItems = document.querySelectorAll('.inventario-item');

    function isMobileOrTablet() {
        return window.innerWidth <= 991.98;
    }

    function openSearch() {
        searchForm?.classList.add('show');
        btnSearch?.classList.add('d-none');

        if (isMobileOrTablet()) {
            topbarTitle?.classList.add('is-hidden');
            topbar?.classList.add('search-open');
        }

        setTimeout(() => {
            searchInput?.focus();
        }, 50);
    }

    function closeSearch() {
        searchForm?.classList.remove('show');
        btnSearch?.classList.remove('d-none');

        topbarTitle?.classList.remove('is-hidden');
        topbar?.classList.remove('search-open');
    }

    function filterInventoryItems() {
        if (!searchInput) {
            return;
        }

        const query = searchInput.value.toLowerCase().trim();

        inventoryItems.forEach(item => {
            const codigo = item.dataset.codigo || '';
            const nombre = item.dataset.nombre || '';
            const matches = codigo.toLowerCase().includes(query) || nombre.toLowerCase().includes(query);
            item.style.display = matches ? '' : 'none';
        });
    }

    btnSearch?.addEventListener('click', openSearch);
    btnCloseSearch?.addEventListener('click', () => {
        if (searchInput) {
            searchInput.value = '';
        }

        inventoryItems.forEach(item => {
            item.style.display = '';
        });

        closeSearch();
        searchInput?.focus();
    });

    searchInput?.addEventListener('input', filterInventoryItems);

});
