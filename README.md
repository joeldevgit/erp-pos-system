# 🚀 MyERP POS Django GOD

Sistema ERP/POS desarrollado con Django para la gestión de inventario, productos, usuarios y auditoría.

## 📋 Descripción

MyERP POS es una aplicación web desarrollada con Django que permite administrar productos, controlar inventario, gestionar usuarios y registrar auditorías de acciones realizadas dentro del sistema.

El proyecto implementa buenas prácticas de desarrollo como pruebas automatizadas, API REST, CI/CD y arquitectura modular.

---

## ✨ Características

- 📦 Gestión de productos
- 📊 Control de inventario
- 👥 Gestión de usuarios
- 🔐 Roles y permisos
- 📝 Auditoría de acciones
- 🌐 API REST
- 🧪 Pruebas automatizadas
- 🚀 Despliegue en Render
- ⚙️ GitHub Actions para CI/CD

---

## 📸 Capturas

### Dashboard

![Dashboard](docs/images/dashboard.png)

### Inventario

![Inventario](docs/images/inventario.png)

### Productos

![Productos](docs/images/productos.png)

### Usuarios

![Usuarios](docs/images/usuarios.png)

---

## 🏗 Arquitectura

```text
Cliente Web
     │
     ▼
Views / API
     │
     ▼
Use Cases
     │
     ▼
Services
     │
     ▼
Repositories
     │
     ▼
Base de Datos
```

---

## 📂 Estructura del Proyecto

```text
myerpposdj/
│
├── apps/
│   ├── productos/
│   ├── inventario/
│   ├── usuarios/
│   ├── auditoria/
│   └── api/
│
├── config/
├── tests/
├── docs/
├── requirements/
└── manage.py
```

---

## 📦 Módulos

### Productos
- Crear productos
- Editar productos
- Eliminar productos
- Consultar productos

### Inventario
- Entradas de stock
- Salidas de stock
- Control de existencias

### Usuarios
- Registro de usuarios
- Roles y permisos

### Auditoría
- Registro de actividades
- Historial de cambios

### API
- Endpoints REST
- Integración con aplicaciones externas

---

## 🔌 API REST

### Obtener productos

```http
GET /api/productos/
```

### Crear producto

```http
POST /api/productos/
```

### Actualizar producto

```http
PUT /api/productos/{id}/
```

### Eliminar producto

```http
DELETE /api/productos/{id}/
```

---

## ⚙️ Instalación

### Clonar repositorio

```bash
git clone https://github.com/dev26bmg/myerpposdj.git
cd myerpposdj
```

### Crear entorno virtual

```bash
python -m venv venv
```

### Activar entorno virtual

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Instalar dependencias

```bash
pip install -r requirements.txt
```

### Aplicar migraciones

```bash
python manage.py migrate
```

### Crear superusuario

```bash
python manage.py createsuperuser
```

### Ejecutar servidor

```bash
python manage.py runserver
```

---

## 🧪 Pruebas

Ejecutar todas las pruebas:

```bash
pytest
```

o

```bash
python manage.py test
```

---

## ☁️ Despliegue en Render

### Variables de entorno

```env
SECRET_KEY=tu_clave
DEBUG=False
DATABASE_URL=postgresql://...
ALLOWED_HOSTS=...
```

### Build Command

```bash
pip install -r requirements.txt
python manage.py migrate
```

### Start Command

```bash
gunicorn config.wsgi
```

---

## 🔄 CI/CD

GitHub Actions ejecuta automáticamente:

- Tests
- Validaciones
- Deploy a Render

---

## 🛠 Tecnologías

- Python 3
- Django
- Django REST Framework
- PostgreSQL
- Pytest
- Playwright
- GitHub Actions
- Render

---

## 📈 Estado del Proyecto

Proyecto en desarrollo activo.

---

## 👨‍💻 Autor

Joel

GitHub: https://github.com/dev26bmg

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT.
