import streamlit as st
import requests
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Simular dados coletados (porque API do YouTube exige chave e quota)
# No futuro podemos colocar a integração real com API ou YouTube RSS
videos_uol = [
    {"title": "Lula discursa na ONU sobre clima", "views": 50000},
    {"title": "Conflito Israel e Hamas: novos ataques", "views": 120000},
    {"title": "CPI das Apostas avança no Senado", "views": 30000},
]

videos_cartacapital = [
    {"title": "Governo Lula enfrenta desafios no Congresso", "views": 60000},
    {"title": "Israel e Palestina: mais uma escalada", "views": 90000},
    {"title": "Economia brasileira e os juros", "views": 25000},
]

def gerar_nuvem(videos, canal):
    texto = " ".join(video["title"] for video in videos)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(texto)
    st.subheader(f"Nuvem de palavras - {canal}")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)

def mostrar_ranking(videos, canal):
    st.subheader(f"Ranking de vídeos por views - {canal}")
    videos_ordenados = sorted(videos, key=lambda x: x["views"], reverse=True)
    for video in videos_ordenados:
        st.write(f"🎥 {video['title']} - 👀 {video['views']} visualizações")

# Streamlit app
st.title("📺 Radar de Notícias - UOL e CartaCapital")

st.markdown("## 🎬 UOL")
gerar_nuvem(videos_uol, "UOL")
mostrar_ranking(videos_uol, "UOL")

st.markdown("## 🎬 CartaCapital")
gerar_nuvem(videos_cartacapital, "CartaCapital")
mostrar_ranking(videos_cartacapital, "CartaCapital")
