import streamlit as st
import requests

# Configuração inicial
st.set_page_config(page_title="Consulta de Projetos de Lei", page_icon="📜")

BASE_URL = "https://dadosabertos.camara.leg.br/api/v2"

# Função para buscar PL por número e ano
def buscar_por_numero(sigla, numero, ano):
    params = {"siglaTipo": sigla, "numero": numero, "ano": ano}
    r = requests.get(f"{BASE_URL}/proposicoes", params=params)
    if r.status_code == 200:
        dados = r.json().get("dados", [])
        if dados:
            return dados[0]
    return None

# Função para buscar PL por palavra-chave
def buscar_por_palavra(termo):
    params = {"keywords": termo, "siglaTipo": "PL", "itens": 20}
    r = requests.get(f"{BASE_URL}/proposicoes", params=params)
    if r.status_code == 200:
        dados = r.json().get("dados", [])
        if dados:
            return dados[0]
    return None

# Interface do aplicativo
st.title("📜 Consulta de Projetos de Lei – Câmara dos Deputados")
st.write("Este aplicativo permite consultar Projetos de Lei por número/ano ou por palavra-chave.")

opcao = st.radio("Escolha o tipo de busca:", ["Por número/ano", "Por palavra-chave"])

if opcao == "Por número/ano":
    tipo = st.text_input("Sigla do tipo (ex.: PL, PEC):", "PL")
    numero = st.text_input("Número (ex.: 2630):")
    ano = st.text_input("Ano (ex.: 2020):")

    if st.button("Buscar"):
        if not numero or not ano:
            st.warning("Preencha o número e o ano.")
        else:
            pl = buscar_por_numero(tipo, numero, ano)
            if pl:
                st.success(f"{pl['siglaTipo']} {pl['numero']}/{pl['ano']}")
                st.write("**Ementa:**", pl.get("ementa", "Ementa não disponível"))
            else:
                st.error("Projeto não encontrado.")

else:
    termo = st.text_input("Digite uma palavra-chave (ex.: liberdade, saúde, educação):")
    if st.button("Buscar"):
        if not termo:
            st.warning("Digite uma palavra para buscar.")
        else:
            pl = buscar_por_palavra(termo)
            if pl:
                st.success(f"{pl['siglaTipo']} {pl['numero']}/{pl['ano']}")
                st.write("**Ementa:**", pl.get("ementa", "Ementa não disponível"))
            else:
                st.error("Nenhum projeto encontrado com esse termo.")
