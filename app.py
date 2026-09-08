import base64
import glob
import os
import time
from gTTS import gTTS
from PIL import Image
import streamlit as st

# Configuración básica de página
st.set_page_config(
    page_title="Entrenador de Lectura y Pronunciación", layout="wide"
)

# Crear directorio temporal si no existe
os.makedirs("temp", exist_ok=True)


# Función para limpiar archivos antiguos de la carpeta temporal
def remove_old_files(days=1):
  now = time.time()
  cutoff = days * 86400
  for f in glob.glob("temp/*.mp3"):
    if os.stat(f).st_mtime < now - cutoff:
      try:
        os.remove(f)
      except OSError:
        pass


remove_old_files(1)


# Función para convertir texto a audio de manera segura
def generate_audio(text_content, lang_code):
  # Asignar nombre seguro al archivo
  safe_name = "".join(
      c for c in text_content[:15] if c.isalnum() or c in (" ", "_")
  ).rstrip()
  if not safe_name:
    safe_name = "audio_generado"

  file_path = f"temp/{safe_name}_{int(time.time())}.mp3"
  tts = gTTS(text=text_content, lang=lang_code, slow=False)
  tts.save(file_path)
  return file_path


# ------------------- INTERFAZ -------------------

st.title("🎧 Entrenador de Pronunciación y Lectura")
st.caption(
    "Herramienta interactiva para practicar la comprensión auditiva y"
    " pronunciación."
)

# Imagen de cabecera
try:
  image = Image.open("gato_raton.png")
  st.image(image, width=320, caption="Lectura interactiva: El gato y el ratón")
except FileNotFoundError:
  st.warning("Asegúrate de tener la imagen 'gato_raton.png' en el directorio.")

# Barra lateral de configuración
with st.sidebar:
  st.header("⚙️ Ajustes de Voz")
  idioma = st.selectbox(
      "Selecciona el idioma de lectura:",
      options=["Español", "English", "Español (Lento)", "English (Slow)"],
  )

  # Mapeo de idioma y velocidad
  if "Español" in idioma:
    lang_code = "es"
  else:
    lang_code = "en"

# Texto de lectura / lectura sugerida
st.subheader("📚 Texto de Práctica")

fabula_es = (
    "¡Ay! -dijo el ratón-. El mundo se hace cada día más pequeño. Al principio"
    " era tan grande que le tenía miedo. Corría y corría y por cierto que me"
    " alegraba ver esos muros, a diestra y siniestra, en la distancia. Pero"
    " esas paredes se estrechan tan rápido que me encuentro en el último"
    " cuarto y ahí en el rincón está la trampa sobre la cual debo pasar. Todo"
    " lo que debes hacer es cambiar de rumbo dijo el gato... y se lo comió."
    " — Franz Kafka."
)

st.info(fabula_es)

# Área de texto interactiva
st.subheader("✍️ Tu Zona de Ensayo")
texto_usuario = st.text_area(
    "Copia el texto de arriba o escribe la frase que quieras practicar:",
    value=fabula_es,
    height=140,
)

# Botón de conversión a audio
if st.button("🔊 Generar y Escuchar Audio"):
  if texto_usuario.strip():
    with st.spinner("Generando audio..."):
      path_audio = generate_audio(texto_usuario, lang_code)

      # Reproducir audio
      with open(path_audio, "rb") as f:
        audio_data = f.read()

      st.success("¡Audio generado con éxito!")
      st.audio(audio_data, format="audio/mp3")

      # Botón de descarga
      b64 = base64.b64encode(audio_data).decode()
      href = f'<a href="data:file/mp3;base64,{b64}" download="practica_pronunciacion.mp3" style="text-decoration:none;"><button style="padding: 8px 16px; background-color: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer;">📥 Descargar MP3</button></a>'
      st.markdown(href, unsafe_allow_html=True)
  else:
    st.error("Por favor ingresa algún texto para generar el audio.")
    print("Deleted ", f)


remove_files(7)
