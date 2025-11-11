import os
import sys
import bs4
from dotenv import load_dotenv
from openai import OpenAI
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain.chat_models import init_chat_model

load_dotenv()

def _mask(s: str, keep=4):
    if not s:
        return "None"
    return s[:keep] + "…" + s[-keep:]

api_key = os.getenv("OPENAI_API_KEY")
project = os.getenv("OPENAI_PROJECT")
org_id = os.getenv("OPENAI_ORG_ID")
user_agent = os.getenv("USER_AGENT", "rag-app/1.0 (Daniel)")

if not api_key:
    sys.exit("Falta OPENAI_API_KEY en .env")

if api_key.startswith("sk-proj-") and not project:
    sys.exit("falta OPENAI_PROJECT en .env")

print(f"OPENAI_API_KEY: {_mask(api_key)}")
print(f"OPENAI_PROJECT: {project or 'None'}")
if org_id:
    print(f"OPENAI_ORG_ID: {org_id}")
print(f"USER_AGENT: {user_agent}")

try:
    client = OpenAI()
    _ = client.models.list()
    print("Conexión con OpenAI verificada correctamente.\n")
except Exception as e:
    sys.exit(f"Error de autenticación con OpenAI: {e}\nRevisa tu OPENAI_API_KEY y OPENAI_PROJECT en .env.")

model = init_chat_model("gpt-4.1")  # o "gpt-4o-mini"
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vector_store = InMemoryVectorStore(embeddings)

print("Cargando contenido del blog de Lilian Weng...")
loader = WebBaseLoader(
    web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(class_=("post-content", "post-title", "post-header"))
    ),
)
docs = loader.load()
print(f"Documento cargado con {len(docs[0].page_content)} caracteres.")

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
all_splits = text_splitter.split_documents(docs)
print(f" Documento dividido en {len(all_splits)} fragmentos.")

print(" Generando embeddings y construyendo índice vectorial...")
_ = vector_store.add_documents(documents=all_splits)
print("Fragmentos indexados en memoria.\n")

@tool(response_format="content_and_artifact")
def retrieve_context(query: str):
    """Recupera información relevante para responder una consulta."""
    retrieved_docs = vector_store.similarity_search(query, k=2)
    serialized = "\n\n".join(
        (f"Fuente: {doc.metadata}\nContenido: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs

prompt = (
    "Eres un asistente útil. Tienes acceso a una herramienta que recupera contexto "
    "del blog de Lilian Weng. Usa la herramienta para ayudar a responder preguntas del usuario."
)
agent = create_agent(model, tools=[retrieve_context], system_prompt=prompt)

print("RAG listo. Escribe tu pregunta (o 'salir' para terminar):\n")

while True:
    query = input("Pregunta: ")
    if query.lower() in ["salir", "exit", "quit"]:
        print("Hasta pronto!")
        break

    for event in agent.stream(
        {"messages": [{"role": "user", "content": query}]},
        stream_mode="values",
    ):
        if "messages" in event:
            msg = event["messages"][-1]
            # Compatibilidad con LangChain >=0.3
            role = getattr(msg, "role", None) or getattr(msg, "type", None)
            content = getattr(msg, "content", "")
            if role == "assistant" or role == "ai":
                print("\nRespuesta:", content, "\n")

