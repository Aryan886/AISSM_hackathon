# 🏛️ Civic Issue Routing System - FastAPI Backend

AI-powered system for routing civic issues to relevant NGOs using Google's Gemini API.

---

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Server](#running-the-server)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Customization](#customization)
- [Deployment](#deployment)

---

## ✨ Features

- **AI-Powered Classification**: Uses Gemini API to intelligently categorize civic issues
- **NGO Recommendations**: Returns top 3 most relevant NGOs from a curated list
- **Fallback System**: Keyword-based classification when Gemini API is unavailable
- **Modular Architecture**: Clean, maintainable codebase with separation of concerns
- **Request Validation**: Pydantic models for robust input/output validation
- **Error Handling**: Comprehensive error handling with fallback mechanisms
- **CORS Support**: Ready for integration with Node.js frontend
- **API Documentation**: Auto-generated Swagger/ReDoc documentation

---

## 📁 Project Structure

```
fastapi-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                      # FastAPI app & routes
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py              # Environment configuration
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py               # Pydantic request/response models
│   ├── services/
│   │   ├── __init__.py
│   │   ├── gemini_service.py        # Gemini API integration
│   │   ├── fallback_service.py      # Keyword-based fallback
│   │   └── ngo_data.py              # NGO database
│   └── utils/
│       ├── __init__.py
│       └── logger.py                # Logging configuration
├── .env                             # Environment variables (create from .env.example)
├── .env.example                     # Environment template
├── .gitignore
├── requirements.txt                 # Python dependencies
└── README.md
```

---

## 🔧 Prerequisites

- **Python 3.8+** (recommended: Python 3.10 or higher)
- **pip** (Python package manager)
- **Google Gemini API Key** ([Get one here](https://makersuite.google.com/app/apikey))

---

## 🚀 Installation

### 1. Clone the repository (or navigate to the project directory)


### 2. Create a virtual environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

### 1. Create `.env` file

Copy the example file and add your credentials:

```bash
cp .env.example .env
```

### 2. Edit `.env` file

```env
# Google Gemini API Configuration
GEMINI_API_KEY=your_actual_gemini_api_key_here

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Environment
ENVIRONMENT=development
```

**Get your Gemini API Key:**
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Get API Key"
4. Copy and paste into `.env` file

### 3. Customize NGO List (Optional)

Edit `app/services/ngo_data.py` to add your actual NGO data:

```python
NGOS = [
    {
        "name": "Your NGO Name",
        "category": "Category",
        "area": "Operating Area"
    },
    # Add more NGOs...
]
```

---

## 🏃 Running the Server

### Development Mode (with auto-reload)

```bash
python app/main.py
```

Or using uvicorn directly:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The server will start at: **http://localhost:8000**

---

## 📚 API Documentation

### Interactive API Docs

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints

#### 1. Health Check

```http
GET /
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "environment": "development",
  "gemini_configured": true
}
```

---

#### 2. Analyze Issue (Main Endpoint)

```http
POST /analyze-issue
```

**Request Body:**
```json
{
  "issue_text": "Water pipe burst near school, urgent help needed",
  "location": "Kothrud",
  "pincode": "411038",
  "image_url": "https://example.com/image.jpg"  // Optional
}
```

**Success Response (200 OK):**
```json
{
  "category": "Water Infrastructure",
  "severity": "High",
  "impact_score": 8.7,
  "suggested_ngos": [
    "CleanWater Foundation",
    "Urban Relief NGO",
    "CommunityAid Trust"
  ],
  "reasoning": "Public safety risk near school. Immediate response recommended."
}
```

**Error Response (400/500):**
```json
{
  "error": "Error message",
  "detail": "Detailed information",
  "fallback_used": false
}
```

---

## 🧪 Testing

### Using cURL

```bash
curl -X POST "http://localhost:8000/analyze-issue" \
  -H "Content-Type: application/json" \
  -d '{
    "issue_text": "Water pipe burst near school, urgent help needed",
    "location": "Kothrud",
    "pincode": "411038"
  }'
```

### Using Python requests

```python
import requests

url = "http://localhost:8000/analyze-issue"
data = {
    "issue_text": "Water pipe burst near school, urgent help needed",
    "location": "Kothrud",
    "pincode": "411038"
}

response = requests.post(url, json=data)
print(response.json())
```

### Using the Swagger UI

1. Go to http://localhost:8000/docs
2. Click on `/analyze-issue` endpoint
3. Click "Try it out"
4. Enter your request data
5. Click "Execute"

---

## 🔄 Customization

### 1. Change NGO Data Source

Currently, NGOs are hardcoded in `app/services/ngo_data.py`. You can modify this to:

**Load from JSON file:**
```python
import json

def get_ngo_list():
    with open("ngos.json", "r") as f:
        return json.load(f)
```

**Fetch from API:**
```python
import requests

def get_ngo_list():
    response = requests.get("http://your-nodejs-server/api/ngos")
    return response.json()
```

**Query from MongoDB:**
```python
from pymongo import MongoClient

def get_ngo_list():
    client = MongoClient("mongodb://localhost:27017")
    db = client.civic_db
    return list(db.ngos.find({}, {"_id": 0}))
```

### 2. Add Image Processing (Future)

When ready to process images with Gemini Vision:

1. Update `app/services/gemini_service.py`
2. Change model to `gemini-pro-vision`
3. Modify `analyze_issue()` to include image data

### 3. Customize Fallback Keywords

Edit `app/services/fallback_service.py`:

```python
CATEGORY_KEYWORDS = {
    "YourCategory": ["keyword1", "keyword2", "keyword3"],
    # Add more categories...
}
```

### 4. Adjust CORS Settings

For production, update `app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://your-frontend-domain.com"],  # Specific origins
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)
```

---

## 🚢 Deployment

### Using Docker (Recommended)

Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY .env .env

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t civic-issue-api .
docker run -p 8000:8000 civic-issue-api
```

### Using systemd (Linux)

Create `/etc/systemd/system/civic-api.service`:
```ini
[Unit]
Description=Civic Issue Routing API
After=network.target

[Service]
User=your_user
WorkingDirectory=/path/to/fastapi-backend
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable civic-api
sudo systemctl start civic-api
```

---

## 🛠️ Troubleshooting

### Gemini API Key Not Working

- Verify your API key is correct in `.env`
- Check if you have billing enabled (if required)
- System will automatically fall back to keyword classification

### Import Errors

```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

### Port Already in Use

```bash
# Change port in .env
PORT=8001
```

Or kill the process:
```bash
# Linux/Mac
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

---

## 📝 License

This project is for hackathon use. Add your license information here.

---

## 👥 Contributors

Your team members here

---

## 🔗 Related

- [Google Gemini API Docs](https://ai.google.dev/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

---

## 💡 Next Steps

1. ✅ Set up FastAPI backend
2. ⬜ Integrate with Node.js
3. ⬜ Connect to MongoDB
4. ⬜ Implement competitive acceptance model
5. ⬜ Add deadline & escalation logic
6. ⬜ Implement image processing with Gemini Vision
7. ⬜ Deploy to production

---

**Happy Hacking! 🚀**