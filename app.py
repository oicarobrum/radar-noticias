import streamlit as st
import requests
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 🔑 Sua chave da API do YouTube
API_KEY = "AIzaSyBdS1g4qPTohtoz1yzSpWGBVCKrMJzN4v8"

# IDs dos canais
CANAIS = {
    "UOL": "UCvC5yPzIBTpdj5M6ZKiH4NQ",
    "CartaCapital": "UC3NB9nNqf_ZkR2iNJl-N44w"
}

# Função para buscar vídeos
def buscar_videos(canal_id, max_results=10):
    url = (
        f"https://www.googleapis.com/youtube/v3/search"
        f"?key={API_KEY}&channelId={canal_id}&part=snippet"
        f"&order=date&maxResults={max_results}"
    )
    resposta = requests.get(url).json()

    videos = []
    for item in resposta.get("items", []):
        if item["id"]["kind"] == "youtube#video":
            titulo = item["snippet"]["title"]
            video_id = item["id"]["videoId"]
            views = buscar_views(video_id)
            videos.append({
                "title": titulo,
                "views": views,
                "url": f"https://www.youtube.com/watch?v={video_id}"
            })
    return videos

# Função para buscar visualizações
def buscar_views(video_id):
    url = (
        f"https://www.googleapis.com/youtube/v3/videos"
        f"?key={API_KEY}&id={video_id}&part=statistics"
    )
    resposta = requests.get(url).json()
    itens = resposta.get("items", [])
    if itens and "viewCount" in itens[0]["statistics"]:
        return int(itens[0]["statistics"]["viewCount"])
    return 0

# Função para gerar nuvem de palavras
def gerar_nuvem(videos, canal):
    if not videos:
        st.warning(f"Nenhum vídeo encontrado para o canal {canal}.")
        return
    texto = " ".join(video["title"] for video in videos if video["title"])
    if not texto.strip():
        st.warning(f"Nenhum título disponível para gerar nuvem no canal {canal}.")
        return
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(texto)
    st.subheader(f"Nuvem de palavras - {canal}")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)

# Interface Streamlit
st.title("📺 Radar de Notícias - UOL e CartaCapital")

dados_todos = []

for nome, canal_id in CANAIS.items():
    st.header(f"🎥 {nome}")
    videos = buscar_videos(canal_id)
    gerar_nuvem(videos, nome)

    if videos:
        st.subheader(f"Ranking de vídeos - {nome}")
        videos_ordenados = sorted(videos, key=lambda x: x["views"], reverse=True)
        for video in videos_ordenados:
            st.write(f"[{video['title']}]({video['url']}) - 👁 {video['views']:,} visualizações")

    dados_todos.extend(videos)

# Ranking geral
if dados_todos:
    st.header("🏆 Ranking geral de visualizações")
    dados_todos = sorted(dados_todos, key=lambda x: x["views"], reverse=True)
    for video in dados_todos:
        st.write(f"[{video['title']}]({video['url']}) - 👁 {video['views']:,} visualizações")
