from wordcloud import WordCloud
import matplotlib.pyplot as plt
import streamlit as st

def generate_wordcloud(texts):
    wordcloud = WordCloud(
        width=1200,
        height=600,
        background_color='white',
        stopwords=['o', 'a', 'de', 'que', 'é']  # Palavras ignoradas
    ).generate(" ".join(texts))
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)
