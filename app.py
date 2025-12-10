import streamlit as st
from agent.core_2 import AgenticTutor
from pathlib import Path
from dotenv import load_dotenv
import json
load_dotenv()

st.set_page_config(page_title="Agentic AI Tutor", layout="centered")
st.title("💬 Agentic AI Tutor")

# Inicializa o tutor
if "tutor" not in st.session_state:
    st.session_state.tutor = AgenticTutor()

# Inicializa o dicionário de usuários
if "users" not in st.session_state:
    st.session_state.users = {}

# 🔹 Identificação simples do usuário
st.sidebar.header("Perfil do Aluno")
user_id = st.sidebar.text_input("Seu nome ou e-mail:", key="user_id")

if not user_id:
    st.info("Por favor, insira seu nome ou e-mail para começar 👇")
    st.stop()

# Inicializa dados do usuário se ainda não existir
if user_id not in st.session_state.users:
    profile = st.session_state.tutor.memory.get_user_profile(user_id)
    st.session_state.users[user_id] = {
        "profile": profile,
        "history": []
    }

user_data = st.session_state.users[user_id]
history = user_data["history"]
profile = user_data["profile"]

# 🔹 Se o perfil não existir, pede para configurar
if not profile:
    st.subheader("🧭 Configuração Inicial")
    nivel = st.selectbox("Escolha seu nível de proficiência:",
    ["A1 - Beginner", "A2 - Elementary", "B1 - Intermediate",
     "B2 - Upper-Intermediate", "C1 - Advanced", "C2 - Proficient"])
    modulo = st.selectbox("Qual o idioma estudado?", ["Inglês"])

    if st.button("Começar! 🚀"):
        st.session_state.tutor.memory.set_user_profile(user_id, nivel, modulo)
        # Atualiza profile na sessão
        st.session_state.users[user_id]["profile"] = st.session_state.tutor.memory.get_user_profile(user_id)
        st.success("Perfil configurado! Pode começar a conversar 👇")
        st.rerun()

    st.stop()  # Impede o resto do app de rodar até configurar

# 🔹 Se já configurou, mostra o perfil na barra lateral
st.sidebar.success(f"Nível: {profile['nivel']} | Idioma: {profile['modulo']}")
st.sidebar.subheader("📚 Guias e Materiais")
material_option = st.sidebar.selectbox("Escolha um guia:", ["Vocabulário", "Gramática", "Conversação"])
# Mapeia a opção selecionada para os nomes de arquivo corretos

file_map = {
    "Vocabulário": "Vocabulario.json",
    "Gramática": "Gramatica.json",
    "Conversação": "Conversacao.json"
}

user_folder = Path(f"data/users/{user_id}")
file_name = file_map.get(material_option)
file_path = user_folder / file_name

if file_path.exists():
    with open(file_path, "r", encoding="utf-8") as f:
        content = json.load(f)
    st.sidebar.json(content)
else:
    st.sidebar.info("Nenhum material salvo nesta categoria ainda.")

# ------------------- ADICIONAR MATERIAIS -------------------
import streamlit as st
from agent.material_manager import MaterialManager
from agent.rag import GuideRAG

mat = MaterialManager()

st.sidebar.subheader("📥 Adicionar material de estudo")

categoria = st.sidebar.selectbox("Categoria do material:", ["conversacao", "gramatica", "vocabulario"])
texto_material = st.sidebar.text_area("Cole o conteúdo aqui:")

if st.sidebar.button("Salvar material"):
    if texto_material.strip():
        file_path = mat.add_material(user_id, categoria, texto_material)
        st.sidebar.success(f"Material salvo em: {file_path}")

        # Atualiza RAG do usuário
        st.session_state.tutor.rag = GuideRAG(user_id)
        st.sidebar.info("RAG atualizado com os novos materiais!")
    else:
        st.sidebar.error("Por favor, insira algum conteúdo para salvar.")

# ------------------- TELA DE INTRODUÇÃO -------------------
st.subheader("👋 Bem-vindo ao Agentic AI Tutor")

st.markdown("""
O Agentic Tutor é um assistente de aprendizagem de inglês projetado para estudantes brasileiros,
adaptando explicações, atividades e dificuldade ao seu nível e estado emocional.

Aqui estão algumas frases que você pode usar para começar ou orientar sua aula:
""")

with st.expander("💬 Como começar a aula"):
    st.markdown("""
    - **Olá, quero começar minha aula de inglês**
    - **Olá, quero começar estudando o vocabulário**
    - **Quero começar com um módulo simples**
    """)

with st.expander("⚙️ Ajustar explicações e estilo de ensino"):
    st.markdown("""
    - **Não entendi, pode explicar de outro jeito?**
    - **Pode dar mais exemplos?**
    - **Quero uma atividade mais difícil**
    """)

with st.expander("🎮 Mini Games e atividades rápidas"):
    st.markdown("""
    - **Quero um mini game**
    - **Não estou gostando assim, podemos mudar?**
    - **Vamos jogar adivinhar palavras**
    - **Quero completar frases**
    """)

st.markdown("""
Quando estiver pronto, basta digitar uma mensagem abaixo e o tutor iniciará sua aula!
""")

# ------------------- CHAT -------------------
user_input = st.text_input("You:", "")

if st.button("Send") and user_input.strip():
    response = st.session_state.tutor.respond(user_id, user_input)
    history.append(("You", user_input))
    history.append(("Tutor", response))
    
for role, msg in history:
    st.write(f"**{role}:** {msg}")