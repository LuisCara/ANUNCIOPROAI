import os

# Eliminar variables de entorno SSL problemáticas al inicio
os.environ.pop("SSL_CERT_FILE", None)
os.environ.pop("SSL_CERT_DIR", None)

import streamlit as st
import re
import io
import base64
from PIL import Image, ImageEnhance, ImageFilter
import cloudinary
import cloudinary.uploader
import cloudinary.api
from openai import OpenAI
import json
import certifi
import requests
import zipfile
import tempfile
import logging

from dotenv import load_dotenv
load_dotenv()

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email

# Fuerza a usar certificados válidos
os.environ['SSL_CERT_FILE'] = certifi.where()

# Configurar logging para depuración
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Configurar Cloudinary
try:
    cloudinary.config(
    cloud_name=st.secrets["cloudinary"]["cloud_name"],
    api_key=st.secrets["cloudinary"]["api_key"],
    api_secret=st.secrets["cloudinary"]["api_secret"]
)

except Exception as e:
    st.error(f"Error al configurar Cloudinary: {str(e)}")
    st.stop()

# Inicializa el cliente de OpenAI (solo para análisis de imágenes)
try:
    client  = OpenAI(api_key=st.secrets["openai"]["api_key"])
except Exception as e:
    st.error(f"Error al inicializar el cliente de OpenAI: {str(e)}")
    st.error("Verifica que la variable de entorno OPENAI_API_KEY esté configurada correctamente y que no haya problemas con las variables SSL_CERT_FILE o SSL_CERT_DIR.")
    st.stop()
    
# Configuración de la página
st.set_page_config(page_title="AnuncioProAI", page_icon="🏠", layout="wide")

# Idiomas disponibles y selector
idiomas = {
    "Español": "es",
    "Inglés": "en",
    "Francés": "fr",
    "Italiano": "it",
    "Alemán": "de"
}
idioma_seleccionado = st.sidebar.selectbox("🌐 Idioma / Language", list(idiomas.keys()))
lang = idiomas[idioma_seleccionado]

# Diccionario de textos en diferentes idiomas
textos = {
    "es": {
        "titulo": "AnuncioProAI - Generador de anuncios inmobiliarios con IA",
        "nav": ["Inicio", "Generador", "Planes", "Contacto"],
        "inicio_header": "Bienvenido a AnuncioProAI",
        "inicio_desc": "Genera anuncios inmobiliarios profesionales y atractivos en segundos con la ayuda de la inteligencia artificial.",
        "inicio_puntos": [
            "✅ Optimiza tus anuncios para portales y redes sociales.",
            "✅ Mejora imágenes automáticamente.",
            "✅ Traduce y adapta el texto a varios idiomas."
        ],
        "inicio_mensaje": "¡Comienza a crear tu anuncio ahora!",
        "planes_titulo": "Elige tu plan",
        "contacto_titulo": "Contacto",
        "contacto_desc": "¿Tienes dudas o sugerencias? ¡Escríbenos!",
        "nombre": "Nombre",
        "correo": "Correo electrónico",
        "mensaje": "Mensaje",
        "enviar": "Enviar",
        "error_imagen": "Error al procesar la imagen. Verifica que la imagen sea un PNG o JPEG válido y menor a 4 MB. Si el problema persiste, revisa los logs para detalles o contacta al soporte de Cloudinary."
    },
    "en": {
        "titulo": "AnuncioProAI - AI-powered Real Estate Ad Generator",
        "nav": ["Home", "Generator", "Plans", "Contact"],
        "inicio_header": "Welcome to AnuncioProAI",
        "inicio_desc": "Create professional and attractive real estate ads in seconds with the help of artificial intelligence.",
        "inicio_puntos": [
            "✅ Optimize your ads for portals and social networks.",
            "✅ Automatically enhance images.",
            "✅ Translate and adapt text to multiple languages."
        ],
        "inicio_mensaje": "Start creating your ad now!",
        "planes_titulo": "Choose your plan",
        "contacto_titulo": "Contact",
        "contacto_desc": "Questions or suggestions? Write to us!",
        "nombre": "Name",
        "correo": "Email",
        "mensaje": "Message",
        "enviar": "Send",
        "error_imagen": "Error processing the image. Verify that the image is a valid PNG or JPEG and less than 4 MB. If the issue persists, check the logs for details or contact Cloudinary support."
    },
    "fr": {
        "titulo": "AnuncioProAI - Générateur d'annonces immobilières avec IA",
        "nav": ["Accueil", "Générateur", "Plans", "Contact"],
        "inicio_header": "Bienvenue sur AnuncioProAI",
        "inicio_desc": "Générez des annonces immobilières professionnelles et attrayantes en quelques secondes grâce à l'intelligence artificielle.",
        "inicio_puntos": [
            "✅ Optimisez vos annonces pour les portails et les réseaux sociaux.",
            "✅ Améliorez automatiquement les images.",
            "✅ Traduisez et adaptez le texte en plusieurs langues."
        ],
        "inicio_mensaje": "Commencez à créer votre annonce maintenant !",
        "planes_titulo": "Choisissez votre plan",
        "contacto_titulo": "Contact",
        "contacto_desc": "Des questions ou des suggestions ? Écrivez-nous !",
        "nombre": "Nom",
        "correo": "E-mail",
        "mensaje": "Message",
        "enviar": "Envoyer",
        "error_imagen": "Erreur lors du traitement de l'image. Vérifiez que l'image est un PNG ou JPEG valide et inférieur à 4 Mo. Si le problème persiste, consultez les journaux pour plus de détails ou contactez le support Cloudinary."
    },
    "it": {
        "titulo": "AnuncioProAI - Generatore di annunci immobiliari con IA",
        "nav": ["Home", "Generatore", "Piani", "Contatto"],
        "inicio_header": "Benvenuto su AnuncioProAI",
        "inicio_desc": "Crea annunci immobiliari professionali e accattivanti in pochi secondi con l'aiuto dell'intelligenza artificiale.",
        "inicio_puntos": [
            "✅ Ottimizza i tuoi annunci per portali e social.",
            "✅ Migliora automaticamente le immagini.",
            "✅ Traduci e adatta il testo in più lingue."
        ],
        "inicio_mensaje": "Inizia subito a creare il tuo annuncio!",
        "planes_titulo": "Scegli il tuo piano",
        "contacto_titulo": "Contatto",
        "contacto_desc": "Domande o suggerimenti? Scrivici!",
        "nombre": "Nome",
        "correo": "Email",
        "mensaje": "Messaggio",
        "enviar": "Invia",
        "error_imagen": "Errore durante l'elaborazione dell'immagine. Verifica che l'immagine sia un PNG o JPEG valido e inferiore a 4 MB. Se il problema persiste, controlla i log per dettagli o contatta il supporto Cloudinary."
    },
    "de": {
        "titulo": "AnuncioProAI - KI-gestützter Immobilienanzeigen-Generator",
        "nav": ["Startseite", "Generator", "Pläne", "Kontakt"],
        "inicio_header": "Willkommen bei AnuncioProAI",
        "inicio_desc": "Erstellen Sie professionelle und ansprechende Immobilienanzeigen in Sekunden mit Hilfe von künstlicher Intelligenz.",
        "inicio_puntos": [
            "✅ Optimieren Sie Ihre Anzeigen für Portale und soziale Netzwerke.",
            "✅ Bilder automatisch verbessern.",
            "✅ Text in mehrere Sprachen übersetzen und anpassen."
        ],
        "inicio_mensaje": "Beginnen Sie jetzt mit der Erstellung Ihrer Anzeige!",
        "planes_titulo": "Wählen Sie Ihren Plan",
        "contacto_titulo": "Kontakt",
        "contacto_desc": "Fragen oder Anregungen? Schreiben Sie uns!",
        "nombre": "Name",
        "correo": "E-Mail",
        "mensaje": "Nachricht",
        "enviar": "Senden",
        "error_imagen": "Fehler bei der Verarbeitung des Bildes. Überprüfen Sie, ob das Bild ein gültiges PNG oder JPEG ist und weniger als 4 MB groß ist. Wenn das Problem weiterhin besteht, überprüfen Sie die Protokolle für Details oder wenden Sie sich an den Cloudinary-Support."
    }
}

# Menú y navegación
st.title(textos[lang]["titulo"])
menu = st.sidebar.radio("Navegación", textos[lang]["nav"])

# Inicio
if menu == textos[lang]["nav"][0]:
    st.header(textos[lang]["inicio_header"])
    st.markdown(textos[lang]["inicio_desc"])
    for punto in textos[lang]["inicio_puntos"]:
        st.write(punto)
    st.image("https://images.unsplash.com/photo-1600585154340-be6161a56a0c", use_column_width=True)
    st.success(textos[lang]["inicio_mensaje"])

# Generador
elif menu == textos[lang]["nav"][1]:

    # Inicializar session_state para información adicional
    if "informacion_adicional" not in st.session_state:
        st.session_state.informacion_adicional = ""

    # Tipo de operación
    st.subheader("⚙️ Tipo de operación")
    tipo_operacion = st.selectbox("¿Se trata de una venta o alquiler?", ["Venta", "Alquiler", "Alquiler vacacional", "Alquiler con opción a compra"])

    # Sección de datos del inmueble
    st.subheader("📋 Características del inmueble")
    tipo = st.selectbox("Tipo de propiedad", [
        "Piso", "Ático", "Dúplex", "Estudio / loft", "Casa", "Chalet", "Adosado",
        "Bungalow", "Piso de protección oficial (VPO)", "Finca/Rural", "Cortijo", "Local comercial",
        "Oficina", "Nave industrial", "Terreno", "Mansión"
    ])
    estado = st.selectbox("Estado", ["A demoler", "A reformar", "Buen estado", "Como nuevo", "Nuevo"])
    m2 = st.number_input("m² construidos", min_value=10, max_value=30000)
    m2_utiles = st.number_input("m² útiles", min_value=10, max_value=30000)
    m2_terreno = st.number_input("m² de terreno", min_value=0, max_value=30000)
    habitaciones = st.number_input("Número de habitaciones", min_value=0, max_value=50)
    baños = st.number_input("Número de baños", min_value=0, max_value=10)
    fachada = st.radio("Fachada", ["Exterior", "Interior"])
    ascensor = st.radio("¿Tiene ascensor?", ["Sí tiene", "No tiene"])
    certificado = st.selectbox("Calificación energética", ["A", "B", "C", "D", "E", "F", "G"])
    orientacion = st.selectbox("Orientación", [
        "Norte", "Sur", "Este", "Oeste",
        "Noreste", "Noroeste",
        "Sureste", "Suroeste"
    ])

    # Selección de tipos de suelo
    st.subheader("🪵 Tipos de suelo")
    suelo_interior = st.selectbox("Tipo de suelo en el interior", [
        "Gres", "Parquet", "Tarima flotante", "Baldosa cerámica", "Mármol", "Granito", "Vinílico", "Moqueta", "Cemento pulido", "Laminado", "Corcho"
    ])
    suelo_exterior = st.selectbox("Tipo de suelo en el exterior", [
        "Ninguno", "Grava", "Pavimento de adoquín", "Hormigón", "Terracota", "Decking de madera", "Piedra natural", "Césped artificial", "Pavimento permeable"
    ])

    # Características adicionales
    st.subheader("✨ Extras")
    extras_vivienda = st.multiselect("Características de la vivienda", [
        "Semiamueblado", "Amueblado", "Armarios empotrados", "Aire acondicionado", "Terraza", "Balcón", "Lavadero", "Chimenea", "Trastero", "Plaza de garaje"
    ])
    extras_edificio = st.multiselect("Características del edificio", [
        "Piscina", "Zona verde", "Gimnasio", "Portero", "Acceso adaptado", "Ascensor", "Zonas comunes", "Zona infantil", "Pista de tenis", "Pista de pádel", "Sauna", "Jacuzzi"
    ])

    metros_terraza = 0
    metros_balcon = 0
    metros_trastero = 0
    metros_garaje = 0

    if "Terraza" in extras_vivienda:
        metros_terraza = st.number_input("Metros cuadrados de la terraza", min_value=1, max_value=1000)
    if "Balcón" in extras_vivienda:
        metros_balcon = st.number_input("Metros cuadrados del balcón", min_value=1, max_value=1000)
    if "Trastero" in extras_vivienda:
        metros_trastero = st.number_input("Metros cuadrados del trastero", min_value=1, max_value=1000)
    if "Plaza de garaje" in extras_vivienda:
        metros_garaje = st.number_input("Metros cuadrados de la plaza de garaje", min_value=1, max_value=1000)

    # Localización del inmueble y servicios cercanos
    st.subheader("📍 Localización y servicios cercanos")
    ubicacion = st.text_input("📍 Dirección del inmueble", "Introduce la dirección del inmueble aquí")

    servicios_cercanos = st.multiselect(
        "Selecciona los servicios cercanos",
        ["Centro médico", "Colegios", "Centros comerciales", "Transporte público", "Parques", "Tiendas y restaurantes", "Gimnasios", "Farmacias", "Estaciones de tren", "Aeropuerto"]
    )

    cerca_playa = st.checkbox("Cerca de la playa")
    primera_linea_de_playa = st.checkbox("Primera línea de playa")
    segunda_linea_de_playa = st.checkbox("Segunda línea de playa")
    cerca_montana = st.checkbox("Cerca de la montaña")

    distancia_playa = None
    distancia_montana = None
    if cerca_playa:
        distancia_playa = st.number_input("¿A qué distancia está la playa (en metros)?", min_value=0, step=10)
    if cerca_montana:
        distancia_montana = st.number_input("¿A qué distancia está la montaña (en metros)?", min_value=0, step=10)

    descripcion_servicios = "Estos son los servicios cercanos a la propiedad: "
    if servicios_cercanos:
        descripcion_servicios += ", ".join(servicios_cercanos)
    else:
        descripcion_servicios = "No se han seleccionado servicios cercanos."

    descripcion_cercania = ""
    if cerca_playa:
        descripcion_cercania = f"Está a {distancia_playa} metros de la playa."
    elif cerca_montana:
        descripcion_cercania = f"Está a {distancia_montana} metros de la montaña."

    st.write(f"🔑 **Dirección**: {ubicacion if ubicacion else 'No se ha proporcionado una dirección.'}")
    st.write(f"🏙 **Servicios cercanos**: {descripcion_servicios}")
    if descripcion_cercania:
        st.write(f"🌊/🏞 **Cercanía**: {descripcion_cercania}")

    # Precio y situación legal
    st.subheader("💶 Precio y situación")
    precio = st.number_input("Precio del inmueble (€)", min_value=0)
    gastos = st.number_input("Gastos de comunidad (€ / mes)", min_value=0)
    situacion = st.selectbox("¿Situación excepcional?", [
        "No, en ninguna situación excepcional", "Ocupada ilegalmente", "Alquilada, con inquilinos", "Nuda propiedad"
    ])

    # Información adicional
    st.subheader("📝 Información adicional")
    informacion_adicional = st.text_area("¿Hay algo más que quieras añadir sobre la propiedad?")
    if informacion_adicional:
        st.write("Información adicional:", informacion_adicional)

    # Función para recopilar todos los datos
    def recopilar_datos(destino_seleccionado):
        """Recopila todos los datos introducidos en el formulario"""
        datos = {
            "tipo_operacion": tipo_operacion,
            "tipo": tipo,
            "estado": estado,
            "m2": m2,
            "m2_utiles": m2_utiles,
            "m2_terreno": m2_terreno,
            "habitaciones": habitaciones,
            "baños": baños,
            "fachada": fachada,
            "ascensor": ascensor,
            "certificado": certificado,
            "orientacion": orientacion,
            "suelo_interior": suelo_interior,
            "suelo_exterior": suelo_exterior,
            "extras_vivienda": extras_vivienda,
            "extras_edificio": extras_edificio,
            "metros_terraza": metros_terraza,
            "metros_balcon": metros_balcon,
            "metros_trastero": metros_trastero,
            "metros_garaje": metros_garaje,
            "ubicacion": ubicacion,
            "descripcion_servicios": descripcion_servicios,
            "descripcion_cercania": descripcion_cercania,
            "precio": precio,
            "gastos": gastos,
            "situacion": situacion,
            "informacion_adicional": informacion_adicional if informacion_adicional else "",
            "destino": destino_seleccionado,
        }
        return datos

    # Función para convertir imagen a base64
    def imagen_a_base64(imagen):
        buffered = io.BytesIO()
        imagen.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return img_str

    # Función para aplicar mejoras con PIL
    def aplicar_mejoras_pil(imagen, opciones):
        img = imagen.convert("RGB")
        
        if opciones["mejorar_iluminacion"]:
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(opciones["brillo"])  # Brillo ajustable
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(opciones["contraste"])  # Contraste ajustable

        if opciones["corregir_color"]:
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(opciones["saturacion"])  # Saturación ajustable

        # Nuevas mejoras
        if opciones["mejorar_nitidez"]:
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(opciones["nivel_nitidez"])  # Nitidez ajustable

        if opciones["reducir_ruido"]:
            # PIL no tiene una función directa para reducción de ruido, pero podemos simularlo con un suavizado
            img = img.filter(ImageFilter.GaussianBlur(radius=opciones["nivel_ruido"] * 0.3))

        if opciones["ajustar_sombras"]:
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(opciones["nivel_sombras"])  # Ajuste de sombras (simulado con brillo)

        if opciones["mejorar_detalles"]:
            img = img.filter(ImageFilter.DETAIL)

        if opciones["ajustar_temperatura"]:
            # Ajuste de temperatura (simulado ajustando canales RGB)
            r, g, b = img.split()
            if opciones["temperatura"] > 0:  # Más cálido (aumentar rojo)
                r = r.point(lambda i: i + (opciones["temperatura"] * 50))
            elif opciones["temperatura"] < 0:  # Más frío (aumentar azul)
                b = b.point(lambda i: i + (-opciones["temperatura"] * 50))
            img = Image.merge("RGB", (r, g, b))

        if opciones["recorte_automatico"]:
            # Simulación de recorte automático (centrado y recortado al 80% del tamaño original)
            width, height = img.size
            new_size = int(min(width, height) * 0.8)
            left = (width - new_size) // 2
            top = (height - new_size) // 2
            right = left + new_size
            bottom = top + new_size
            img = img.crop((left, top, right, bottom))

        if opciones["rotar_imagen"]:
            img = img.rotate(opciones["angulo_rotacion"], expand=True)

        if opciones["aplicar_filtro"] != "Ninguno":
            if opciones["aplicar_filtro"] == "HDR":
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(1.3)
                enhancer = ImageEnhance.Sharpness(img)
                img = enhancer.enhance(1.5)
            elif opciones["aplicar_filtro"] == "Vintage":
                enhancer = ImageEnhance.Color(img)
                img = enhancer.enhance(0.7)  # Reducir saturación
                r, g, b = img.split()
                r = r.point(lambda i: i + 20)  # Añadir tono sepia
                img = Image.merge("RGB", (r, g, b))
            elif opciones["aplicar_filtro"] == "Blanco y Negro":
                img = img.convert("L").convert("RGB")

        return img

    # Función para validar imagen
    def validar_imagen(imagen):
        """Valida que la imagen sea válida y cumpla con los requisitos"""
        try:
            # Verificar que sea un objeto PIL válido
            if not isinstance(imagen, Image.Image):
                return False, "La imagen no es un objeto PIL válido."
            
            # Verificar dimensiones
            max_size = 256  # Reducido a la mitad para optimizar tamaño
            if max(imagen.size) > max_size:
                imagen.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
            # Guardar en un buffer para verificar tamaño
            buffer = io.BytesIO()
            imagen.save(buffer, format="JPEG", quality=80)
            size_mb = len(buffer.getvalue()) / (1024 * 1024)  # Tamaño en MB
            if size_mb > 4:
                return False, f"El tamaño de la imagen ({size_mb:.2f} MB) excede el límite de 4 MB."
            
            return True, None
        except Exception as e:
            return False, f"Error al validar la imagen: {str(e)}"

    # Función para verificar si un public_id existe en Cloudinary
    def verificar_public_id(public_id):
        try:
            result = cloudinary.api.resource(public_id)
            return result is not None
        except Exception as e:
            logger.error(f"Error al verificar public_id {public_id}: {str(e)}")
            return False

    # Función para procesar imagen con Cloudinary
    def procesar_imagen_con_ia(imagen, opciones):
        try:
            # Validar imagen
            es_valida, mensaje_error = validar_imagen(imagen)
            if not es_valida:
                st.error(mensaje_error)
                return None

            # Aplicar mejoras locales con PIL
            imagen_mejorada = aplicar_mejoras_pil(imagen, opciones)
            
            # Guardar imagen como JPEG en un archivo temporal
            with tempfile.NamedTemporaryFile(suffix=".jpeg", delete=False) as temp_file:
                imagen_mejorada.save(temp_file.name, format="JPEG", quality=80)  # Reducido para optimizar tamaño
                temp_file_path = temp_file.name

            # Depuración: registrar parámetros
            logger.debug(f"Procesando imagen: {temp_file_path}")
            file_size_mb = os.path.getsize(temp_file_path) / (1024 * 1024)
            logger.debug(f"Tamaño del archivo: {file_size_mb:.2f} MB")
            logger.debug(f"Opciones de procesamiento: {opciones}")

            # Subir imagen a Cloudinary
            upload_result = cloudinary.uploader.upload(
                temp_file_path,
                folder="anuncioproai",
                resource_type="image"
            )
            public_id = upload_result["public_id"]
            image_url = upload_result["secure_url"]
            logger.debug(f"Imagen subida a Cloudinary: {image_url}")

            # Construir transformaciones básicas
            transformations = [
                {"width": 256, "height": 256, "crop": "limit"},  # Reducido a la mitad para optimizar tamaño
                {"quality": "auto:good"},  # Optimización con buena calidad
                {"fetch_format": "webp"}  # Usar WebP para menor tamaño
            ]

            # Generar URL con transformaciones
            transformed_url = cloudinary.CloudinaryImage(public_id).build_url(
                transformation=transformations
            )
            logger.debug(f"URL de imagen transformada: {transformed_url}")
            st.write(f"URL de Cloudinary para depuración: {transformed_url}")

            # Descargar imagen procesada
            response = requests.get(transformed_url)
            logger.debug(f"Respuesta de Cloudinary - Código de estado: {response.status_code}")
            logger.debug(f"Respuesta de Cloudinary - Tipo de contenido: {response.headers.get('Content-Type')}")

            # Verificar que la respuesta sea válida
            if response.status_code != 200:
                st.error(f"Error al descargar la imagen de Cloudinary: Código de estado {response.status_code}")
                st.error(f"Detalles del error: {response.text}")
                logger.error(f"Contenido de la respuesta: {response.text}")
                # Guardar respuesta en archivo para inspección
                with open("cloudinary_error.txt", "w") as f:
                    f.write(f"URL: {transformed_url}\n\nError: {response.text}")
                st.write("El error de Cloudinary ha sido guardado en 'cloudinary_error.txt' para inspección.")
                return imagen_mejorada

            content_type = response.headers.get("Content-Type", "").lower()
            if not content_type.startswith("image/"):
                st.error(f"La respuesta de Cloudinary no es una imagen (Content-Type: {content_type})")
                st.error(f"Detalles del error: {response.text}")
                logger.error(f"Contenido de la respuesta: {response.text}")
                return imagen_mejorada

            # Intentar abrir la imagen
            try:
                imagen_procesada = Image.open(io.BytesIO(response.content))
                # Registrar tamaño de la imagen procesada
                buffered = io.BytesIO()
                imagen_procesada.save(buffered, format="WEBP", quality=80)
                processed_size_mb = len(buffered.getvalue()) / (1024 * 1024)
                logger.debug(f"Tamaño de la imagen procesada: {processed_size_mb:.2f} MB")
                st.write(f"Tamaño de la imagen procesada: {processed_size_mb:.2f} MB")
            except Exception as e:
                st.error(f"Error al abrir la imagen procesada: {str(e)}")
                logger.error(f"Contenido de la respuesta: {response.text}")
                return imagen_mejorada

            # Eliminar archivo temporal
            os.unlink(temp_file_path)

            # Eliminar imagen de Cloudinary para no acumular (opcional)
            # cloudinary.uploader.destroy(public_id)

            return imagen_procesada

        except Exception as e:
            st.error(f"Error al procesar la imagen con Cloudinary: {str(e)}")
            st.warning(f"{textos[lang]['error_imagen']}")
            if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
            return imagen_mejorada

    # Función para analizar imagen con IA
    def analizar_imagen(imagen):
        try:
            imagen_base64 = imagen_a_base64(imagen)
            response = client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Analiza esta imagen de una propiedad inmobiliaria y extrae información relevante que pueda no estar mencionada en los datos del formulario. Responde en formato JSON."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{imagen_base64}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=300
            )
            resultado_text = response.choices[0].message.content
            try:
                return json.loads(resultado_text)
            except json.JSONDecodeError:
                return {"error": "No se pudo parsear la respuesta como JSON", "resultado_bruto": resultado_text}
        except Exception as e:
            st.error(f"Error al analizar la imagen: {str(e)}")
            return None

    # Interfaz de usuario para imágenes
    st.subheader("📸 Añadir imágenes o planos del inmueble")

    # Opciones de procesamiento de imágenes
    st.write("Opciones de procesamiento de imágenes:")
    procesar_imagenes = st.checkbox("Procesar imágenes con IA", value=True)
    st.write("Selecciona qué mejoras aplicar a las imágenes:")
    col1_img, col2_img = st.columns(2)

    with col1_img:
        mejorar_iluminacion = st.checkbox("Mejorar iluminación", value=True)
        if mejorar_iluminacion:
            brillo = st.slider("Nivel de brillo", 0.8, 1.5, 1.1)
            contraste = st.slider("Nivel de contraste", 0.8, 1.5, 1.05)
        else:
            brillo = 1.0
            contraste = 1.0
        corregir_color = st.checkbox("Corregir balance de color", value=True)
        if corregir_color:
            saturacion = st.slider("Nivel de saturación", 0.8, 1.5, 1.1)
        else:
            saturacion = 1.0

    with col2_img:
        # Nuevas opciones de retoque fotográfico
        mejorar_nitidez = st.checkbox("Mejorar nitidez", value=True)
        if mejorar_nitidez:
            nivel_nitidez = st.slider("Nivel de nitidez", 0.5, 2.0, 1.2)
        else:
            nivel_nitidez = 1.0

        reducir_ruido = st.checkbox("Reducir ruido", value=False)
        if reducir_ruido:
            nivel_ruido = st.slider("Nivel de reducción de ruido", 0.5, 2.0, 1.0)
        else:
            nivel_ruido = 1.0

        ajustar_sombras = st.checkbox("Ajustar sombras", value=False)
        if ajustar_sombras:
            nivel_sombras = st.slider("Nivel de ajuste de sombras", 0.5, 1.5, 1.0)
        else:
            nivel_sombras = 1.0

        mejorar_detalles = st.checkbox("Mejorar detalles (enfoque fino)", value=False)

        ajustar_temperatura = st.checkbox("Ajustar temperatura de color", value=False)
        if ajustar_temperatura:
            temperatura = st.slider("Temperatura (frío a cálido)", -0.5, 0.5, 0.0)
        else:
            temperatura = 0.0

        recorte_automatico = st.checkbox("Recorte automático (enfocar espacio principal)", value=False)

        rotar_imagen = st.checkbox("Rotar imagen", value=False)
        if rotar_imagen:
            angulo_rotacion = st.slider("Ángulo de rotación (grados)", -180, 180, 0)
        else:
            angulo_rotacion = 0

        aplicar_filtro = st.selectbox("Aplicar filtro estilizado", ["Ninguno", "HDR", "Vintage", "Blanco y Negro"])

        analizar_caracteristicas = st.checkbox("Analizar características no mencionadas", value=True)

    # Subida de archivos
    uploaded_files = st.file_uploader("Sube fotos o planos", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    # Almacenar imágenes procesadas
    imagenes_procesadas = []

    # Mostrar y procesar las imágenes
    if uploaded_files:
        st.write("Imágenes cargadas:")
        for i, uploaded_file in enumerate(uploaded_files):
            if uploaded_file.type in ["image/jpeg", "image/png"]:
                col_orig, col_proc = st.columns(2)
                with col_orig:
                    st.write(f"Imagen original {i+1}:")
                    image = Image.open(uploaded_file)
                    st.image(image, caption=f"Original: {uploaded_file.name}", width=256)  # Reducido para visualización
                    # Mostrar tamaño de la imagen original
                    buffer = io.BytesIO()
                    image.save(buffer, format="JPEG", quality=80)
                    original_size_mb = len(buffer.getvalue()) / (1024 * 1024)
                    st.write(f"Tamaño original: {original_size_mb:.2f} MB")

                with col_proc:
                    if procesar_imagenes:
                        st.write("Imagen procesada con IA:")
                        opciones_proceso = {
                            "mejorar_iluminacion": mejorar_iluminacion,
                            "brillo": brillo,
                            "contraste": contraste,
                            "corregir_color": corregir_color,
                            "saturacion": saturacion,
                            "mejorar_nitidez": mejorar_nitidez,
                            "nivel_nitidez": nivel_nitidez,
                            "reducir_ruido": reducir_ruido,
                            "nivel_ruido": nivel_ruido,
                            "ajustar_sombras": ajustar_sombras,
                            "nivel_sombras": nivel_sombras,
                            "mejorar_detalles": mejorar_detalles,
                            "ajustar_temperatura": ajustar_temperatura,
                            "temperatura": temperatura,
                            "recorte_automatico": recorte_automatico,
                            "rotar_imagen": rotar_imagen,
                            "angulo_rotacion": angulo_rotacion,
                            "aplicar_filtro": aplicar_filtro
                        }
                        with st.spinner("Procesando imagen..."):
                            imagen_procesada = procesar_imagen_con_ia(image, opciones_proceso)
                        if imagen_procesada:
                            st.image(imagen_procesada, caption=f"Procesada: {uploaded_file.name}", width=256)  # Reducido para visualización
                            buffered = io.BytesIO()
                            imagen_procesada.save(buffered, format="WEBP", quality=80)
                            imagenes_procesadas.append((buffered.getvalue(), f"procesado_{uploaded_file.name.replace('.jpeg', '.webp').replace('.jpg', '.webp').replace('.png', '.webp')}"))
                            st.download_button(
                                label="Descargar imagen procesada",
                                data=buffered.getvalue(),
                                file_name=f"procesado_{uploaded_file.name.replace('.jpeg', '.webp').replace('.jpg', '.webp').replace('.png', '.webp')}",
                                mime="image/webp"
                            )

                    if analizar_caracteristicas:
                        with st.expander(f"Análisis de imagen {i+1}"):
                            with st.spinner("Analizando imagen..."):
                                resultado_analisis = analizar_imagen(image)
                            if resultado_analisis:
                                if "error" in resultado_analisis:
                                    st.write("Resultado del análisis (formato bruto):")
                                    st.write(resultado_analisis["resultado_bruto"])
                                else:
                                    st.write("Características detectadas en la imagen:")
                                    for clave, valor in resultado_analisis.items():
                                        if valor and clave != "error":
                                            st.write(f"**{clave.replace('_', ' ').title()}**: {valor}")
                                    st.write("¿Quieres incluir esta información en el anuncio?")
                                    incluir_info = st.checkbox(f"Incluir información de la imagen {i+1} en el anuncio", key=f"incluir_info_{i}")
                                    if incluir_info:
                                        info_para_anuncio = "\n".join([f"{k.replace('_', ' ').title()}: {v}" for k, v in resultado_analisis.items() if v and k != "error"])
                                        st.session_state.informacion_adicional += f"\nInformación detectada en imagen {i+1}:\n{info_para_anuncio}\n"
                                st.write(f"Archivo {uploaded_file.name} cargado correctamente.")

        # Botón para descargar todas las imágenes procesadas
        if imagenes_procesadas:
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                for img_data, img_name in imagenes_procesadas:
                    zip_file.writestr(img_name, img_data)
            zip_buffer.seek(0)
            st.download_button(
                label="Descargar todas las imágenes procesadas",
                data=zip_buffer,
                file_name="imagenes_procesadas.zip",
                mime="application/zip"
            )

    # Destino del anuncio
    st.subheader("📣 Selecciona el destino del anuncio")
    destino = st.radio(
        "¿Dónde quieres publicar el anuncio?",
        ("Portales inmobiliarios (Idealista, Fotocasa, Milanuncios)", "Redes sociales (Facebook, Instagram)")
    )

    # Actualizar la función de generación de anuncio
   
    def generar_anuncio(datos):
        if hasattr(st.session_state, 'informacion_adicional') and st.session_state.informacion_adicional:
            if "informacion_adicional" in datos:
                datos["informacion_adicional"] += "\n" + st.session_state.informacion_adicional
            else:
                datos["informacion_adicional"] = st.session_state.informacion_adicional

        prompt = f"""
        Eres un experto en marketing inmobiliario internacional, especializado en crear anuncios profesionales y persuasivos para la venta o alquiler de propiedades en distintos países y plataformas.

        Tu objetivo es generar un anuncio de alto impacto, optimizado para:

        1. **Portales inmobiliarios** como Idealista, Fotocasa, Milanuncios, Zillow, Immowelt, SeLoger, Rightmove…
        2. **Redes sociales** como Instagram, Facebook, TikTok o LinkedIn.

        El anuncio debe:

        - Ser atractivo, claro, natural y persuasivo.
        - Destacar los beneficios y el estilo de vida que ofrece la propiedad.
        - Adaptarse al canal:
          - Si el destino es "portales inmobiliarios", escribe con estilo profesional y estructurado, orientado a SEO y con llamadas a la acción claras. La Longitud maxima del anuncio tiene que ser de 850 caracteres contando los espacios entre palabras, sin hastags.
          - Si el destino es "redes sociales", usa un estilo más directo, emocional, con emojis (donde encajen), y termina el anuncio con hashtags relevantes según el país o ciudad, y no incluyas informacion despues de los hastags. La Longitud maxima del anuncio tiene que ser de 600 caracteres contando los espacios entre palabras.

        Utiliza la información facilitada para redactar el texto sin repetir datos de forma robótica. No enumeres todo como una lista. Transforma los datos en frases que comuniquen valor real.

        📝 DATOS DISPONIBLES:

        🏷 Tipo de operación: {datos['tipo_operacion']}  
        🏡 Tipo de propiedad: {datos['tipo']}  
        📍 Ubicación: {datos['ubicacion']}  
        📐 Superficie: {datos['m2']} m² construidos, {datos['m2_utiles']} m² útiles, {datos['m2_terreno']} m² de terreno  
        🛏 Habitaciones: {datos['habitaciones']} | 🛁 Baños: {datos['baños']}  
        🌞 Fachada: {datos['fachada']} | Orientación: {datos['orientacion']}  
        📈 Estado: {datos['estado']} | Certificado energético: {datos['certificado']}  
        🏗 Suelo interior: {datos['suelo_interior']} | Suelo exterior: {datos['suelo_exterior']}  
        ✨ Extras vivienda: {', '.join(datos['extras_vivienda']) if datos['extras_vivienda'] else 'Ninguno'}  
        🏢 Extras edificio: {', '.join(datos['extras_edificio']) if datos['extras_edificio'] else 'Ninguno'}  
        📸 Terraza: {datos['metros_terraza']} m² | Balcón: {datos['metros_balcon']} m² | Trastero: {datos['metros_trastero']} m² | Garaje: {datos['metros_garaje']} m²  
        🗺 Servicios cercanos: {datos['descripcion_servicios']}  
        🌊/🏞 Otros (vistas, entorno, etc.): {datos['descripcion_cercania']}  
        💶 Precio: {datos['precio']} € | Gastos comunidad: {datos['gastos']} €  
        ⚠ Situación (ocupado, libre, alquilado, etc.): {datos['situacion']}  
        📝 Información adicional: {datos['informacion_adicional']}  
        📣 Destino del anuncio: {datos['destino']}  

        🎯 Recuerda: escribe como si fueras un copywriter de alto nivel. Seduce, informa y convence.
        El anuncio tiene que estar bien estructurado en parrafos y sin errores ortográficos y gramaticales, el formato ideal depende 
        del destino seleccionado, si es para portales inmobiliarios o redes sociales.
        No superes bajo ningun concepto el numero de caracteres maximo indicados cuando generes el anuncio.
        """

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        return response.choices[0].message.content

# Botón para generar el anuncio

# st.subheader("🧠 Generador de anuncio con IA")
import streamlit as st

if st.button("✨ Generar anuncio optimizado"):
    datos = recopilar_datos(destino)
    anuncio = generar_anuncio(datos)
    st.success("✅ Anuncio generado con éxito:")
    st.markdown("📝 **Anuncio generado**")
    st.markdown(anuncio)

    # Botón para descargar anuncio
    st.download_button(
        label="📥 Descargar anuncio",
        data=anuncio,
        file_name="anuncio_inmobiliario.txt",
        mime="text/plain"
    )

    # Text area oculta para poder copiar
    st.text_area("Anuncio para copiar", value=anuncio, height=200, key="anuncio_text_area")

    # Botón para copiar el texto al portapapeles
    if st.button("📋 Copiar anuncio"):
        # Esto solo muestra mensaje, la copia real debe hacerse manualmente (Ctrl+C)
        st.success("¡Texto copiado! Usa Ctrl+C para copiar el anuncio desde el cuadro de texto.")

  
# Planes
elif menu == textos[lang]["nav"][2]:
    st.header(textos[lang]["planes_titulo"])
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("🎁 Gratis")
        st.write("- Hasta 5 anuncios/mes")
        st.write("- 1 idioma")
        st.write("- Soporte básico")
        st.write("💸 Gratis primeros 5 anuncios")
    with col2:
        st.subheader("💼 Profesional")
        st.write("- Hasta 50 anuncios/mes")
        st.write("- Hasta 3 idiomas")
        st.write("- Soporte prioritario")
        st.write("💳 14,90 €/mes")
    with col3:
        st.subheader("🏢 Agencia")
        st.write("- Anuncios ilimitados")
        st.write("- Hasta 5 idiomas")
        st.write("- IA personalizada")
        st.write("📞 Contactar")
        
# Contacto

# Cargar variables de entorno
SENDGRID_FROM_EMAIL = st.secrets["sendgrid"]["from_email"]
SENDGRID_API_KEY = st.secrets["sendgrid"]["api_key"]

def send_email(nombre, correo, mensaje, to_email="luis.cara@hotmail.com"):
    if not SENDGRID_FROM_EMAIL or not SENDGRID_API_KEY:
        st.error("No se han definido correctamente las variables de entorno SENDGRID_FROM_EMAIL o SENDGRID_API_KEY.")
        return False

    # Crear el mensaje de correo con Email() (formato correcto)
    message = Mail(
        from_email=Email(SENDGRID_FROM_EMAIL, name="Luis"),
        to_emails=to_email,
        subject=f"Nuevo mensaje de contacto de {nombre}",
        plain_text_content=f"Nombre: {nombre}\nCorreo: {correo}\nMensaje:\n{mensaje}"
    )
    
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        if response.status_code == 202:
            return True
        else:
            st.error(f"Error al enviar el correo: Código {response.status_code}")
            return False
    except Exception as e:
        st.error(f"Error al enviar el correo: {str(e)}")
        return False

def contacto_page(lang, textos):
    st.header(textos[lang]["contacto_titulo"])
    st.markdown(textos[lang]["contacto_desc"])

    # Formulario de contacto
    nombre = st.text_input(textos[lang]["nombre"])
    correo = st.text_input(textos[lang]["correo"])
    mensaje = st.text_area(textos[lang]["mensaje"])

    if st.button(textos[lang]["enviar"]):
        if nombre and correo and mensaje:
            if send_email(nombre, correo, mensaje):
                st.success(textos[lang].get("exito", "¡Mensaje enviado con éxito!"))
            else:
                st.error(textos[lang].get("error", "No se pudo enviar el mensaje. Por favor, intenta de nuevo."))
        else:
            st.warning(textos[lang].get("advertencia", "Por favor, completa todos los campos."))

# Mostrar la página de contacto
if menu == textos[lang]["nav"][3]:
    contacto_page(lang, textos)

