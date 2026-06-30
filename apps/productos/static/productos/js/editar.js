const form = document.getElementById('productoForm');

function agregarPrecio() {
    const totalForms = document.getElementById('id_precios_adicionales-TOTAL_FORMS');
    const currentCount = parseInt(totalForms.value, 10);
    const container = document.getElementById('precios-container');

    const html = `
        <div class="border rounded p-2 mb-2">
            <input type="hidden"
                   name="precios_adicionales-${currentCount}-id">

            <div class="row g-2">
                <div class="col-md-6">
                    <input type="text"
                           name="precios_adicionales-${currentCount}-nombre"
                           class="form-control"
                           placeholder="Nombre">
                </div>

                <div class="col-md-5">
                    <input type="number"
                           step="0.01"
                           name="precios_adicionales-${currentCount}-precio"
                           class="form-control"
                           placeholder="Precio">
                </div>
            </div>
        </div>
    `;

    container.insertAdjacentHTML('beforeend', html);
    totalForms.value = currentCount + 1;
}

function agregarCaducidad() {
    const totalForms = document.getElementById('id_caducidades-TOTAL_FORMS');
    const currentCount = parseInt(totalForms.value, 10);
    const container = document.getElementById('caducidades-container');

    const html = `
        <div class="border rounded p-2 mb-2">
            <input type="hidden" name="caducidades-${currentCount}-id">

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

                <div class="col-md-3">
                    <input type="text"
                        name="caducidades-${currentCount}-informacion"
                        class="form-control"
                        placeholder="Información">
                </div>
            </div>
        </div>
    `;

    container.insertAdjacentHTML('beforeend', html);
    totalForms.value = currentCount + 1;
}

function marcarEditado(element) {
    element.classList.remove('guardado');
    element.classList.add('editando');
}

function marcarGuardado() {
    document.querySelectorAll('.editando').forEach(el => {
        el.classList.remove('editando');
        el.classList.add('guardado');

        setTimeout(() => {
            el.classList.remove('guardado');
        }, 1500);
    });
}

let timeout = null;
let guardando = false;
let guardarPendiente = false;

function autoGuardar() {
    clearTimeout(timeout);
    timeout = setTimeout(() => {
        guardarAhora();
    }, 700);
}

function guardarAhora() {
    if (guardando) {
        guardarPendiente = true;
        return;
    }

    guardando = true;
    const formData = new FormData(form);

    fetch(window.location.href, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        },
        credentials: 'same-origin'
    })
    .then(async res => {
        const data = await res.json();

        if (!res.ok || !data.ok) {
            console.error(data);
            return;
        }

        if (data.precios_ids) {
            data.precios_ids.forEach(item => {
                const inputId = document.querySelector(`[name="${item.prefix}-id"]`);
                if (inputId) {
                    inputId.value = item.id;
                }
            });
            document.getElementById('id_precios_adicionales-INITIAL_FORMS').value =
                document.getElementById('id_precios_adicionales-TOTAL_FORMS').value;
        }

        if (data.caducidades_ids) {
            data.caducidades_ids.forEach(item => {
                const inputId = document.querySelector(`[name="${item.prefix}-id"]`);
                if (inputId) {
                    inputId.value = item.id;
                }
            });
            document.getElementById('id_caducidades-INITIAL_FORMS').value =
                document.getElementById('id_caducidades-TOTAL_FORMS').value;
        }

        marcarGuardado();
    })
    .catch(err => console.error(err))
    .finally(() => {
        guardando = false;
        if (guardarPendiente) {
            guardarPendiente = false;
            guardarAhora();
        }
    });
}

if (form) {
    form.addEventListener('input', function (e) {
        if (e.target.matches('input, textarea, select')) {
            marcarEditado(e.target);
            autoGuardar();
        }
    });
}

function eliminarProducto() {
    const isDarkMode = document.body.classList.contains('dark-mode');

    Swal.fire({
        title: '¿Eliminar producto?',
        text: 'Esta acción no se puede deshacer',
        icon: 'warning',
        background: isDarkMode ? '#1e1e1e' : '#ffffff',
        color: isDarkMode ? '#ffffff' : '#000000',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#6c757d',
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            if (window.PRODUCTOS_DELETE_URL) {
                window.location.href = window.PRODUCTOS_DELETE_URL;
            }
        }
    });
}

const inputImagen = document.getElementById('id_imagen');
const preview = document.getElementById('preview');
const placeholder = document.getElementById('placeholder');

if (inputImagen) {
    inputImagen.addEventListener('change', async function () {
        const file = this.files[0];
        if (!file) return;

        const compressedFile = await comprimirImagen(file, 1200, 0.75);
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(compressedFile);

        inputImagen.files = dataTransfer.files;
        preview.src = URL.createObjectURL(compressedFile);

        preview.classList.remove('d-none');
        placeholder.classList.add('d-none');

        marcarEditado(preview);
        autoGuardar();
    });
}

function comprimirImagen(file, maxWidth = 1200, quality = 0.75) {
    return new Promise((resolve) => {
        const img = new Image();
        img.src = URL.createObjectURL(file);

        img.onload = function () {
            const canvas = document.createElement('canvas');
            let width = img.width;
            let height = img.height;

            if (width > maxWidth) {
                height = Math.round((height * maxWidth) / width);
                width = maxWidth;
            }

            canvas.width = width;
            canvas.height = height;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0, width, height);

            canvas.toBlob((blob) => {
                const newFile = new File([
                    blob
                ], file.name.replace(/\.[^/.]+$/, '.webp'), {
                    type: 'image/webp'
                });
                resolve(newFile);
            }, 'image/webp', quality);
        };
    });
}

if (preview) {
    preview.onload = function () {
        const ratio = preview.naturalWidth / preview.naturalHeight;
        if (ratio > 0.85 && ratio < 1.15) {
            preview.style.objectFit = 'contain';
            preview.style.padding = '10px';
            preview.style.background = '#f5f5f5';
        } else {
            preview.style.objectFit = 'cover';
            preview.style.padding = '0';
        }
    };
}
