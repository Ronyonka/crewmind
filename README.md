## ✅ Prerequisites

- **Python 3.8+** (for the backend)
- **Node.js 16+ and npm** (for the frontend)
- **MongoDB Atlas account** (or your own MongoDB URI)
- **Git** (to clone the repository)

---

## 🚀 Installation & Startup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Ronyonka/crewmind.git
cd crewmind
```

---

### 2. Environment Variables

- Copy the example environment file and fill in your own values:

```bash
cp .env.example .env
```

- Edit `.env` with your MongoDB Atlas credentials.

---

### 3. Backend Setup (FastAPI + MongoDB)

1. **Create and activate a virtual environment** (in the root or backend):

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies:**

   ```bash
   pip install -r backend/requirements.txt
   ```

3. **Start the FastAPI server:**

   ```bash
   cd backend
   uvicorn main:app --reload
   ```

---

### 4. Frontend Setup (React)

1. **Install dependencies:**

   ```bash
   cd frontend
   npm install
   ```

2. **Start the React development server:**

   ```bash
   npm start
   ```

   > The app will be available at [http://localhost:3000](http://localhost:3000)

---

## 🛠️ Technologies/Libraries Used

- **Frontend:** React, Tailwind CSS
- **Backend:** FastAPI, Motor (async MongoDB), Pydantic
- **Database:** MongoDB Atlas

---

## 💡 What I'd Do Differently With More Time

- Connect the backend to an actual LLM API (such as OpenAI or similar) for real AI-generated responses instead of a simulated one.

---
