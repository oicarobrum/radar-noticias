import streamlit as st
from utils.youtube_scraper import get_youtube_data
from utils.wordcloud import generate_wordcloud
import pandas as pd
import os
from dotenv import load_dotenv

# Configuração
load_dotenv()
st.set_page_config(layout="wide", page_title="Radar de Notícias")

# Dados fixos (substitua com seus canais)
YOUTUBE_CHANNELS = ["UCJF6Rl6aLO7GgfvQKoWqZfw"]  # CartaCapital
API_KEY = os.getenv("YOUTUBE_API_KEY") or "AIzaSyBdS1g4qPTohtoz1yzSpWGBVCKrMJzN4v8"  # Sua chave

# Título
st.title("🔍 Radar de Notícias")

# Busca dados do YouTube
if API_KEY:
    st.header("📺 Vídeos do YouTube")
    all_videos = []
    for channel in YOUTUBE_CHANNELS:
        videos = get_youtube_data(API_KEY, channel)
        all_videos.extend(videos)
    
    # Exibe tabela
    df = pd.DataFrame(all_videos)
    st.dataframe(df)

    # Nuvem de palavras
    if len(all_videos) > 0:
        st.header("📊 Nuvem de Palavras")
        generate_wordcloud([video['title'] for video in all_videos])
else:
    st.error("❌ Adicione sua API Key do YouTube no arquivo
