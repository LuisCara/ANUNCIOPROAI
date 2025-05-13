
# 🏠 AnuncioProAI

**AnuncioProAI** es una aplicación web desarrollada en Python con Streamlit que permite a profesionales del sector inmobiliario generar anuncios optimizados para portales y redes sociales usando inteligencia artificial.

## 🚀 Funcionalidades destacadas

- ✨ Generación de anuncios persuasivos con GPT-4.
- 🌐 Traducción y localización en 5 idiomas.
- 📸 Mejora automática de imágenes con PIL y Cloudinary.
- 🧠 Análisis de imágenes con GPT-4 Vision.
- 💌 Formulario de contacto con envío de correos mediante SendGrid.
- 📤 Descarga de imágenes procesadas (individuales o en ZIP).

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

### 2. Crea un entorno virtual (opcional pero recomendado)

```bash
python -m venv venv
```

### 3. Activa el entorno virtual

- En Windows:
  ```bash
  venv\Scripts\activate
  ```
- En macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

### 4. Instala las dependencias

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

Una vez configurado todo, ejecuta:

```bash
streamlit run app4.py
```

La app se abrirá automáticamente en tu navegador en `http://localhost:8501`.

---

## 🛠️ Personalización

Puedes adaptar los textos, idiomas o funcionalidad modificando el archivo `app4.py`. Está bien estructurado y documentado por secciones:

- Inicio
- Generador de anuncios
- Planes
- Contacto

---

## 📬 Contacto

Desarrollado por **Luis Cara Galafat**  
📧 [luis.cara@hotmail.com](mailto:luis.cara@hotmail.com)  
🌐 Proyecto personal y educativo basado en IA generativa.

---

## 🧠 Licencia

Este proyecto se utiliza con fines educativos, experimentales y profesionales. No puedes adaptarlo a tus necesidades comerciales bajo tu responsabilidad.
