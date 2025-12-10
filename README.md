# 🤖 Agentic AI Tutor

O **Agentic AI Tutor** é um tutor inteligente para ensino de inglês que utiliza **Inteligência Artificial, análise de emoções, memória de aprendizado e RAG (Retrieval-Augmented Generation)** para oferecer uma experiência personalizada, adaptativa e interativa ao estudante.

Ele foi projetado especialmente para estudantes brasileiros, ajustando:
- O nível de dificuldade
- O tipo de explicação
- As atividades
- E até o estilo de resposta conforme o estado emocional do aluno.

---

## 🚀 Funcionalidades Principais

- ✅ Tutor conversacional baseado em LLM  
- ✅ Análise de emoções do aluno em tempo real  
- ✅ Sistema de **memória** (palavras, tópicos, progresso)  
- ✅ Suporte a **mini-games educacionais**  
- ✅ RAG com materiais personalizados (vocabulário, gramática e conversação)  
- ✅ Interface web com **Streamlit**  
- ✅ Salvamento automático de materiais por usuário  
- ✅ Perfil do aluno com nível (A1 a C2)  
- ✅ Adaptação automática do ensino conforme desempenho  

---

## 🧠 Arquitetura do Projeto

- `agent/core.py` → Cérebro principal do tutor (AgenticTutor)  
- `EmotionAnalyser` → Análise emocional do aluno  
- `MemoryManager` → Histórico e progresso do estudante  
- `LLMHandler` → Comunicação com o modelo de linguagem  
- `GuideRAG` → Recuperação de conteúdo com vetorização  
- `MaterialManager` → Gerenciamento dos materiais de estudo  
- `app.py` → Interface web com Streamlit  

Fluxo geral:
1. O aluno envia uma mensagem  
2. O sistema detecta a emoção  
3. O mini-agente interpreta a intenção  
4. O RAG busca conteúdo nos materiais  
5. O LLM gera a resposta adaptada  
6. O progresso é salvo automaticamente  

---

## 🖥️ Interface (Streamlit)

A aplicação possui:
- Cadastro simples do aluno (nome ou e-mail)  
- Escolha de nível (A1 a C2)  
- Visualização de materiais salvos  
- Upload manual de conteúdos  
- Chat interativo com o tutor  
- Sugestões de como iniciar as aulas  
- Mini-games educacionais  

---

## 📦 Requisitos do Projeto

Crie um ambiente virtual e instale os requisitos abaixo:

```bash
pip install -r requirements.txt

---
### 🔹 Core
- `streamlit==1.26.0`
- `python-dotenv==1.0.1`
- `gTTS==2.3.2`
- `SpeechRecognition==3.9.0`

### 🔹 LangChain + Groq
- `langchain-groq==0.1.3`
- `langchain-core>=0.1.45,<0.2.0`
- `langchain-community>=0.0.10`
- `langchain-text-splitters>=0.0.2`

### 🔹 RAG / Vetorização
- `chromadb==0.4.6`
- `sentence-transformers==2.6.1`

### 🔹 Utilitários
- `numpy==1.26.0`
- `pandas==2.1.1`
- `tiktoken==0.4.0`

---

## ▶️ Como Executar o Projeto

### 👨‍💻 Autor
Desenvolvido por Emerson Sousa
Mestrado em Engenharia Informática – Universidade de Coimbra
Human Centered AI