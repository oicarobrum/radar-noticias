import streamlit as st
import requests
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Sua chave da API do YouTube
API_KEY = "AIzaSyBdS1g4qPTohtoz1yzSpWGBVCKrMJzN4v8"

# IDs dos canais
CANAIS = {
    "UOL": "UCJ6w9AUgHSqv49QjGcgq4pA",
    "CartaCapital": "UCqpeJk1vW6EQqRQFyoqUeVg"
}

def buscar_videos(canal_id, max_results=10):
    url = (
        "https://www.googleapis.com/youtube/v3/search"
        f"?key={API_KEY}"
        f"&channelId={canal_id}"
        "&part=snippet"
        "&order=date"
        f"&maxResults={max_results}"
    )
    response = requests.get(url)
    if response.status_code != 200:
        st.error(f"Erro ao acessar API: {response.status_code}")
        return []
    data = response.json()
    videos = []
    for item in data.get("items", []):
        if "title" in item["snippet"]:
            videos.append({
                "title": item["snippet"]["title"],
                "url": f"https://www.youtube.com/watch?v={item['id'].get('videoId')}"
            })
    return videos

def gerar_nuvem(videos, canal):
    if not videos:
        st.warning(f"Nenhum vídeo encontrado para o canal {canal}.")
        return
    texto = " ".join(video["title"] for video in videos if video["title"])
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
    except ValueError as e:
        st.error(f"Erro ao gerar nuvem de palavras: {e}")

# App Streamlit
st.title("📺 Radar de Notícias - UOL e CartaCapital")

for nome, canal_id in CANAIS.items():
    st.header(f"🎥 {nome}")
    videos = buscar_videos(canal_id)
    gerar_nuvem(videos, nome)
    for video in videos:
        st.markdown(f"- [{video['title']}]({video['url']})")
