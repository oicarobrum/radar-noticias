import streamlit as st
import requests
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# === CONFIGURAÇÕES ===
API_KEY = 'AIzaSyBdS1g4qPTohtoz1yzSpWGBVCKrMJzN4v8'
CHANNEL_IDS = {
    "UOL": "UCvC5nQtw14Bwt8Ue6K0Z7IQ",
    "CartaCapital": "UCXUA_3yFwyiV7xBMQ41rVPA"
}

# === FUNÇÕES ===
def get_videos(channel_id):
    url = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={channel_id}&part=snippet,id&order=date&maxResults=10"
    res = requests.get(url).json()
    videos = []
    for item in res.get('items', []):
        if item['id']['kind'] == 'youtube#video':
            videos.append({
                'video_id': item['id']['videoId'],
                'title': item['snippet']['title']
            })
    return videos

def get_view_count(video_id):
    url = f"https://www.googleapis.com/youtube/v3/videos?key={API_KEY}&id={video_id}&part=statistics"
    res = requests.get(url).json()
    try:
        return int(res['items'][0]['statistics']['viewCount'])
    except:
        return 0

# === APP ===
st.title("📺 Radar de Notícias - UOL e CartaCapital")

all_videos = []
for name, channel_id in CHANNEL_IDS.items():
    st.header(f"🎥 {name}")
    videos = get_videos(channel_id)
    for video in videos:
        video['views'] = get_view_count(video['video_id'])
        video['channel'] = name
    videos = sorted(videos, key=lambda x: x['views'], reverse=True)
    for video in videos:
        st.write(f"[{video['title']}](https://www.youtube.com/watch?v={video['video_id']}) — 👁️ {video['views']} views")
    all_videos.extend(videos)

# === NUVEM DE PALAVRAS ===
if all_videos:
    text = ' '.join([v['title'] for v in all_videos])
    wc = WordCloud(width=800, height=400, background_color='white').generate(text)
    st.subheader("☁️ Nuvem de Palavras dos Títulos")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)
