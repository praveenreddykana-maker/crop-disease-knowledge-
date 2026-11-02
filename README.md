# 🌿 Crop Disease Knowledge Assistant

An AI-powered agricultural assistant using **Retrieval-Augmented Generation (RAG)** to provide accurate information about crop diseases, symptoms, causes, prevention, and management.

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────────────────────────┐     ┌─────────────┐
│  React.js   │────▶│         FastAPI Backend           │────▶│ Gemini LLM  │
│  Tailwind   │◀────│  RAG Pipeline (LangChain + FAISS) │     │    API      │
│  Frontend   │     │  SentenceTransformers Embeddings  │     └─────────────┘
└─────────────┘     └──────────────────────────────────┘
                            │
                    ┌───────▼───────┐
                    │  FAISS Vector │
                    │     Store     │
                    └───────────────┘
```

### RAG Pipeline Flow
1. User asks a question → 2. Embed question (all-MiniLM-L6-v2) → 3. Similarity search in FAISS → 4. Retrieve top-K chunks → 5. Build prompt with context → 6. Gemini generates grounded answer → 7. Return answer + source citations

## 📦 Project Structure

```
crop-disease-assistant/
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI routers
│   │   │   ├── chat.py       # Chat/RAG endpoints
│   │   │   ├── documents.py  # Document upload/management
│   │   │   ├── admin.py      # Admin authentication
│   │   │   └── crops.py      # Crop disease info
│   │   ├── core/
│   │   │   ├── config.py         # Settings
│   │   │   └── knowledge_base.py # Built-in disease data
│   │   ├── models/
│   │   │   └── schemas.py    # Pydantic models
│   │   └── services/
│   │       ├── rag_service.py      # Core RAG pipeline
│   │       ├── document_service.py # Document management
│   │       └── chat_history_service.py
│   ├── uploads/      # Uploaded PDFs
│   ├── vector_store/ # FAISS index
│   ├── data/         # Chat history
│   ├── main.py       # FastAPI app
│   ├── requirements.txt
│   ├── .env          # Environment variables
│   └── .env.example
│
└── frontend/
    ├── src/
    │   ├── components/   # Reusable components
    │   ├── pages/        # Page components
    │   ├── context/      # React context (chat state)
    │   ├── layouts/      # Layout components
    │   └── api.js        # API client
    ├── .env
    └── package.json
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 16+
- A [Google AI Studio](https://makersuite.google.com/app/apikey) API key (free)

---

### Step 1: Clone & Navigate

```bash
cd "crop-disease-assistant"
```

---

### Step 2: Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate
# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Configure environment:**

Copy `.env.example` to `.env` and set your API key:

```ini
GEMINI_API_KEY=your_actual_api_key_here
ADMIN_PASSWORD=admin123
```

**Start the backend:**

```bash
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`  
API docs: `http://localhost:8000/docs`

---

### Step 3: Frontend Setup

```bash
cd frontend

# Install dependencies
npm install --legacy-peer-deps

# Start development server
npm run dev
```

The app will be available at `http://localhost:5173`

---

## 🔑 Getting a Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click **"Create API Key"**
3. Copy the key
4. Paste it in `backend/.env` as `GEMINI_API_KEY=...`
5. Restart the backend

> **Without an API key**: The system works in fallback mode, returning raw retrieved content from the knowledge base. Full AI-generated responses require the key.

---

## 🌾 Built-in Knowledge Base

The system comes pre-loaded with disease profiles for:

| Crop | Diseases Included |
|------|------------------|
| 🌾 Rice | Blast, Bacterial Leaf Blight, Sheath Blight |
| 🌾 Wheat | Stem Rust, Yellow/Stripe Rust, Powdery Mildew |
| 🍅 Tomato | Leaf Curl Virus, Early Blight, Late Blight |
| 🥔 Potato | Late Blight, Common Scab |
| ☁️ Cotton | Leaf Curl Virus, Fusarium Wilt |
| 🌽 Maize | Lethal Necrosis, Gray Leaf Spot |
| 🥜 Groundnut | Early Leaf Spot, Rosette Virus |

Each profile includes: disease name, pathogen, symptoms, causes, favorable conditions, prevention, management, and source references.

---

## 📋 API Endpoints

### Chat
- `POST /api/chat/` — Send a question, get RAG-powered answer
- `GET /api/chat/history` — List all conversations
- `GET /api/chat/history/{id}` — Get conversation messages
- `DELETE /api/chat/history/{id}` — Delete a conversation
- `DELETE /api/chat/history` — Clear all history

### Crops
- `GET /api/crops/` — List supported crops
- `GET /api/crops/{crop}/diseases` — Get diseases for a crop

### Documents (Admin required)
- `POST /api/documents/upload` — Upload a PDF
- `GET /api/documents/` — List uploaded documents
- `DELETE /api/documents/{id}` — Delete a document
- `GET /api/documents/stats/knowledge-base` — Get KB statistics

### Admin
- `POST /api/admin/login` — Authenticate as admin
- `GET /api/admin/health` — System health check

---

## 🛡️ Admin Panel

Access the admin panel at `/admin` in the frontend.

**Default credentials:** `admin123` (change in `.env`)

Admin capabilities:
- Upload agricultural PDFs to expand the knowledge base
- View all uploaded documents and their indexing status
- Delete documents
- View vector store statistics

---

## ⚙️ Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `GEMINI_API_KEY` | — | Google Gemini API key |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | SentenceTransformers model |
| `CHUNK_SIZE` | `1000` | Document chunk size (chars) |
| `CHUNK_OVERLAP` | `200` | Chunk overlap (chars) |
| `TOP_K_RESULTS` | `5` | Number of chunks to retrieve |
| `ADMIN_PASSWORD` | `admin123` | Admin panel password |

---

## 🔒 Security Notes

- API keys are stored in environment variables, never in code
- Document management is admin-protected
- File upload validation (PDF only, 50MB max)
- CORS configured for local development only
- Change `ADMIN_PASSWORD` before any production deployment

---

## 🌱 Extending the Knowledge Base

You can add knowledge in two ways:

**1. Upload PDFs via the Admin Panel:**
- Agricultural research papers
- Government extension service guides
- Crop protection manuals

**2. Add to the built-in data:**
Edit `backend/app/core/knowledge_base.py` and add entries to `CROP_DISEASE_DATA`, then restart the backend (the vector store will be rebuilt).

---

## 📚 Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend | React.js + Tailwind CSS + Vite |
| Backend | Python + FastAPI |
| RAG Framework | LangChain |
| Embeddings | SentenceTransformers (all-MiniLM-L6-v2) |
| Vector DB | FAISS |
| LLM | Google Gemini 1.5 Flash |
| PDF Processing | PyPDF |

---

## ⚠️ Disclaimer

This application is for informational purposes only. Always consult qualified local agricultural experts or extension services before making decisions about crop management, especially regarding pesticide applications or chemical treatments.

