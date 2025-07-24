import os
import hashlib
import base64  # Importación faltante para decodificar base64
from pathlib import Path
import fitz
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from langchain.chains import RetrievalQA
from pinecone import Pinecone, ServerlessSpec

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
        chunk_size=2000,
        chunk_overlap=500,
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
        # Verificar si se envió como form-data o json
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

        # Procesamiento del archivo
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
        
        pregunta = data['question'] + "\nRecuerda que debes responder en español."
        respuesta = qa_chain.run(pregunta)
        
        return jsonify({
            "success": True,
            "answer": respuesta
        }), 200
        
    except Exception as e:
        app.logger.error(f"Error en ask_question: {str(e)}")
        return jsonify({"error": f"Error al procesar la pregunta: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


# # === Interfaz Streamlit ===
# st.set_page_config(page_title="PDF Gemini QA", layout="centered")
# st.title("📄🔍 Pregunta a tu PDF con Gemini + Pinecone")

# # --- Subida de PDF (opcional) ---
# uploaded_file = st.file_uploader("Sube un archivo PDF (opcional)", type="pdf")
# if uploaded_file:
#     content = uploaded_file.read()
#     file_hash = hash_archivo(content)

#     if ya_existente(file_hash):
#         st.info("✅ Este archivo ya fue vectorizado anteriormente.")
#     else:
#         with st.spinner("📚 Procesando y vectorizando el PDF..."):
#             texto = leer_pdf_bytes(content)
#             if texto.strip():
#                 vectorizar_documento(texto)
#                 guardar_hash(file_hash)
#                 st.success("✅ Documento vectorizado y almacenado correctamente.")
#             else:
#                 st.error("⚠️ No se pudo extraer texto del PDF.")

# # --- Crear chain QA (sin estado) ---
# if "qa_chain" not in st.session_state:
#     st.session_state.qa_chain = crear_chain_qa()

# # --- Entrada de pregunta ---
# pregunta = st.text_input("📝 Escribe tu pregunta:")
# pregunta = pregunta + "/n Recuerda que debes responder en español."

# if st.button("💬 Preguntar") and pregunta.strip():
#     with st.spinner("🧠 Pensando..."):
#         try:
#             # Cada llamada es independiente, no hay historial guardado
#             with get_openai_callback() as cb:
#                 respuesta = st.session_state.qa_chain.run(pregunta)
#                 st.success(respuesta)
#                 st.info(f"🔢 Tokens estimados utilizados: {cb.total_tokens}")
#         except Exception as e:
#             st.error(f"❌ Ocurrió un error: {e}")
