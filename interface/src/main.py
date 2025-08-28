import os
from datetime import datetime, timedelta

import requests
import streamlit as st

# Configurações
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://fastapi:8000")

# Inicializar estado da sessão para o timer
if "timer_start" not in st.session_state:
    st.session_state.timer_start = None
    st.session_state.timer_running = False


# Função para formatar o tempo restante
def format_time(seconds):
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins:02d}:{secs:02d}"


# Customização de estilo css
st.markdown(
    """
    <style>
    #timer {
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
        color: #4CAF50;
    }
    div.stButton > button {
        background-color: #4CAF50; 
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
    }
    /* Efeito hover */
    div.stButton > button:hover {
        background-color: #45a049;
    }
    </style>
    <script>
    function updateTimer(endTime) {
        let timerElement = document.getElementById("timer");
        if (!timerElement) return;

        let interval = setInterval(() => {
            let now = new Date().getTime();
            let timeLeft = endTime - now;
            if (timeLeft <= 0) {
                clearInterval(interval);
                timerElement.innerText = "00:00";
                return;
            }
            let minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
            let seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);
            timerElement.innerText = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        }, 1000);
    }
    </script>
    """,
    unsafe_allow_html=True,
)

st.title("Interface de Integração com n8n")
st.write(
    "Controle a ativação do fluxo n8n. O arquivo final é retornado quando o processo é concluído com sucesso."
)

# Botão para disparar o webhook
if st.button("Ativar Fluxo"):
    try:
        response = requests.post(f"{FASTAPI_URL}/activate", json={"activate": True})
        response.raise_for_status()
        result = response.json()
        if result["status"] == "success":
            st.success(result["message"])

            # Iniciar o timer de 1 hora
            st.session_state.timer_start = datetime.now() + timedelta(hours=1)
            st.session_state.timer_running = True
            # Injetar JavaScript para atualizar o timer
            end_time_ms = int(st.session_state.timer_start.timestamp() * 1000)
            st.markdown(
                f"<script>updateTimer({end_time_ms});</script>", unsafe_allow_html=True
            )
        else:
            st.error(result["message"])
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao enviar sinal: {str(e)}")
    except Exception as e:
        st.error(
            "Ocorreu um erro ao tentar se conectar com o servidor. Verifique se o seu backend está funcionando corretamente"
        )
        print(e)

# Verificar status do arquivo
st.subheader("Status do Arquivo")

st.write("Tempo médio para processamento de dados: 60 minutos")

# Timer de execução
if st.session_state.timer_running:
    time_left = (st.session_state.timer_start - datetime.now()).total_seconds()
    if time_left > 0:
        st.markdown(
            f'<div id="timer">{format_time(int(time_left))}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown('<div id="timer">00:00</div>', unsafe_allow_html=True)
        st.session_state.timer_running = False
else:
    st.markdown('<div id="timer">Não iniciado</div>', unsafe_allow_html=True)

if st.button("Verificar Arquivo"):
    try:
        response = requests.get(f"{FASTAPI_URL}/check-file")
        response.raise_for_status()
        file_result = response.json()
        if file_result["status"] == "success":
            st.success("Arquivo recebido com sucesso!")
            st.download_button(
                label="Baixar Arquivo",
                data=requests.get(
                    f"{FASTAPI_URL}/download/{file_result['file_name']}"
                ).content,
                file_name=file_result["file_name"],
                mime="application/octet-stream",
            )
        elif file_result["status"] == "pending":
            st.info(file_result["message"])
        else:
            st.error(file_result["message"])
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao verificar arquivo: {str(e)}")
