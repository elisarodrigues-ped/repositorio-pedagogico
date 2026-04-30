import streamlit as st
import os

# 1. Configurações e Injeção de CSS
st.set_page_config(page_title="PNEERQ - Repositório", layout="wide")

# CSS customizado para aplicar o "verde prefeitura" em todos os botões e arredondar bordas
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #196F3D;
        color: white;
        border-radius: 20px;
        border: none;
        font-weight: bold;
    }
    div.stButton > button:first-child:hover {
        background-color: #145A32;
        color: white;
    }
    /* Reduz o espaçamento superior para subir os elementos */
    .block-container {
        padding-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Cabeçalho (Título entre os logos e sem linha divisória)
col1, col2, col3 = st.columns([1, 4, 1], vertical_alignment="center")
with col1:
    if os.path.exists("logo_prefeitura.png"): 
        st.image("logo_prefeitura.png", width=120)
with col2:
    st.markdown("<h2 style='text-align: center; margin-bottom: 0;'>REPOSITÓRIO DE SEQUÊNCIAS DIDÁTICAS PNEERQ</h2>", unsafe_allow_html=True)
with col3:
    if os.path.exists("logo_proape.png"): 
        st.image("logo_proape.png", width=160) # Tamanho do logo PROAPE aumentado

# 3. Lógica de Navegação em Sessão
if 'pagina' not in st.session_state: st.session_state.pagina = 'home'
if 'path' not in st.session_state: st.session_state.path = ""

def navegar(destino, caminho=""):
    st.session_state.pagina = destino
    st.session_state.path = caminho

# Listas atualizadas estritamente sem acentuação para estabilidade no servidor
disciplinas_reg_ef2 = ["LINGUA_PORTUGUESA", "MATEMATICA", "CIENCIAS", "HISTORIA", "GEOGRAFIA", "INGLES", "ARTE", "EDUCACAO_FISICA"]
disciplinas_em = ["LINGUA_PORTUGUESA", "MATEMATICA", "FISICA", "QUIMICA", "BIOLOGIA", "INGLES", "ARTE", "EDUCACAO_FISICA", "CIENCIAS_HUMANAS"]

# --- PÁGINA 1: INICIAL ---
if st.session_state.pagina == 'home':
    c1, c2 = st.columns(2)
    if c1.button("ENSINO REGULAR", use_container_width=True): navegar('regular')
    if c2.button("EDUCAÇÃO DE JOVENS E ADULTOS", use_container_width=True): navegar('eja_niveis')

# --- PÁGINA 2: ANOS REGULAR (6º ao 9º) ---
elif st.session_state.pagina == 'regular':
    st.subheader("Ensino Regular - Selecione o Ano")
    anos = [f"{i}º ANO" for i in range(6, 10)]
    cols = st.columns(4)
    for i, ano in enumerate(anos):
        if cols[i].button(ano, use_container_width=True): navegar('disciplinas', f"documentos/Regular/{ano}")
    if st.button("⬅️ Voltar"): navegar('home')

# --- PÁGINA 2: EJA (EF2 vs EM) ---
elif st.session_state.pagina == 'eja_niveis':
    c1, c2 = st.columns(2)
    if c1.button("ENSINO FUNDAMENTAL 2", use_container_width=True): navegar('eja_ef2_termos')
    if c2.button("ENSINO MÉDIO", use_container_width=True): navegar('eja_em_termos')
    if st.button("⬅️ Voltar"): navegar('home')

# --- PÁGINA 3: TERMOS EJA ---
elif st.session_state.pagina in ['eja_ef2_termos', 'eja_em_termos']:
    tipo = "EF2" if st.session_state.pagina == 'eja_ef2_termos' else "EM"
    pasta = "EJA_EF2" if tipo == "EF2" else "EJA_EM"
    termos = 4 if tipo == "EF2" else 3
    st.subheader(f"EJA {tipo} - Selecione o Termo")
    cols = st.columns(termos)
    for i in range(1, termos + 1):
        label = f"{i}º Termo"
        if cols[i-1].button(label, use_container_width=True): navegar('disciplinas', f"documentos/{pasta}/{label}")
    if st.button("⬅️ Voltar"): navegar('eja_niveis')

# --- PÁGINA 4: DISCIPLINAS ---
elif st.session_state.pagina == 'disciplinas':
    st.subheader("Selecione a Disciplina")
    lista = disciplinas_em if "EJA_EM" in st.session_state.path else disciplinas_reg_ef2
    cols = st.columns(4)
    for i, disc in enumerate(lista):
        if cols[i%4].button(disc.replace("_", " "), use_container_width=True): 
            navegar('download', f"{st.session_state.path}/{disc}")
    if st.button("⬅️ Voltar"): navegar('home')

# --- PÁGINA 5: DOWNLOADS (GRID 5 COLUNAS) ---
elif st.session_state.pagina == 'download':
    parts = st.session_state.path.split('/')
    st.info(f"Arquivos: {parts[-2]} > {parts[-1].replace('_', ' ')}")
    
    if os.path.exists(st.session_state.path):
        arquivos = sorted([f for f in os.listdir(st.session_state.path) if f.lower().endswith(('.pdf', '.doc', '.docx'))])
        if arquivos:
            for i in range(0, len(arquivos), 5):
                cols = st.columns(5)
                for j, arq in enumerate(arquivos[i:i+5]):
                    with open(f"{st.session_state.path}/{arq}", "rb") as f:
                        cols[j].download_button(label=f"📄 {arq}", data=f, file_name=arq, use_container_width=True)
        else: st.warning("Ainda não há arquivos nesta categoria.")
    else: st.error("Pasta não encontrada. Verifique o nome no GitHub.")
    
    if st.button("⬅️ Voltar para Disciplinas"): 
        novo_path = "/".join(st.session_state.path.split('/')[:-1])
        navegar('disciplinas', novo_path)
