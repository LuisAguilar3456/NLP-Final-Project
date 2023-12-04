import openai
import whisper

import pandas as pd
import numpy as np
import glob
import streamlit as st

st.title("Proyecto Final NLP")
st.subheader("Interfaz de Reconocimiento de Voz y Procesamiento de Lenguaje Natural")

st.sidebar.title("Idioma")
idiomas = ["English","Español", "Deutsch","François"]
language = st.sidebar.selectbox("Selecciona un idioma:",idiomas)



ListaAudios = glob.glob("*.m4a")

Audio=st.selectbox("Selecciona el audio con el que quieres trabajar:",ListaAudios)

NombreAudio = Audio[:-4]

TextoAudio = str(NombreAudio + " Transcribe.txt")
ResumenAudio = str(NombreAudio + " Summary.txt")

ArchivosTxt=glob.glob("*.txt")

openai.api_key = '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'

model = whisper.load_model("base")

file_path = Audio

def transcribe_audio(model, file_path):
    transcript = model.transcribe(file_path)
    return transcript['text']

def CustomChatGPT(user_input):
    messages = [{"role": "system", "content": "You are an office administer, summarize the text in key points"}]
    messages.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages
    )
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    return ChatGPT_reply

def TranslateChatGPT(language,text):
    translate2="You are an office administer, translate the next text from english to"+language
    messages = [{"role": "system", "content": translate2}]
    messages.append({"role": "user", "content": text})
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages
    )
    Translation = response["choices"][0]["message"]["content"]
    return Translation

transcription = ""
summary = ""

if TextoAudio in ArchivosTxt:
        st.write("Archivo con transcripción existente como "+TextoAudio)
        with open(TextoAudio, 'r') as archivo:
            transcription = archivo.read()
else:
     if st.button("Trasncribir"):
           st.write("Creando archivo con transcripción...")
           transcription = transcribe_audio(model, file_path)
           with open(TextoAudio, 'w') as archivo:
                archivo.write(transcription)
                st.write("Archivo de transcripción creado como "+ TextoAudio)


if ResumenAudio in glob.glob('*.txt'):
    st.write("Archivo con resumen existente como "+ResumenAudio)
    with open(ResumenAudio,'r') as archivo:
         summary = archivo.read()
else:
     if st.button("Resumen"):
           st.write("Creando archivo de resumen...")
           summary = CustomChatGPT(transcription)
           with open(ResumenAudio, 'w') as archivo:
                archivo.write(summary)
                st.write("Archivo de resumen creado como "+ ResumenAudio)


Transcribir_state = st.sidebar.checkbox("Muestra la transcripción")
Summary_state = st.sidebar.checkbox("Muestra el resumen")

if language == "English":
     
    if Transcribir_state:
          st.write(transcription)

    if Summary_state:
         st.write(summary)

else:
    if Transcribir_state:
          transcription = TranslateChatGPT(language, transcription)
          st.write(transcription)

    if Summary_state:
         summary = TranslateChatGPT(language,summary)
         st.write(summary)

