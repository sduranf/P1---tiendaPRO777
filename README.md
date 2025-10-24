# TiendaPRO777 - Tienda de Camisas Personalizadas con IA

## Descripción
**TiendaPRO777** es una plataforma web avanzada para la personalización y compra de prendas de vestir, desarrollada con Django. La aplicación integra **Inteligencia Artificial** para generar diseños personalizados automáticamente, permitiendo a los usuarios crear camisetas, camibuzos y hoodies únicos con diseños generados por IA.

### Características Principales
- **Generación de diseños con IA** usando Hugging Face Stable Diffusion
- **Catálogo completo** de camisetas, camibuzos y hoodies
- **Personalización avanzada** con control de posición y tamaño
- **Sistema de carrito** con productos personalizados
- **Múltiples tipos de usuario** (Clientes, Empresas, Administradores)
- **Generación automática de PDFs** para recibos
- **Sistema de empresas** para gestión de pedidos

## Requisitos del Sistema
- **Python 3.8+** (recomendado 3.9+)
- **Django 4.2.7**
- **Base de datos SQLite** (por defecto)
- **Token de Hugging Face** para funcionalidades de IA

## Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd P1---tiendaPRO777
```

### 2. Crear entorno virtual (recomendado)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Crea un archivo `IA.env` en la raíz del proyecto:
```env
HF_TOKEN=tu_token_de_huggingface_aqui
```

**Obtener token de Hugging Face:**
1. Ve a [huggingface.co](https://huggingface.co)
2. Crea una cuenta o inicia sesión
3. Ve a Settings → Access Tokens
4. Crea un nuevo token con permisos de lectura

### 5. Configurar la base de datos
```bash
python manage.py migrate
```

### 6. Crear superusuario (opcional)
```bash
python manage.py createsuperuser
```

### 7. Ejecutar el servidor
```bash
python manage.py runserver
```

## Acceso a la Aplicación
- **URL principal**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Panel de administración**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## Funcionalidades Principales

### Para Clientes
- **Catálogo de productos**: `/` - Explora camisetas, camibuzos y hoodies
- **Detalle de producto**: `/items/<id>/` - Información detallada del producto
- **Personalización con IA**: `/personalizaciones/personalizar/<id>/` - Crea diseños únicos
- **Carrito de compras**: `/cart/` - Gestiona tus productos personalizados
- **Historial de compras**: `/profile/purchase-history/` - Ve tus pedidos anteriores

### Para Empresas
- **Gestión de pedidos**: `/items/pedidos-empresa/` - Administra órdenes asignadas
- **Panel de empresa**: Acceso especializado para empresas registradas

### Para Administradores
- **Panel de administración**: `/admin/` - Gestión completa del sistema
- **Gestión de usuarios**: Control de clientes y empresas
- **Gestión de productos**: Catálogo y categorías
- **Gestión de diseños**: Control de plantillas base

## Funcionalidades de IA

### Generación de Diseños
- **Prompt personalizado**: Describe tu diseño ideal
- **Múltiples estilos**: Animales, texto, geométrico, abstracto, logos
- **Control de posición**: Ajusta ubicación y tamaño del diseño
- **Vista previa**: Visualiza el resultado antes de comprar

### Tipos de Diseños Soportados
- **Animales**: Diseños de mascotas y animales
- **Texto**: Frases y palabras personalizadas
- **Geométrico**: Formas y patrones modernos
- **Abstracto**: Arte y diseños artísticos
- **Logos**: Diseños corporativos

## Estructura del Proyecto
```
P1---tiendaPRO777/
├── items/                 # Catálogo de productos y pedidos
├── cart/                  # Sistema de carrito de compras
├── core/                  # Usuarios y autenticación
├── personalizaciones/     # Diseños y personalización con IA
├── user_profile/         # Perfiles de usuario
├── mshop/               # Configuración principal de Django
└── media/               # Archivos multimedia (imágenes, PDFs)
```

## Tecnologías Utilizadas
- **Backend**: Django 4.2.7
- **Base de datos**: SQLite
- **IA**: Hugging Face Stable Diffusion XL
- **Procesamiento de imágenes**: Pillow, CairoSVG
- **Generación de PDFs**: ReportLab
- **Formularios**: Django Crispy Forms + Bootstrap 4
- **Frontend**: HTML, CSS, JavaScript, Bootstrap

## Notas Importantes
- Los productos personalizados se agregan automáticamente al carrito
- Los diseños generados por IA se guardan en la base de datos
- El sistema genera PDFs automáticamente para cada compra
- Las empresas pueden gestionar pedidos asignados aleatoriamente
- Los usuarios pueden ajustar posición y tamaño de sus diseños

## Solución de Problemas

### Error de conexión con Hugging Face
- Verifica que tu token esté correctamente configurado en `IA.env`
- Asegúrate de tener conexión a internet
- El sistema tiene un fallback local si la API falla

### Problemas con imágenes
- Verifica que Pillow esté instalado correctamente
- Asegúrate de que la carpeta `media/` tenga permisos de escritura

## Soporte
Para dudas, reportes de bugs o sugerencias, contacta al equipo de desarrollo.

---
**Desarrollado con Django y IA**
