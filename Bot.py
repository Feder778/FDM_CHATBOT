#streamlit run Bot.py (stop=crtl+c)

import streamlit as st
import groq

#modelos
MODELOS = ["llama3-8b-8192", "llama3-70b-8192"]

#configurar la pagina

def configurar_pagina():
    st.set_page_config(page_title="CHATBOT" , page_icon="🤣")
    st.title("Bienvenidos a mi chatbot")


# MOSTRAR EL SIDEBAR CON LOS MODELOS

def mostrar_sidebar():
    st.sidebar.title("ELEJÍ TU MODELO DE IA FAVORITO")
    modelo = st.sidebar.selectbox("¿ Cuál elegís ?" , MODELOS, index=0)
    st.write(f"**MODELO SELECCIONADO** : {modelo}")
    return modelo

#UN CLIENTE GROQ
def crear_cliente_groq():
    groq_api_key = st.secrets["GROQ_API_KEY"]
    return groq.Groq(api_key=groq_api_key)

#Estado de los mensajes
def inicializacion_estado_chat():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []


#Historial del chat
def mostrar_historial_chat():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"]):
         st.markdown(mensaje["content"])

#obtener mensaje de ususario
def obtener_mensaje_usuario():
    return st.chat_input("Envía un mensaje")

#agregtar mensaje al estado
def agregar_mensaje_al_historial(role, content):
    st.session_state.mensajes.append({"role":role, "content":content})

#mostrar los mensajes en pantalla
def  mostrar_mensaje(role, content):
    with st.chat_message(role):
        st.markdown(content)

#llamar al modelo groq
def obtener_respuesta_modelo (cliente, modelo, mensajes):
    respuesta = cliente.chat.completions.create(
        model=modelo,
        messages=mensajes,
        stream = False
    )
    return respuesta.choices[0].message.content

#flujo de la app
def ejecutar_app():
    configurar_pagina()
    modelo = mostrar_sidebar()
    cliente = crear_cliente_groq()

    inicializacion_estado_chat()
    mostrar_historial_chat()

    mensaje_usuario = obtener_mensaje_usuario()
    print(mensaje_usuario)

    if mensaje_usuario :
        agregar_mensaje_al_historial("user",mensaje_usuario)
        mostrar_mensaje("user",mensaje_usuario)

        mensaje_modelo = obtener_respuesta_modelo(cliente,modelo,st.session_state.mensajes)

        agregar_mensaje_al_historial("assistant",mensaje_modelo)
        mostrar_mensaje("assistant",mensaje_modelo)


if __name__ == "__main__":
        ejecutar_app()