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
        return jsonify({"error": "OpenAI no configurado"}), 503

    data = request.json
    prompt = data.get("prompt", "")
    accion = data.get("accion", "inicio")  # 'inicio', 'continuar', 'escenario', 'giro'
    historia_actual = data.get("historia_actual", "")

    try:
        # Definimos instrucciones específicas para cada acción
        instrucciones = {
            "inicio": f"Eres un narrador creativo. Comienza una historia sobre: {prompt}",
            "continuar": f"Continúa esta historia de manera coherente sin perder el hilo:\n{historia_actual}, recuerda, debes continuar la historia donde te quedaste. la primera parte generada debe terninar en un '.'",
            "escenario": f"Manteniendo los personajes, cambia completamente el escenario de esta historia:\n{historia_actual}",
            "giro": f"Añade un giro inesperado a esta historia:\n{historia_actual}"
        }

        # Generamos la historia
        respuesta = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": instrucciones[accion]},
                {"role": "user", "content": "Genera aproximadamente 200 palabras"}
            ],
            max_tokens=150,
            temperature=0.7 if accion in ["inicio", "continuar"] else 0.9
        )
        historia = respuesta.choices[0].message.content.strip()

        # Generamos imagen (versión simplificada)
        try:
            estilo = "dibujo animado" if accion != "giro" else "arte dramático"
            respuesta_imagen = client.images.generate(
                model="dall-e-2",
                prompt=f"{estilo} para: {historia[:200]}", 
                n=1,
                size="512x512"
            )
            url_imagen = respuesta_imagen.data[0].url
        except Exception as e:
            print(f"Error generando imagen: {e}")
            url_imagen = "https://via.placeholder.com/512"

        return jsonify({
            "historia": historia,
            "imagen": url_imagen,
            "opciones": [
                "Continuar la historia",
                "Cambiar el escenario",
                "Hacer un giro inesperado"
            ]
        })

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500
        
        
@main.route("/historial", methods=["GET"])
def obtener_historial():
    return jsonify(historial=[])  # Base para implementar persistencia en backend


#Codigo corregid para poder reproducir accion.mp3
@main.route("/detectar_genero", methods=["POST"])
def detectar_genero():
    data = request.json
    historia = data.get("historia", "")
    
    try:
        respuesta = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """Clasifica el género de esta historia (solo responde una palabra): 
                suspenso, aventura, terror, amor, accion, acción. Ejemplo: 'accion'"""},  # <-- Añadí "acción"
                {"role": "user", "content": historia[:1000]}
            ],
            max_tokens=10,
            temperature=0.3
        )
        genero = respuesta.choices[0].message.content.lower()
        # Normaliza a "accion" sin tilde si es necesario
        return jsonify({"genero": "accion" if "acción" in genero else genero})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500