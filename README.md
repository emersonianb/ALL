# 🤖 Agentic AI Tutor (ALL)

The **Agentic AI Tutor (ALL)** is an AI-powered English learning assistant designed to provide Brazilian students with a personalized, adaptive, and interactive learning experience.

The project combines **Large Language Models (LLMs), emotion analysis, learning memory, and Retrieval-Augmented Generation (RAG)** to adapt its teaching approach according to each student's proficiency level, learning progress, and emotional state.

🔗 **Live Demo:** [https://emerson-all.streamlit.app/](https://emerson-all.streamlit.app/)

---

## 🚀 Key Features

- **AI-powered conversational tutor:** Interactive English practice using a Large Language Model.
- **Emotion Analysis:** Identifies the student's emotional state and adapts the tone and style of responses.
- **Learning Memory:** Stores conversation history, vocabulary, topics, and student progress to support continuous learning.
- **Personalized Learning:** Adjusts explanations, activities, and difficulty according to proficiency level (A1–C2).
- **RAG Integration:** Retrieves relevant information from personalized learning materials, including vocabulary, grammar, and conversation guides.
- **Educational Mini-games:** Provides interactive activities to reinforce learning.
- **Student Profiles:** Maintains individual learning information and progress.
- **Automatic Data Persistence:** Saves learning materials and student information.
- **Web Interface:** Built with Streamlit for an accessible and interactive experience.

---

## 🧠 Project Architecture

The system is organized into specialized components that work together to deliver an adaptive learning experience.

| Component | Responsibility |
|---|---|
| `agent/core.py` | Main tutor orchestration (`AgenticTutor`) |
| `EmotionAnalyser` | Analyzes the student's emotional state |
| `MemoryManager` | Manages conversation history and learning progress |
| `LLMHandler` | Handles communication with the language model |
| `GuideRAG` | Retrieves relevant content from learning materials |
| `MaterialManager` | Organizes and manages student learning materials |
| `app.py` | Streamlit web application |

### Conversation Workflow

1. The student submits a message through the chat interface.
2. The system analyzes the student's emotional state.
3. An interpretation component identifies the student's intent.
4. The RAG module retrieves relevant information from available learning materials.
5. The language model generates a context-aware and personalized response.
6. The student's interaction and learning progress are stored in memory.

---

## 🖥️ User Interface

The Streamlit application provides the following features:

- Student registration using a name or email.
- English proficiency level selection (A1–C2).
- Interactive chat with the AI tutor.
- Personalized study material management.
- Manual upload of learning resources.
- Suggestions to help students start their lessons.
- Educational mini-games.

---

## 🛠️ Technologies

- **Python** – Main programming language.
- **Streamlit** – Web application interface.
- **Groq API** – Language model inference.
- **LangChain** – LLM integration and orchestration.
- **ChromaDB** – Vector database for semantic retrieval.
- **Sentence Transformers** – Text embeddings.
- **Pandas & NumPy** – Data processing.
- **gTTS & SpeechRecognition** – Text-to-speech and speech recognition.

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/emersonianb/all.git
cd all
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Linux / macOS:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

Replace `your_groq_api_key` with your API key from [Groq Console](https://console.groq.com/).

**Important:** Never commit your `.env` file or expose your API key publicly. When deploying on Streamlit Community Cloud, configure the key through the application's Secrets settings.

### 5. Run the application

```bash
streamlit run app.py
```

---

## 📚 Main Dependencies

The project uses the following core libraries:

| Category | Libraries |
|---|---|
| Core | Streamlit, python-dotenv |
| LLM Integration | LangChain, LangChain-Groq |
| RAG & Vectorization | ChromaDB, Sentence Transformers |
| Data Processing | NumPy, Pandas, tiktoken |
| Speech | gTTS, SpeechRecognition |

For exact versions, refer to [`requirements.txt`](requirements.txt).

---

## 👨‍💻 Author

**Emerson Sousa**

M.Sc. student in Computer Science / Informatics Engineering  
University of Coimbra

**Research Interests:** Human-Centered AI, Agentic AI, and AI for Education.
