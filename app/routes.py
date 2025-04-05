from flask import Blueprint, render_template, request, jsonify
import openai

main = Blueprint('main', __name__)

# Cargar clave de API desde el entorno
openai.api_key = 'OPENAI_API_KEY'

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/generar_historia", methods=["POST"])
@main.route("/generar_historia", methods=["POST"])
def generar_historia():
    data = request.json
    prompt = data.get("prompt", "Cuéntame una historia interesante.")

    # Generar la primera parte de la historia
    respuesta_historia = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Modelo actualizado
        messages=[
            {"role": "system", "content": "Eres un narrador de historias interactivas."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )
    historia = respuesta_historia["choices"][0]["message"]["content"].strip()

    # Generar una imagen relacionada con la historia
    respuesta_imagen = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512"
    )
    url_imagen = respuesta_imagen["data"][0]["url"]

    # Proveer opciones de continuación
    opciones = [
        "Explorar un camino misterioso",
        "Entrar en la casa embrujada"
    ]

    return jsonify({"historia": historia, "imagen": url_imagen, "opciones": opciones})
