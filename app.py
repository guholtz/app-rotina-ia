import streamlit as st
import os
from dotenv import load_dotenv
from google import genai

# Carrega configurações e IA
load_dotenv()
CHAVE_API = os.getenv("GEMINI_API_KEY")
cliente = genai.Client(api_key=CHAVE_API)

# Configuração da página para parecer um app mobile
st.set_page_config(page_title="Rotina.AI", page_icon="📱", layout="centered")

st.title("📱 Rotina.AI")
st.write("Configure seus horários fixos e os hábitos que deseja enciaxar.")

st.divider() # Linha divisória

# Organizando os horários em duas colunas para economizar espaço
st.subheader("⏰ Seus Horários Fixos")
col1, col2 = st.columns(2)

with col1:
    hora_acordar = st.time_input("Hora de acordar")
    hora_dormir = st.time_input("Hora de dormir")

with col2:
    hora_trabalho_inicio = st.time_input("Início do trabalho")
    hora_trabalho_fim = st.time_input("Fim do trabalho")

# Seleção de hábitos
st.subheader("🎯 Novos Hábitos")
habitos = st.multiselect(
    "O que você quer incluir no seu dia?",
    ["Leitura", "Exercícios Físicos", "Estudos", "Meditação", "Caminhada"]
)
detalhes_extras = st.text_input("Mais algum detalhe? (Ex: 1h de almoço às 12h)")

st.divider()

# Botão de geração
if st.button("Gerar Minha Rotina Ideal", type="primary", use_container_width=True):
    with st.spinner("A IA está calculando os melhores horários..."):
        
        # Montando o texto (prompt) que será enviado para a IA
        prompt_ia = f"""
        Aja como um especialista em produtividade e crie uma rotina diária otimizada.
        Considere estritamente os seguintes horários fixos do usuário:
        - Acorda às: {hora_acordar}
        - Dorme às: {hora_dormir}
        - Trabalha das {hora_trabalho_inicio} até as {hora_trabalho_fim}.
        
        O usuário deseja encaixar os seguintes hábitos na rotina: {', '.join(habitos)}.
        Detalhes extras: {detalhes_extras}
        
        Crie um cronograma hora a hora, sendo realista com tempos de deslocamento, refeições e descanso. 
        Formate a resposta de forma limpa e fácil de ler no celular.
        """
        
        try:
            # Tenta conectar e enviar a mensagem para a IA
            chat = cliente.chats.create(model='gemini-3.6-flash')
            resposta = chat.send_message(prompt_ia)
            
            # Se der certo, exibe o resultado
            st.success("Cronograma criado com sucesso!")
            st.markdown(resposta.text)
            
        except Exception as e:
            # Se o servidor do Google cair ou estiver ocupado, exibe este aviso
            st.warning("O servidor da inteligência artificial está muito ocupado neste momento. Por favor, aguarde alguns segundos e clique em gerar novamente.")
            # st.error(f"Detalhe técnico: {e}") # Opcional: descomente para ver o erro técnico na tela