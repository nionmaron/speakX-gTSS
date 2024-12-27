# docker build -t text2speak-app .
# docker run -d -p 8505:8505 text2speak-app

# 
import streamlit as st
from gtts import gTTS
import tempfile
import base64

# Configuração da página com título e ícone
st.set_page_config(
    page_title="Multilingual Text-to-Speech Converter",
    page_icon="🎤",  # Você pode substituir por uma URL de ícone ou outro emoji
    layout="centered",
    initial_sidebar_state="auto",
)

# Dicionário para suportar múltiplos idiomas na interface
LANGUAGE_UI = {
    'English': {
        'title': "Multilingual Text-to-Speech Converter",
        'description': "Enter text, select language, and listen to the generated audio!",
        'dev_message': "Developed by Nion M. Dransfeld nionmaron.com",
        'text_input': "Enter your text here:",
        'select_lang': "Select language:",
        'button_speak': "Speak",
        'warning_text': "Please enter some text.",
        'download_button': "Download Audio",
        'credits_gtts': "Credits to [gTTS](https://pypi.org/project/gTTS/).",
    },
    'Português': {
        'title': "Conversor de Texto para Fala Multilíngue",
        'description': "Digite algum texto, selecione o idioma e ouça o áudio gerado!",
        'dev_message': "Desenvolvido por Nion M. Dransfeld nionmaron.com",
        'text_input': "Digite seu texto aqui:",
        'select_lang': "Selecione o idioma:",
        'button_speak': "Falar",
        'warning_text': "Por favor, insira algum texto.",
        'download_button': "Baixar Áudio",
        'credits_gtts': "Créditos ao [gTTS](https://pypi.org/project/gTTS/).",
    }
}

# Dicionário de idiomas suportados pelo gTTS (nomes em inglês)
LANGUAGES = {
    'English (United States)': 'en',
    'Portuguese (Brazil)': 'pt',
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de',
    'Italian': 'it',
    'Japanese': 'ja',
    'Chinese (Simplified)': 'zh-cn',
    'Korean': 'ko',
    # Adicione mais idiomas conforme necessário
}

# Função para converter texto em áudio offline
def text_to_speech(text, lang):
    try:
        # Adicionar crédito ao final do texto
        text_with_credit = f"{text} (nionmaron.com)"
        # Converte texto em fala usando gTTS
        tts = gTTS(text_with_credit, lang=lang, slow=False)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            tts.save(temp_audio.name)
            return temp_audio.name
    except Exception as e:
        if interface_lang == 'English':
            st.error(f"Error converting text to speech: {e}")
        else:
            st.error(f"Erro ao converter texto para áudio: {e}")
        return None

# Função para gerar link de download
def get_download_link(file_path, filename, label):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:audio/mp3;base64,{b64}" download="{filename}">{label}</a>'
    return href

# Seleção de idioma da interface
interface_lang = st.sidebar.selectbox("Select Interface Language / Selecionar Idioma da Interface", list(LANGUAGE_UI.keys()), index=0)

# Selecionar o dicionário de idioma com base na seleção
ui = LANGUAGE_UI[interface_lang]

# Configuração do Streamlit
st.title(ui['title'])
st.markdown(f"**{ui['description']}**")

# Mensagem de Desenvolvimento abaixo do título
st.markdown(f"_{ui['dev_message']}_")

# Entrada de texto
text_input = st.text_area(ui['text_input'], height=200)

# Seleção de idioma para TTS
selected_language = st.selectbox(ui['select_lang'], list(LANGUAGES.keys()), index=0)

# Botão para converter texto em áudio
audio_file = None
if st.button(ui['button_speak']):
    if text_input.strip():
        # Obter o código do idioma selecionado
        lang_code = LANGUAGES[selected_language]
        
        # Gerar o arquivo de áudio
        audio_file = text_to_speech(text_input, lang_code)
        
        if audio_file:
            # Reproduzir o áudio no Streamlit
            st.audio(audio_file, format="audio/mp3")
    else:
        st.warning(ui['warning_text'])

# Opção de download do áudio gerado
if audio_file:
    # Nome do arquivo para download
    filename = "tts_audio.mp3"
    # Ler o arquivo de áudio
    with open(audio_file, "rb") as f:
        audio_bytes = f.read()
    # Botão de download
    st.download_button(
        label=ui['download_button'],
        data=audio_bytes,
        file_name=filename,
        mime="audio/mp3"
    )

# Créditos para o pacote gTTS
st.markdown("---")
st.markdown(ui['credits_gtts'])

