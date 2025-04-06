from flask import Blueprint, render_template, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

main = Blueprint('main', __name__)

# Configuración segura del cliente OpenAI
try:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    if not client.api_key:
        raise ValueError("La clave API de OpenAI no está configurada correctamente")
except Exception as e:
    print(f"Error al configurar OpenAI: {str(e)}")
    client = None

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/generar_historia", methods=["POST"])
def generar_historia():
    if not client:
        return jsonify({
            "error": "OpenAI no configurado",
            "message": "El servicio no está disponible temporalmente"
        }), 503

    data = request.json
    prompt = data.get("prompt", "Cuéntame una historia interesante.")
    
    try:
        # 1. Generar historia
        respuesta_historia = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Cambiado a modelo más accesible para pruebas
            messages=[
                {"role": "system", "content": "Eres un narrador de historias interactivas. Genera historias cortas de aproximadamente 100 palabras."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.7
        )
        historia = respuesta_historia.choices[0].message.content.strip()

        # 2. Generar imagen (versión simplificada para pruebas)
        try:
            respuesta_imagen = client.images.generate(
                model="dall-e-2",  # Más accesible que dall-e-3
                prompt=f"Imagen para: {historia[:200]}",
                n=1,
                size="512x512"
            )
            url_imagen = respuesta_imagen.data[0].url
        except Exception as img_error:
            print(f"Error generando imagen: {img_error}")
            url_imagen = "https://via.placeholder.com/512"

        # 3. Opciones de continuación (versión simplificada)
        opciones = [
            "Continuar explorando",
            "Tomar un atajo misterioso"
        ]

        return jsonify({
            "historia": historia,
            "imagen": url_imagen,
            "opciones": opciones
        })

    except Exception as e:
        print(f"Error en generación: {str(e)}")
        return jsonify({
            "error": str(e),
            "message": "Error al generar la historia. Intenta con un prompt diferente."
        }), 500
        
        
@main.route("/historial", methods=["GET"])
def obtener_historial():
    return jsonify(historial=[])  # Base para implementar persistencia en backend