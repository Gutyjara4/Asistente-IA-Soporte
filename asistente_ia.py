import spacy
from flask import Flask, request, jsonify

# 1. CARGA DEL MODELO 
# Usamos el modelo grande de español para mejor comprensión semántica
nlp = spacy.load("es_core_news_lg")

app = Flask(__name__)

# 2. BASE DE CONOCIMIENTOS 
# Diccionario con problemas comunes y soluciones técnicas
faq_support = {
    "internet": "Verifica que el router tenga las luces verdes y reinicia el equipo.",
    "password": "Para restablecer su contraseña, acceda al portal de IT y use su DNI.",
    "impresora": "Asegúrese de que el cable USB esté conectado o que esté en la red Wi-Fi 'Office'.",
    "lentitud": "Cierre las aplicaciones en segundo plano y limpie la memoria caché."
}

# 3. PROCESAMIENTO DE LENGUAJE 
def procesar_consulta(texto_usuario):
    # Tokenización y limpieza (eliminamos palabras vacías y puntuación)
    doc = nlp(texto_usuario.lower())
    tokens_limpios = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    
    # Buscamos coincidencia entre las palabras clave y nuestra base de datos
    for palabra in tokens_limpios:
        if palabra in faq_support:
            return faq_support[palabra]
    
    return "Lo siento, no he identificado el problema. ¿Puede darme más detalles?"

# 4. DESPLIEGUE DE API 
@app.route('/chat', methods=['POST'])
def chat():
    datos = request.json
    consulta = datos.get("pregunta", "")
    respuesta = procesar_consulta(consulta)
    return jsonify({"respuesta": respuesta})

if __name__ == '__main__':
    print("Asistente técnico iniciado...")
    app.run(port=5000)