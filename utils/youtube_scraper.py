import requests
import os

def get_youtube_data(api_key, channel_id, max_results=10):
    try:
        url = f"https://www.googleapis.com/youtube/v3/search?key={api_key}&channelId={channel_id}&part=snippet&order=date&maxResults={max_results}"
        response = requests.get(url)
        data = response.json()
        
        videos = []
        for item in data.get('items', []):
            if 'videoId' not in item['id']:
                continue
            videos.append({
                'title': item['snippet']['title'],
                'channel': item['snippet']['channelTitle'],
                'data': item['snippet']['publishedAt'][:10],  # Formata data
                'url': f"https://youtu.be/{item['id']['videoId']}"
            })
        return videos
    except Exception as e:
        print(f"Erro: {e}")
        return []
