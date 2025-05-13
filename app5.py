import streamlit as st
import io
import base64
from PIL import Image
import openai
import json
import requests
import streamlit as st
from PIL import ImageEnhance
import os 
from openai import OpenAI


# Elimina la variable de entorno antes de que httpx la use
os.environ.pop("SSL_CERT_FILE", None)

# Inicializa el nuevo cliente
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



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
        "enviar": "Enviar"
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
        "enviar": "Send"
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
        "enviar": "Envoyer"
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
        "enviar": "Invia"
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
        "enviar": "Senden"
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

    # Tipo de operación
    st.subheader("⚙️ Tipo de operación")
    tipo_operacion = st.selectbox("¿Se trata de una venta o alquiler?", ["Venta", "Alquiler","Alquiler vacacional", "Alquiler con opción a compra"])

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
        "Gres","Parquet", "Tarima flotante", "Baldosa cerámica", "Mármol", "Granito", "Vinílico", "Moqueta", "Cemento pulido", "Laminado", "Corcho"
    ])
    suelo_exterior = st.selectbox("Tipo de suelo en el exterior", [
        "Ninguno", "Grava", "Pavimento de adoquín", "Hormigón", "Terracota", "Decking de madera", "Piedra natural", "Césped artificial", "Pavimento permeable"
    ])

    # Características adicionales
    st.subheader("✨ Extras")
    extras_vivienda = st.multiselect("Características de la vivienda", [
        "Semiamueblado","Amueblado", "Armarios empotrados", "Aire acondicionado", "Terraza", "Balcón","Lavadero","Chimenea", "Trastero", "Plaza de garaje"])
    extras_edificio = st.multiselect("Características del edificio", ["Piscina", "Zona verde", "Gimnasio", "Portero", "Acceso adaptado", "Ascensor", "Zonas comunes","zona infantil", "Pista de tenis","Pista de pádel", "Sauna", "Jacuzzi"])

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
    if 'servicios_cercanos' in locals() and servicios_cercanos:
        descripcion_servicios += ", ".join(servicios_cercanos)
    else:
        descripcion_servicios = "No se han seleccionado servicios cercanos."

    descripcion_cercania = ""
    if cerca_playa:
        descripcion_cercania = f"Está a {distancia_playa} metros de la playa."
    elif cerca_montana:
        descripcion_cercania = f"Está a {distancia_montana} metros de la montaña."

    st.write(f"🔑 **Dirección**: {ubicacion if 'ubicacion' in locals() else 'No se ha proporcionado una dirección.'}")
    st.write(f"🏙 **Servicios cercanos**: {descripcion_servicios}")
    if descripcion_cercania:
        st.write(f"🌊/🏞 **Cercanía**: {descripcion_cercania}")

    # Precio y situación legal
    st.subheader("💶 Precio y situación")
    precio = st.number_input("Precio del inmueble (€)", min_value=0)
    gastos = st.number_input("Gastos de comunidad (€ / mes)", min_value=0)
    situacion = st.selectbox("¿Situación excepcional?", [
        "No, en ninguna situación excepcional", "Ocupada ilegalmente", "Alquilada, con inquilinos", "Nuda propiedad"])

    # Información adicional
    st.subheader("📝 Información adicional")
    informacion_adicional = st.text_area("¿Hay algo más que quieras añadir sobre la propiedad?")
    if informacion_adicional:
        st.write("Información adicional:", informacion_adicional)

    # esta función recopila todos los datos introducidos en el formulario y los devuelve como un diccionario
    def recopilar_datos():
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
            "descripcion_cercania": descripcion_cercania if 'descripcion_cercania' in locals() else "",
            "precio": precio,
            "gastos": gastos,
            "situacion": situacion,
            "informacion_adicional": informacion_adicional if informacion_adicional else "",
            "destino": destino if 'destino' in locals() else "",
        }
        return datos

    # Función para convertir imagen a base64
    def imagen_a_base64(imagen):
        buffered = io.BytesIO()
        imagen.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return img_str

    # Función para aplicar mejoras simples con PIL (brillo, color, etc.)
    def aplicar_mejoras_pil(imagen, opciones):
        # Copia la imagen para no modificar la original
        img = imagen.convert("RGB")
        
        if opciones["mejorar_iluminacion"]:
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(1.2)  # Aumenta el brillo

        if opciones["corregir_color"]:
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1.3)  # Aumenta la saturación
        
        # Puedes añadir más mejoras aquí según las opciones
        return img

    # Función para procesar imagen con IA
    def procesar_imagen_con_ia(imagen, opciones):
        try:
            # Primero aplica mejoras locales con PIL según las opciones
            imagen_mejorada = aplicar_mejoras_pil(imagen, opciones)
            
            # Convertimos la imagen mejorada a base64
            imagen_base64 = imagen_a_base64(imagen_mejorada)
            
            instrucciones = "Analiza esta imagen de una propiedad inmobiliaria y "
            if opciones["agregar_muebles"]:
                instrucciones += "añade muebles en espacios vacíos con un estilo moderno y acogedor. "
            if opciones["mejorar_iluminacion"]:
                instrucciones += "mejora la iluminación para hacerla más atractiva. "
            if opciones["corregir_color"]:
                instrucciones += "corrige el balance de color para que sea más natural. "
            if opciones["eliminar_objetos"]:
                instrucciones += "elimina objetos innecesarios o desordenados. "
            if opciones["virtualstaging"]:
                instrucciones += "realiza un virtual staging completo con decoración moderna y atractiva. "
            
            # Aquí puedes enviar la imagen a la IA si deseas que aplique análisis o mejoras adicionales, pero no para inventarla.
            response = openai.Image.create(
                model="dall-e-3",
                prompt=instrucciones,
                n=1,
                size="1024x1024",
                quality="standard",
            )
            imagen_url = response.data[0]['url']
            
            # Obtener la URL de la imagen procesada por IA y devolverla
            imagen_url = response['data'][0]['url']
            respuesta = requests.get(imagen_url)
            imagen_procesada = Image.open(io.BytesIO(respuesta.content))
            return imagen_procesada
        except Exception as e:
            st.error(f"Error al procesar la imagen: {str(e)}")
            return None

    # Función para analizar imagen con IA (si es necesario para extraer información adicional)
    def analizar_imagen(imagen):
        try:
            imagen_base64 = imagen_a_base64(imagen)
            response = openai.Completion.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": "Analiza esta imagen de una propiedad inmobiliaria y extrae información relevante que pueda no estar mencionada en los datos del formulario. Responde en formato JSON."
                    },
                    {
                        "role": "user",
                        "content": f"data:image/jpeg;base64,{imagen_base64}"
                    }
                ]
            )
            resultado_text = response.choices[0].message['content']
            return json.loads(resultado_text)
        except Exception as e:
            st.error(f"Error al analizar la imagen: {str(e)}")
            return None

    # Interfaz de usuario
    st.subheader("📸 Añadir imágenes o planos del inmueble")

    # Opciones de procesamiento de imágenes
    st.write("Opciones de procesamiento de imágenes:")
    procesar_imagenes = st.checkbox("Procesar imágenes con IA", value=True)
    st.write("Selecciona qué mejoras aplicar a las imágenes:")
    col1_img, col2_img = st.columns(2)

    with col1_img:
        agregar_muebles = st.checkbox("Agregar muebles en espacios vacíos", value=True)
        mejorar_iluminacion = st.checkbox("Mejorar iluminación", value=True)
        corregir_color = st.checkbox("Corregir balance de color", value=True)

    with col2_img:
        eliminar_objetos = st.checkbox("Eliminar objetos innecesarios", value=False)
        virtualstaging = st.checkbox("Virtual staging (decoración completa)", value=False)
        analizar_caracteristicas = st.checkbox("Analizar características no mencionadas", value=True)

    # Subida de archivos
    uploaded_files = st.file_uploader("Sube fotos o planos", type=["jpg", "jpeg", "png", "pdf"], accept_multiple_files=True)

    # Mostrar y procesar las imágenes
    if uploaded_files:
        st.write("Imágenes cargadas:")
        for i, uploaded_file in enumerate(uploaded_files):
            if uploaded_file.type in ["image/jpeg", "image/png"]:
                col_orig, col_proc = st.columns(2)
                with col_orig:
                    st.write(f"Imagen original {i+1}:")
                    image = Image.open(uploaded_file)
                    st.image(image, caption=f"Original: {uploaded_file.name}", use_container_width=True)

                with col_proc:
                    if procesar_imagenes:
                        st.write("Imagen procesada con IA:")
                        opciones_proceso = {
                            "agregar_muebles": agregar_muebles,
                            "mejorar_iluminacion": mejorar_iluminacion,
                            "corregir_color": corregir_color,
                            "eliminar_objetos": eliminar_objetos,
                            "virtualstaging": virtualstaging
                        }
                        with st.spinner("Procesando imagen..."):
                            imagen_procesada = procesar_imagen_con_ia(image, opciones_proceso)
                        if imagen_procesada:
                            st.image(imagen_procesada, caption=f"Procesada: {uploaded_file.name}", use_container_width=True)
                            buffered = io.BytesIO()
                            imagen_procesada.save(buffered, format="JPEG")
                            st.download_button(
                                label="Descargar imagen procesada",
                                data=buffered.getvalue(),
                                file_name=f"procesado_{uploaded_file.name}",
                                mime="image/jpeg"
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
                                        if "informacion_adicional" not in st.session_state:
                                            st.session_state.informacion_adicional = ""
                                        info_para_anuncio = "\n".join([f"{k.replace('_', ' ').title()}: {v}" for k, v in resultado_analisis.items() if v and k != "error"])
                                        st.session_state.informacion_adicional += f"\nInformación detectada en imagen {i+1}:\n{info_para_anuncio}\n"
                                st.write(f"Archivo {uploaded_file.name} cargado correctamente.")

    # Destino del anuncio
    st.subheader("📣 Selecciona el destino del anuncio")
    destino = st.radio(
        "¿Dónde quieres publicar el anuncio?",
        ("Portales inmobiliarios (Idealista, Fotocasa, Milanuncios)", "Redes sociales (Facebook, Instagram)")
    )

    # Actualizar la función de generación de anuncio para que incluya la información de las imágenes
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
          - Si el destino es "portales inmobiliarios", escribe con estilo profesional y estructurado, orientado a SEO y con llamadas a la acción claras.
          - Si el destino es "redes sociales", usa un estilo más directo, emocional, con emojis (donde encajen), y termina con hashtags relevantes según el país o ciudad.

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
        Incluye una mención a las imágenes mejoradas con IA si estas se han proporcionado, destacando los aspectos visuales del inmueble.
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
    st.subheader("🧠 Generador de anuncio con IA")
    if st.button("✨ Generar anuncio optimizado"):
        datos = recopilar_datos()
        anuncio = generar_anuncio(datos)
        st.success("✅ Anuncio generado con éxito:")
        st.text_area("📝 Anuncio generado", value=anuncio, height=300)

# Planes
elif menu == textos[lang]["nav"][2]:
    st.header(textos[lang]["planes_titulo"])
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("🎁 Gratis")
        st.write("- Hasta 5 anuncios/mes")
        st.write("- 1 idioma")
        st.write("- Soporte básico")
        st.write("💸 0 €/mes")
    with col2:
        st.subheader("💼 Profesional")
        st.write("- Hasta 50 anuncios/mes")
        st.write("- Hasta 3 idiomas")
        st.write("- Soporte prioritario")
        st.write("💳 14,90 €/mes")
    with col3:
        st.subheader("🏢 Agencia")
        st.write("- Anuncios ilimitados")
        st.write("- Hasta 10 idiomas")
        st.write("- IA personalizada")
        st.write("📞 Contactar")

# Contacto
elif menu == textos[lang]["nav"][3]:
    st.header(textos[lang]["contacto_titulo"])
    st.markdown(textos[lang]["contacto_desc"])
    st.text_input(textos[lang]["nombre"])
    st.text_input(textos[lang]["correo"])
    st.text_area(textos[lang]["mensaje"])
    st.button(textos[lang]["enviar"])

