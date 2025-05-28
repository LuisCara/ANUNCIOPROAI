
# 🏠 AnuncioProAI

**AnuncioProAI** es una aplicación web desarrollada en Python con Streamlit que permite a particulares, profesionales y agencias inmobiliarias generar anuncios optimizados para portales y redes sociales usando inteligencia artificial. También mejora imágenes, analiza fotos y adapta los anuncios en varios idiomas.

---

## 🚀 Funcionalidades destacadas

- ✨ Generación automática de textos persuasivos con IA (GPT-4).
- 🌐 Traducción y localización en 5 idiomas (es, en, fr, it, de).
- 📸 Mejora de imágenes con filtros personalizables y Cloudinary.
- 🧠 Análisis de imágenes con GPT-4 Vision.
- 📤 Descarga de imágenes procesadas individualmente o en ZIP.
- 📄 Generación de anuncios adaptados a portales inmobiliarios o redes sociales.
- 💌 Formulario de contacto con envío automático de correos mediante SendGrid.

---

## 💰 Planes de uso

| Plan              | Precio       | Incluye                                                                 |
|-------------------|--------------|--------------------------------------------------------------------------|
| 🎁 **Gratis**       | 0 € (prueba) | ✅ Hasta 2 anuncios de prueba  <br> ✅ 1 idioma  <br> ✅ Soporte básico por email |
| 💼 **Profesional** | 14,90 €/mes  | ✅ Hasta 50 anuncios/mes  <br> ✅ Hasta 3 idiomas <br> ✅ Soporte prioritario <br> ✅ Generador de imágenes y textos IA |
| 🏢 **Agencia**      | 30 €/mes     | ✅ Hasta 200 anuncios/mes  <br> ✅ Hasta 5 idiomas <br> ✅ Branding personalizado <br> ✅ Soporte premium <br> ✅ Subida masiva (opcional) |

---

## 🧱 Tecnologías usadas

| Tecnología     | Uso principal                                     |
|----------------|--------------------------------------------------|
| Python         | Lenguaje base                                     |
| Streamlit      | Interfaz web interactiva                          |
| OpenAI API     | Generación de textos e interpretación de imágenes |
| Pillow (PIL)   | Procesamiento de imágenes                         |
| Cloudinary     | Almacenamiento y transformación de imágenes       |
| SendGrid       | Envío de correos electrónicos                     |
| dotenv         | Gestión de variables de entorno                   |

---

## ⚙️ Requisitos

- Python 3.9 o superior
- Cuenta en [OpenAI](https://platform.openai.com)
- Cuenta en [SendGrid](https://sendgrid.com)
- Cuenta en [Cloudinary](https://cloudinary.com)

---

## 📁 Instalación

### 1. Clona el repositorio (o descarga los archivos)

```bash
git clone https://github.com/tuusuario/anuncioproai.git
cd anuncioproai
```

### 2. Crea y activa un entorno virtual (opcional pero recomendado)

```bash
python -m venv venv
source venv/bin/activate  # o venv\Scripts\activate en Windows
```

### 3. Instala las dependencias

```bash
pip install -r requirements.txt
```

---

## 🔐 Configura el archivo `.env`

Crea un archivo llamado `.env` en la raíz del proyecto con este contenido:

```env
OPENAI_API_KEY=tu_clave_openai
CLOUDINARY_CLOUD_NAME=tu_cloud_name
CLOUDINARY_API_KEY=tu_api_key_cloudinary
CLOUDINARY_API_SECRET=tu_api_secret_cloudinary
SENDGRID_API_KEY=tu_api_key_sendgrid
SENDGRID_FROM_EMAIL=tu_email_verificado_en_sendgrid
```

⚠️ **Importante:** El email debe estar verificado en tu cuenta de SendGrid.

---

## ▶️ Ejecutar la aplicación

```bash
streamlit run app.py
```

La app se abrirá automáticamente en tu navegador:  
🌐 `http://localhost:8501`

---

## 📬 Contacto

Desarrollado por **Luis Cara Galafat**  
📧 [luis.cara@hotmail.com](mailto:luis.cara@hotmail.com)  
🌐 Proyecto personal y educativo basado en inteligencia artificial generativa.

---

## 🧠 Licencia

Este proyecto tiene fines educativos y profesionales. Su uso comercial queda bajo responsabilidad del usuario.
