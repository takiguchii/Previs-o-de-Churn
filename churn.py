import streamlit as st
import pandas as pd
import pickle

try:
    with open('modelo_correto.pkl', 'rb') as arquivo:
        modelo = pickle.load(arquivo)
except FileNotFoundError:
    st.error("Erro: O arquivo 'modelo_correto.pkl' não foi encontrado na pasta.")
    st.stop()

st.title("Sistema de Previsão de Churn")
st.write("Insira os dados do cliente para verificar o risco de cancelamento.")

mensalidade = st.number_input("Qual o valor da Mensalidade?", min_value=0.0, value=50.0)
tempo_contrato = st.number_input("Quantos meses de contrato?", min_value=0, value=1)
contrato_mensal = st.selectbox("O contrato é Mês a Mês?", ["Sim", "Não"])

é_mensal = 1 if contrato_mensal == "Sim" else 0

if st.button("Analisar Cliente"):
    
    colunas_do_modelo = modelo.feature_names_in_
    pistas = pd.DataFrame(columns=colunas_do_modelo)
    
    pistas.loc[0] = 0 
    
    if 'MonthlyCharges' in pistas.columns:
        pistas.at[0, 'MonthlyCharges'] = mensalidade
        
    if 'tenure' in pistas.columns:
        pistas.at[0, 'tenure'] = tempo_contrato
        
    if 'Contract_Month-to-month' in pistas.columns:
        pistas.at[0, 'Contract_Month-to-month'] = é_mensal

    previsao = modelo.predict(pistas)
    
    st.divider()
    if previsao[0] == 1:
        st.error(" ALTO RISCO: O cliente deve cancelar o serviço. Acione a retenção!")
    else:
        st.success(" SEGURO: O cliente tem baixo risco de cancelamento.")