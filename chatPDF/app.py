import os
import hashlib
import base64
from pathlib import Path
import fitz
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from langchain.chains import RetrievalQA
from pinecone import Pinecone, ServerlessSpec

from langchain.callbacks import get_openai_callback

from flask import Flask, request, jsonify
from flask_cors import CORS

# === Configuración inicial ===
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Configuración de Pinecone
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "asistente"
AI_MODEL = "gemini-2.5-flash"

# Inicializar Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
if INDEX_NAME not in [idx["name"] for idx in pc.list_indexes()]:
    pc.create_index(
        name=INDEX_NAME,
        dimension=768,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

# Inicializar modelo y embeddings
llm = ChatGoogleGenerativeAI(model=AI_MODEL, convert_system_message_to_human=True)
embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vectorstore = PineconeVectorStore(index_name=INDEX_NAME, embedding=embedding)

# === Funciones utilitarias ===
def hash_archivo(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()

def ya_existente(file_hash: str) -> bool:
    if not Path("hashes.txt").exists():
        return False
    return file_hash in Path("hashes.txt").read_text().splitlines()

def guardar_hash(file_hash: str):
    with open("hashes.txt", "a") as f:
        f.write(file_hash + "\n")

def leer_pdf_bytes(content: bytes) -> str:
    try:
        texto = ""
        with fitz.open(stream=content, filetype="pdf") as doc:
            for page in doc:
                texto += page.get_text()
        return texto
    except Exception as e:
        raise Exception(f"Error al leer PDF: {str(e)}")

def fragmentar(texto: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,      # Cambiado a 1500
        chunk_overlap=400,    # Cambiado a 400
        length_function=len
    )
    return splitter.create_documents([texto])

def vectorizar_documento(texto: str):
    try:
        docs = fragmentar(texto)
        PineconeVectorStore.from_documents(
            docs,
            index_name=INDEX_NAME,
            embedding=embedding
        )
    except Exception as e:
        raise Exception(f"Error al vectorizar documento: {str(e)}")

def crear_chain_qa():
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )

# Función cifrado César +3 (igual que antes)
def cifrado_cesar(texto: str, desplazamiento: int = 3) -> str:
    resultado = ""
    for char in texto:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            resultado += chr((ord(char) - base + desplazamiento) % 26 + base)
        else:
            resultado += char
    return resultado

# Inicializar Flask
app = Flask(__name__)
CORS(app, resources={
    r"/upload": {"origins": "*"},
    r"/ask": {"origins": "*"}
})
qa_chain = crear_chain_qa()

@app.route('/upload', methods=['POST'])
def upload_pdf():
    try:
        if request.content_type == 'application/json':
            data = request.get_json()
            if not data or 'file' not in data:
                return jsonify({"error": "No se proporcionó archivo"}), 400
            
            content = base64.b64decode(data['file'])
        else:
            if 'file' not in request.files:
                return jsonify({"error": "No se proporcionó archivo"}), 400
            
            file = request.files['file']
            if file.filename == '':
                return jsonify({"error": "Nombre de archivo vacío"}), 400
            
            if not file.filename.lower().endswith('.pdf'):
                return jsonify({"error": "El archivo debe ser PDF"}), 400
            
            content = file.read()

        file_hash = hash_archivo(content)
        
        if ya_existente(file_hash):
            return jsonify({"message": "El archivo ya fue vectorizado anteriormente"}), 200
        
        texto = leer_pdf_bytes(content)
        if not texto.strip():
            return jsonify({"error": "No se pudo extraer texto del PDF"}), 400
        
        vectorizar_documento(texto)
        guardar_hash(file_hash)
        
        return jsonify({
            "success": True,
            "message": "Documento vectorizado correctamente",
            "filename": request.form.get('filename') or data.get('filename', 'unknown')
        }), 200
        
    except Exception as e:
        app.logger.error(f"Error en upload_pdf: {str(e)}")
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500

@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({"error": "Se requiere una pregunta"}), 400
        
        pregunta = data['question'] + "\nResponde en español."
        
        # Usar get_openai_callback para contar tokens
        with get_openai_callback() as cb:
            respuesta = qa_chain.run(pregunta)
            tokens_usados = cb.total_tokens
        
        respuesta_cifrada = cifrado_cesar(respuesta)
        
        return jsonify({
            "success": True,
            "answer": respuesta_cifrada,
            "tokens_used": tokens_usados
        }), 200
        
    except Exception as e:
        app.logger.error(f"Error en ask_question: {str(e)}")
        return jsonify({"error": f"Error al procesar la pregunta: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
