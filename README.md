# RAG App · Búsqueda y Respuesta con LangChain

Aplicación de **búsqueda aumentada con recuperación (RAG)** sobre el artículo “LLM Powered Autonomous Agents” de Lilian Weng.  
Carga el contenido web, lo divide en fragmentos, genera embeddings y responde preguntas usando contexto recuperado.

---

## Requisitos

- Python 3.10+
- Cuenta y clave de API de OpenAI
- Conexión a Internet
---

## Estructura

```
rag_app/
├─ rag_app.py
├─ requirements.txt
└─ .env
```

---

## Instalación

1) Instalar dependencias:
```bash
pip install -r requirements.txt
```
2) Agrega los valores OPENAI_API_KEY y LANGSMITH_API_KEY
   
## Ejecución

```bash
python rag_app.py
```

Flujo esperado en consola:
```
Conexión con OpenAI verificada correctamente.
Cargando contenido del blog…
Documento cargado con N caracteres.
Documento dividido en M fragmentos.
Generando embeddings y construyendo índice vectorial…
Fragmentos indexados en memoria.

RAG listo. Escribe tu pregunta (o 'salir' para terminar):
```

Ejemplo:
```
Pregunta: ¿De qué colores se compone el verde?
Respuesta: …
```
<img width="1265" height="748" alt="imagen" src="https://github.com/user-attachments/assets/a1890fe3-92c2-43a2-ad6c-459680e132f0" />

---

## Detalles técnicos

- **Carga**: `WebBaseLoader` (BeautifulSoup) sobre URL objetivo.
- **Split**: `RecursiveCharacterTextSplitter` (tamaño 1000, solapamiento 200).
- **Embeddings**: `OpenAIEmbeddings` con `text-embedding-3-small` (ajustable a `text-embedding-3-large`).
- **Vector store**: `InMemoryVectorStore`.
- **Agente**: `create_agent` con herramienta `retrieve_context` (búsqueda k=2 y respuesta con contexto).

---

## Ajustes recomendados

- **Cuota/Costos**: si la cuenta no tiene facturación activa o el proyecto no tiene saldo, usar `text-embedding-3-small`.
- **USER_AGENT**: define `USER_AGENT` en `.env` para evitar advertencias.
- **Velocidad/Precisión**: aumentar o reducir `chunk_size`, `chunk_overlap` y `k` según el caso de uso.

---

## Solución de problemas

- **401 Invalid API Key**  
  Verifica que `OPENAI_API_KEY` esté en una sola línea y sin espacios.  
  Si usas `sk-proj_…`, añade `OPENAI_PROJECT=proj_…` del panel de OpenAI.

- **429 Insufficient Quota**  
  Activa facturación en la cuenta o usa `text-embedding-3-small`.  
  Revisa el uso en: https://platform.openai.com/usage

- **Error al imprimir respuesta**  
  El script ya maneja compatibilidad de mensajes en LangChain ≥0.3 (atributos en lugar de dicts).  
  Si actualizas LangChain y cambia el tipo de mensaje, ajusta la lectura de `role`/`content`.

---

## Licencia

Uso académico y de demostración. Modifica libremente según tus necesidades.
