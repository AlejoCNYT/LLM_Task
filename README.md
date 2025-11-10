# LangChain RAG (Agent + Chain) — Windows 11 / VSCode

## 1) Crear entorno y activar
```powershell
cd "$HOME\OneDrive\Documents\rag-openai-pinecone"
python -m venv venv
.env\Scriptsctivate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 2) Variables de entorno
- Copia `.env.example` a `.env` y pon tu `OPENAI_API_KEY`.
- `.env` está ignorado por Git.

## 3) Ejecutar
- Agente (herramienta de retrieval + stream de pasos):
```powershell
python .\src\rag_agent.py
```
- Cadena simple (una sola llamada al modelo con dynamic prompt):
```powershell
python .\src\rag_chain.py
```

## 4) Cambiar fuente de datos
Edita `src/rag_setup.py` y reemplaza la URL en `web_paths`.
