from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# Configura tu clave de API
openai.api_key = 'tu_clave_secreta'

@app.route('/generar_historia', methods=['POST'])
def generar_historia():
    # Obtener el prompt principal y las opciones del cliente
    data = request.get_json()
    prompt = data.get('prompt', '')
    
    # Generar la primera parte de la historia
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    historia = response.choices[0].text.strip()
    
    # Presentar opciones para continuar la historia
    opciones = [f"Continúa la historia con opción {i+1}" for i in range(2)]
    
    return jsonify({"historia": historia, "opciones": opciones})

@app.route('/generar_imagen', methods=['POST'])
def generar_imagen():
    # Obtener la opción seleccionada para continuar la historia
    data = request.get_json()
    opcion = data.get('opcion', '')
    
    # Generar la continuación de la historia y una imagen relacionada
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=opcion,
        max_tokens=150
    )
    historia = response.choices[0].text.strip()
    
    # Aquí podrías generar una imagen usando las funcionalidades de OpenAI si quieres
    # Por simplificar, retornaremos solo la historia
    return jsonify({"historia": historia})

if __name__ == '__main__':
    app.run(debug=True)
