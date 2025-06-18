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
YOUTUBE_CHANNELS = ["UCJF6Rl6aLO7GgfvQKoWqZfw"]  # ID do CartaCapital
API_KEY
