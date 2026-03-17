import streamlit as st
import pandas as pd
from datetime import datetime, date

# Configuração da página
st.set_page_config(page_title="Validade Supermercado", page_icon="🛒")

st.title("🛡️ Controle de Validade")

# Arquivo para salvar os dados (Simples CSV)
NOME_ARQUIVO = "estoque_validade.csv"

# Carregar dados existentes ou criar novos
try:
    df = pd.read_csv(NOME_ARQUIVO)
    df['Validade'] = pd.to_datetime(df['Validade']).dt.date
except FileNotFoundError:
    df = pd.DataFrame(columns=["Produto", "Validade", "Setor"])

# --- ÁREA DE CADASTRO ---
with st.sidebar:
    st.header("➕ Novo Cadastro")
    nome = st.text_input("Nome do Produto").upper()
    validade = st.date_input("Data de Validade", min_value=date.today())
    setor = st.selectbox("Setor", ["Mercearia", "Laticínios", "Açougue", "Hortifruti", "Padaria"])
    
    if st.button("Cadastrar no Sistema"):
        if nome:
            novo_item = pd.DataFrame([{"Produto": nome, "Validade": validade, "Setor": setor}])
            df = pd.concat([df, novo_item], ignore_index=True)
            df.to_csv(NOME_ARQUIVO, index=False)
            st.success(f"{nome} adicionado!")
            st.rerun()
        else:
            st.error("Digite o nome do produto!")

# --- LÓGICA DE ALERTAS ---
st.subheader("📋 Relatório de Estoque")

if not df.empty:
    hoje = date.today()
    
    # Função para definir o status visual
    def verificar_status(val):
        dias = (val - hoje).days
        if dias < 0: return "🔴 VENCIDO"
        if dias <= 30: return f"⚠️ ALERTA ({dias} dias)"
        return "✅ OK"

    df['Status'] = df['Validade'].apply(verificar_status)
    
    # Exibe a tabela organizada
    st.dataframe(df, use_container_width=True)
    
    # Filtro rápido para o colaborador
    if st.button("Limpar lista (CUIDADO)"):
        pd.DataFrame(columns=["Produto", "Validade", "Setor"]).to_csv(NOME_ARQUIVO, index=False)
        st.rerun()
else:
    st.info("Nenhum produto cadastrado ainda.")