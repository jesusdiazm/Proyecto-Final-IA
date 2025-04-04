from flask import Blueprint, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde venv/.env
load_dotenv(dotenv_path="venv/.env")

# Configurar la clave API de OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Crear el blueprint
main = Blueprint('main', __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/continuar", methods=["POST"])
def continuar_historia():
    opcion = request.json.get("opcion")
    historia = generar_historia(opcion)
    imagen = generar_imagen(historia)
    return jsonify({"historia": historia, "imagen_url": imagen})

# Función para generar la historia
def generar_historia(opcion):
    prompt = f"La historia continúa con la elección: {opcion}. ¿Qué sucede después?"
    respuesta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Modelo más reciente para interacción conversacional
        messages=[
            {"role": "system", "content": "Eres un generador de historias interactivas."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )
    # Extraer la respuesta generada
    return respuesta["choices"][0]["message"]["content"].strip()


# Función para generar imágenes

def generar_imagen(descripcion):
    # Generar una imagen basada en la descripción
    respuesta = openai.Image.create(
        prompt=descripcion,
        n=1,  # Número de imágenes a generar
        size="512x512"  # Tamaño de la imagen: 256x256, 512x512 o 1024x1024
    )
    return respuesta['data'][0]['url']  # Retorna el URL de la imagen generada
