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
    respuesta = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return respuesta.choices[0].text.strip()

# Función para generar imágenes
def generar_imagen(descripcion):
    respuesta = openai.Image.create(
        prompt=descripcion,
        n=1,
        size="512x512"
    )
    return respuesta['data'][0]['url']
