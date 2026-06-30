document.addEventListener("DOMContentLoaded", () => {
    const inputImagen = document.getElementById("id_imagen");
    const preview = document.getElementById("preview");
    const placeholder = document.getElementById("placeholder");
    const buscarProducto = document.getElementById("buscar-producto");

    if (inputImagen) {
        inputImagen.addEventListener("change", async () => {
            const file = inputImagen.files[0];
            if (!file) return;

            const compressedFile = await comprimirImagen(file, 1200, 0.75);
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(compressedFile);
            inputImagen.files = dataTransfer.files;

            preview.src = URL.createObjectURL(compressedFile);
            preview.classList.remove("d-none");
            placeholder.classList.add("d-none");

            preview.onload = () => {
                const ratio = preview.naturalWidth / preview.naturalHeight;
                if (ratio > 0.85 && ratio < 1.15) {
                    preview.style.objectFit = "contain";
                    preview.style.padding = "10px";
                    preview.style.background = "#000";
                } else {
                    preview.style.objectFit = "cover";
                    preview.style.padding = "0";
                }
            };
        });
    }

    document.querySelectorAll(".producto-item").forEach(btn => {
        btn.addEventListener("click", function () {
            document.getElementById("id_nombre").value = this.dataset.nombre || "";
            document.getElementById("id_precio_compra").value = normalizarNumero(this.dataset.precioCompra);
            document.getElementById("id_codigo").value = this.dataset.codigo || "";
            document.getElementById("id_stock").value = normalizarNumero(this.dataset.stock);
            document.getElementById("id_stock_minimo").value = normalizarNumero(this.dataset.stockMinimo);
            document.getElementById("id_unidad").value = this.dataset.unidad || "";
            document.getElementById("id_categoria").value = this.dataset.categoria || "";
            document.getElementById("id_informacion_adicional").value = this.dataset.info || "";

            bootstrap.Modal.getInstance(document.getElementById("modalCopiarProducto")).hide();
        });
    });

    if (buscarProducto) {
        buscarProducto.addEventListener("keyup", () => {
            const texto = buscarProducto.value.toLowerCase();
            document.querySelectorAll(".producto-item").forEach(item => {
                item.style.display = item.textContent.toLowerCase().includes(texto) ? "block" : "none";
            });
        });
    }
});

function comprimirImagen(file, maxWidth = 1200, quality = 0.75) {
    return new Promise((resolve) => {
        const img = new Image();
        img.src = URL.createObjectURL(file);

        img.onload = () => {
            const canvas = document.createElement("canvas");
            let width = img.width;
            let height = img.height;

            if (width > maxWidth) {
                height = Math.round((height * maxWidth) / width);
                width = maxWidth;
            }

            canvas.width = width;
            canvas.height = height;
            const ctx = canvas.getContext("2d");
            ctx.drawImage(img, 0, 0, width, height);

            canvas.toBlob((blob) => {
                const newFile = new File([
                    blob
                ], file.name.replace(/\.[^/.]+$/, ".webp"), {
                    type: "image/webp"
                });
                resolve(newFile);
            }, "image/webp", quality);
        };
    });
}

function eliminarImagen() {
    const inputImagen = document.getElementById("id_imagen");
    const preview = document.getElementById("preview");
    const placeholder = document.getElementById("placeholder");

    if (!inputImagen) return;

    inputImagen.value = "";
    preview.src = "";
    preview.classList.add("d-none");
    placeholder.classList.remove("d-none");
}

function agregarPrecio() {
    const totalForms = document.getElementById("id_precios_adicionales-TOTAL_FORMS");
    const container = document.getElementById("precios-container");
    const currentCount = parseInt(totalForms.value, 10);

    const html = `
        <div class="border rounded p-3 mb-2">
            <div class="row">
                <div class="col-md-6">
                    <input type="text"
                           name="precios_adicionales-${currentCount}-nombre"
                           class="form-control"
                           placeholder="Nombre">
                </div>
                <div class="col-md-6">
                    <input type="number"
                           step="0.01"
                           name="precios_adicionales-${currentCount}-precio"
                           class="form-control"
                           placeholder="Precio">
                </div>
            </div>
        </div>
    `;

    container.insertAdjacentHTML("beforeend", html);
    totalForms.value = currentCount + 1;
}

function agregarCaducidad() {
    const totalForms = document.getElementById("id_caducidades-TOTAL_FORMS");
    const container = document.getElementById("caducidades-container");
    const currentCount = parseInt(totalForms.value, 10);

    const html = `
        <div class="border rounded p-3 mb-2">
            <div class="row g-2">
                <div class="col-md-4">
                    <input type="text"
                           name="caducidades-${currentCount}-lote"
                           class="form-control"
                           placeholder="Lote">
                </div>
                <div class="col-md-4">
                    <input type="date"
                           name="caducidades-${currentCount}-fecha_caducidad"
                           class="form-control">
                </div>
                <div class="col-md-4">
                    <input type="text"
                        name="caducidades-${currentCount}-informacion"
                        class="form-control"
                        placeholder="Información">
                </div>
            </div>
        </div>
    `;

    container.insertAdjacentHTML("beforeend", html);
    totalForms.value = currentCount + 1;
}

function guardarUnidad() {
    const nombre = document.getElementById("nueva-unidad").value.trim();
    if (!nombre) {
        alert("Ingrese una unidad");
        return;
    }

    fetch(window.PRODUCTOS_URLS.crearUnidadAjax, {
        method: "POST",
        headers: {
            "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ nombre })
    })
    .then(response => response.json())
    .then(data => {
        if (!data.ok) return;

        const select = document.getElementById("id_unidad");
        const option = new Option(data.nombre, data.id, true, true);
        select.add(option);

        document.getElementById("lista-unidades").insertAdjacentHTML("beforeend", `
            <button type="button"
                    class="list-group-item list-group-item-action"
                    onclick="seleccionarUnidad('${data.id}')">
                ${data.nombre}
            </button>
        `);
        document.getElementById("nueva-unidad").value = "";
        bootstrap.Modal.getInstance(document.getElementById("modalUnidad")).hide();
    });
}

function seleccionarUnidad(id) {
    document.getElementById("id_unidad").value = id;
    bootstrap.Modal.getInstance(document.getElementById("modalUnidad")).hide();
}

function guardarCategoria() {
    const nombre = document.getElementById("nueva-categoria").value.trim();
    if (!nombre) {
        alert("Ingrese una categoría");
        return;
    }

    fetch(window.PRODUCTOS_URLS.crearCategoriaAjax, {
        method: "POST",
        headers: {
            "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ nombre })
    })
    .then(response => response.json())
    .then(data => {
        if (!data.ok) return;

        const select = document.getElementById("id_categoria");
        const option = new Option(data.nombre, data.id, true, true);
        select.add(option);

        document.getElementById("lista-categorias").insertAdjacentHTML("beforeend", `
            <button type="button"
                    class="list-group-item list-group-item-action"
                    onclick="seleccionarCategoria('${data.id}')">
                ${data.nombre}
            </button>
        `);
        document.getElementById("nueva-categoria").value = "";
        bootstrap.Modal.getInstance(document.getElementById("modalCategoria")).hide();
    });
}

function seleccionarCategoria(id) {
    document.getElementById("id_categoria").value = id;
    bootstrap.Modal.getInstance(document.getElementById("modalCategoria")).hide();
}

function normalizarNumero(valor) {
    return valor ? valor.replace(/\./g, "").replace(",", ".") : "";
}
