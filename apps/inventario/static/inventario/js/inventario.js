(function () {
    'use strict';

    function llenarSelect(select, valores, textoDefault) {
        if (!select) return;
        select.innerHTML = `<option value="">${textoDefault}</option>`;

        [...new Set(valores)]
            .filter(valor => valor && valor.trim() !== '')
            .sort()
            .forEach(valor => {
                const option = document.createElement('option');
                option.value = valor;
                option.textContent = valor;
                select.appendChild(option);
            });
    }

    function aplicarFiltrosInventario() {
        const ordenar = document.getElementById('ordenarInventario')?.value || '';
        const categoria = document.getElementById('categoriaInventario')?.value || '';
        const unidad = document.getElementById('unidadInventario')?.value || '';
        const info = document.getElementById('infoInventario')?.value.toLowerCase().trim() || '';

        const items = document.querySelectorAll('.inventario-item');

        items.forEach(item => {
            const itemCategoria = item.dataset.categoria || '';
            const itemUnidad = item.dataset.unidad || '';
            const itemInfo = (item.dataset.info || '').toLowerCase();

            let visible = true;

            if (categoria && itemCategoria !== categoria) visible = false;
            if (unidad && itemUnidad !== unidad) visible = false;
            if (info && !itemInfo.includes(info)) visible = false;

            item.style.display = visible ? '' : 'none';
        });

        ordenarInventario(ordenar);
    }

    function ordenarInventario(tipo) {
        const row = document.querySelector('.inventario-inventory-grid .row');
        if (!row || !tipo) return;

        const items = Array.from(row.querySelectorAll('.inventario-item'));

        items.sort((a, b) => {
            const nombreA = a.dataset.nombre || '';
            const nombreB = b.dataset.nombre || '';
            const stockA = parseFloat(a.dataset.stock || 0);
            const stockB = parseFloat(b.dataset.stock || 0);
            const precioA = parseFloat(a.dataset.precio || 0);
            const precioB = parseFloat(b.dataset.precio || 0);

            switch (tipo) {
                case 'nombre_asc': return nombreA.localeCompare(nombreB);
                case 'nombre_desc': return nombreB.localeCompare(nombreA);
                case 'stock_asc': return stockA - stockB;
                case 'stock_desc': return stockB - stockA;
                case 'precio_asc': return precioA - precioB;
                case 'precio_desc': return precioB - precioA;
                default: return 0;
            }
        });

        items.forEach(item => row.appendChild(item));
    }

    function cerrarModalFiltros() {
        const modalEl = document.getElementById('modalFiltrosInventario');
        if (!modalEl) return;
        const ModalCtor = window.bootstrap && window.bootstrap.Modal;
        const modal = ModalCtor ? (ModalCtor.getInstance(modalEl) || new ModalCtor(modalEl)) : null;
        if (modal) modal.hide();
    }

    function ocultarBotonFiltrarInfo() {
        const cont = document.getElementById('contenedorBtnFiltrarInfo');
        if (cont) cont.classList.add('d-none');
    }

    document.addEventListener('DOMContentLoaded', () => {
        const btnCantidadMinima = document.getElementById('btnCantidadMinima');
        let filtroActivo = false;

        if (btnCantidadMinima) {
            btnCantidadMinima.addEventListener('click', function (e) {
                e.preventDefault();

                const items = document.querySelectorAll('.inventario-item');

                if (filtroActivo) {
                    items.forEach(item => { item.style.display = ''; });
                    btnCantidadMinima.classList.remove('active-filter');
                    filtroActivo = false;
                    return;
                }

                items.forEach(item => {
                    const stock = parseFloat(item.dataset.stock || 0);
                    item.style.display = (stock <= 0) ? '' : 'none';
                });

                btnCantidadMinima.classList.add('active-filter');
                filtroActivo = true;
            });
        }

        // init filter controls
        const categoriaSelect = document.getElementById('categoriaInventario');
        const unidadSelect = document.getElementById('unidadInventario');
        const ordenarSelect = document.getElementById('ordenarInventario');
        const infoInput = document.getElementById('infoInventario');
        const btnMostrarTodos = document.getElementById('mostrarTodosInventario');
        const items = document.querySelectorAll('.inventario-item');

        const btnFiltrarInfo = document.getElementById('btnFiltrarInfo');
        const contenedorBtnFiltrarInfo = document.getElementById('contenedorBtnFiltrarInfo');

        llenarSelect(
            categoriaSelect,
            [...items].map(item => item.dataset.categoria),
            'Todas las categorías'
        );

        llenarSelect(
            unidadSelect,
            [...items].map(item => item.dataset.unidad),
            'Todas las unidades'
        );

        categoriaSelect && categoriaSelect.addEventListener('change', () => {
            aplicarFiltrosInventario();
            ocultarBotonFiltrarInfo();
            cerrarModalFiltros();
        });

        unidadSelect && unidadSelect.addEventListener('change', () => {
            aplicarFiltrosInventario();
            ocultarBotonFiltrarInfo();
            cerrarModalFiltros();
        });

        ordenarSelect && ordenarSelect.addEventListener('change', () => {
            aplicarFiltrosInventario();
            ocultarBotonFiltrarInfo();
            cerrarModalFiltros();
        });

        infoInput && infoInput.addEventListener('input', () => {
            const texto = infoInput.value.trim();
            if (texto.length > 0 && contenedorBtnFiltrarInfo) contenedorBtnFiltrarInfo.classList.remove('d-none');
            else if (contenedorBtnFiltrarInfo) contenedorBtnFiltrarInfo.classList.add('d-none');
        });

        btnMostrarTodos && btnMostrarTodos.addEventListener('click', () => {
            if (categoriaSelect) categoriaSelect.value = '';
            if (unidadSelect) unidadSelect.value = '';
            if (ordenarSelect) ordenarSelect.value = '';
            if (infoInput) infoInput.value = '';

            aplicarFiltrosInventario();
            ocultarBotonFiltrarInfo();
            cerrarModalFiltros();
        });

        btnFiltrarInfo && btnFiltrarInfo.addEventListener('click', () => {
            aplicarFiltrosInventario();
            ocultarBotonFiltrarInfo();
            cerrarModalFiltros();
        });
    });
})();