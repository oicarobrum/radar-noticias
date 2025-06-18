import streamlit as st
import requests
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# SUA CHAVE DE API DO YOUTUBE
API_KEY = "AIzaSyBdS1g4qPTohtoz1yzSpWGBVCKrMJzN4v8"

# Função para buscar vídeos de um canal
def buscar_videos(canal_id, max_results=5):
    url = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={canal_id}&part=snippet&order=date&maxResults={max_results}"
    resposta = requests.get(url).json()
    
    videos = []
    for item in resposta.get("items", []):
        if item["id"]["kind"] == "youtube#video":
            title = item["snippet"]["title"]
            video_id = item["id"]["videoId"]
            views = buscar_views(video_id)
            videos.append({"title": title, "views": views})
    return videos

# Função para buscar visualizações
def buscar_views(video_id):
    url = f"https://www.googleapis.com/youtube/v3/videos?key={API_KEY}&id={video_id}&part=statistics"
    resposta = requests.get(url).json()
    stats = resposta["items"][0]["statistics"]
    return int(stats.get("viewCount", 0))

# Função para gerar nuvem
def gerar_nuvem(videos, canal):
    texto = " ".join(video["title"] for video in videos)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(texto)
    st.subheader(f"Nuvem de palavras - {canal}")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)

# Função para ranking
def mostrar_ranking(videos, canal):
    st.subheader(f"Ranking de vídeos por views - {canal}")
    videos_ordenados = sorted(videos, key=lambda x: x["views"], reverse=True)
    for video in videos_ordenados:
        st.write(f"🎥 {video['title']} - 👀 {video['views']} visualizações")

# IDs dos canais
CANAL_UOL = "UCFF1pdaH00PzPMyGbVbKR0Q"
CANAL_CARTA = "UCaKZDEMDdQc8t6GzFj1_TDw"

st.title("📺 Radar de Notícias - YouTube em Tempo Real")

# UOL
st.markdown("## 🎬 UOL")
videos_uol = buscar_videos(CANAL_UOL)
gerar_nuvem(videos_uol, "UOL")
mostrar_ranking(videos_uol, "UOL")

# CartaCapital
st.markdown("## 🎬 CartaCapital")
videos_carta = buscar_videos(CANAL_CARTA)
gerar_nuvem(videos_carta, "CartaCapital")
mostrar_ranking(videos_carta, "CartaCapital")
