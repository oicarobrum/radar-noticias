import streamlit as st
import requests
from wordcloud import WordCloud
import matplotlib.pyplot as plt

API_KEY = "AIzaSyBdS1g4qPTohtoz1yzSpWGBVCKrMJzN4v8"
CANAIS = {
    "UOL": "UCJ6w9AUgHSqv49QjGcgq4pA",
    "CartaCapital": "UCqpeJk1vW6EQqRQFyoqUeVg"
}

def buscar_videos(canal_id, max_results=5):
    url = (
        f"https://www.googleapis.com/youtube/v3/search"
        f"?key={API_KEY}&channelId={canal_id}&part=snippet&order=date&maxResults={max_results}"
    )
    resposta = requests.get(url).json()
    if "error" in resposta:
        st.error(f"Erro da API: {resposta['error'].get('message')}")
        return []
    videos = []
    for item in resposta.get("items", []):
        if item["id"]["kind"] == "youtube#video":
            titulo = item["snippet"]["title"]
            video_id = item["id"]["videoId"]
            videos.append({"title": titulo, "url": f"https://www.youtube.com/watch?v={video_id}"})
    return videos

def gerar_nuvem(videos, canal):
    if not videos:
        st.warning(f"Nenhum vídeo encontrado para o canal {canal}.")
        return
    texto = " ".join(v["title"] for v in videos if v["title"])
    if not texto.strip():
        st.warning(f"Nenhum título disponível para gerar nuvem no canal {canal}.")
        return
    try:
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(texto)
        st.subheader(f"Nuvem de palavras - {canal}")
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)
    except ValueError:
        st.warning(f"Nuvem não gerada: texto insuficiente para {canal}.")

st.title("📺 Radar de No
