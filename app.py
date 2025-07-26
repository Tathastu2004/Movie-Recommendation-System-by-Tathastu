import streamlit as st
import pandas as pd
import requests
import os
from dotenv import load_dotenv
from movie_recommender import final_data, recommend, get_movie_overview_and_genres

# Load environment variables
load_dotenv()

# TMDb API credentials from environment variables
TMDB_API_KEY = os.getenv('TMDB_API_KEY')
TMDB_BEARER_TOKEN = os.getenv('TMDB_BEARER_TOKEN')



# --- CSS for Netflix-like look and full-width adaptation ---
st.markdown('''
    <style>
    body {background-color: #141414;}
    .stApp {font-family: "Netflix Sans", Arial, sans-serif;}
    .block-container {padding-top: 1.5rem !important; padding-bottom: 0 !important; max-width: 100vw !important; width: 100vw !important;}
    .movie-row {display: flex; flex-direction: row; gap: 1.5rem; overflow-x: auto; padding-bottom: 1rem; width: 100vw; margin-left: -3vw;}
    .movie-card {background: #222; border-radius: 12px; min-width: 220px; max-width: 220px; color: #fff; box-shadow: 0 2px 8px #0008; display: flex; flex-direction: column; align-items: center; padding: 1rem 0.5rem; transition: transform 0.2s;}
    .movie-card:hover {transform: scale(1.04); box-shadow: 0 4px 16px #e5091440;}
    .movie-poster {border-radius: 8px; width: 180px; height: 270px; object-fit: cover; margin-bottom: 0.5rem;}
    .movie-title {font-size: 1.1rem; font-weight: bold; margin: 0.5rem 0 0.2rem 0; text-align: center;}
    .movie-genres {font-size: 0.95rem; color: #e50914; margin-bottom: 0.3rem; text-align: center;}
    .movie-overview {font-size: 0.92rem; color: #ccc; text-align: center;}
    .search-section {margin-top: 1.5rem;}
    .genre-btn {background: #222; color: #fff; border-radius: 20px; padding: 0.5rem 1.2rem; cursor: pointer; border: 2px solid #222; transition: background 0.2s, border 0.2s, color 0.2s; font-weight: 500; font-size: 1rem; white-space: nowrap; margin-right: 0.5rem; margin-bottom: 0.5rem; display: inline-block;}
    .genre-btn:hover {background: #e50914; color: #fff; border: 2px solid #e50914;}
    </style>
''', unsafe_allow_html=True)

st.set_page_config(page_title='Movie Recommendation System', layout='wide')

st.title('🎬 Movie Recommendation System by Tathastu')
st.markdown('<div style="font-size:1.2rem; color:#fff; margin-bottom:1.2rem;">Click a genre below for quick recommendations, or use the search box for custom results!</div>', unsafe_allow_html=True)

# Prepare data for searching
all_titles = pd.Series(final_data['title']).unique().tolist()
all_titles = sorted(all_titles)

# Get all genres from the dataset
import ast
def extract_all_genres():
    genres_set = set()
    import movie_recommender
    for i, row in movie_recommender.data.iterrows():
        try:
            genres = [g['name'].lower() for g in ast.literal_eval(row['genres'])]
            genres_set.update(genres)
        except Exception:
            continue
    return sorted(list(genres_set))
all_genres = extract_all_genres()

# --- Helper function for poster fetching ---
def fetch_poster_url(title):
    url = f'https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={title}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            poster_path = data['results'][0].get('poster_path')
            if poster_path:
                return f'https://image.tmdb.org/t/p/w500{poster_path}'
    return 'https://via.placeholder.com/300x450?text=No+Image'

# --- Genre bar at the top using Streamlit-native buttons in a horizontal scrollable row ---
if 'selected_genre' not in st.session_state:
    st.session_state['selected_genre'] = None

# Set number of genres per row for scrollability
GENRES_PER_ROW = 10
num_rows = (len(all_genres) + GENRES_PER_ROW - 1) // GENRES_PER_ROW

for row in range(num_rows):
    cols = st.columns(GENRES_PER_ROW)
    for i in range(GENRES_PER_ROW):
        idx = row * GENRES_PER_ROW + i
        if idx >= len(all_genres):
            continue
        genre = all_genres[idx]
        is_selected = (genre == st.session_state['selected_genre'])
        btn_label = genre.title()
        btn_style = f"background-color: {'#e50914' if is_selected else '#222'}; color: #fff; border-radius: 20px; border: 2px solid {'#e50914' if is_selected else '#222'}; font-weight: 500; font-size: 1rem; min-width: 120px; max-width: 120px; height: 48px; margin-bottom: 0.2rem;"
        if cols[i].button(btn_label, key=f'genre_{genre}', help=f'Show movies in {genre.title()} genre', use_container_width=True):
            st.session_state['selected_genre'] = genre
            st.session_state['search_input'] = ''

# --- Search box ---
st.markdown('<div class="search-section">', unsafe_allow_html=True)
if 'search_input' not in st.session_state:
    st.session_state['search_input'] = ''
search_input = st.text_input('Search by movie title or genre/keyword:', st.session_state['search_input'])
st.session_state['search_input'] = search_input
st.markdown('</div>', unsafe_allow_html=True)

# --- Helper to display movies in horizontal row ---
def display_movie_row(movie_titles, header=None):
    if header:
        st.subheader(header)
    if not movie_titles:
        st.warning('No movies found.')
        return
    row_html = '<div class="movie-row">'
    for title in movie_titles:
        poster_url = fetch_poster_url(title)
        overview, genres = get_movie_overview_and_genres(title)
        genres_str = ', '.join(genres)
        row_html += f'''<div class="movie-card">
            <img src="{poster_url}" class="movie-poster"/>
            <div class="movie-title">{title}</div>
            <div class="movie-genres">{genres_str}</div>
            <div class="movie-overview">{overview[:120] + ('...' if len(overview) > 120 else '')}</div>
        </div>'''
    row_html += '</div>'
    st.markdown(row_html, unsafe_allow_html=True)

# --- Logic for displaying results ---
import movie_recommender
selected_genre = st.session_state['selected_genre']
if selected_genre:
    matches = []
    for i, row in movie_recommender.data.iterrows():
        try:
            genres = [g['name'].lower() for g in ast.literal_eval(row['genres'])]
            if selected_genre in genres:
                matches.append(row['title'])
        except Exception:
            continue
    display_movie_row(matches[:20], header=f'Movies in genre: {selected_genre.title()}')
    st.info('You can also use the search box below for more options.')
elif search_input:
    search_lower = search_input.lower().strip()
    if search_lower in all_genres:
        matches = []
        for i, row in movie_recommender.data.iterrows():
            try:
                genres = [g['name'].lower() for g in ast.literal_eval(row['genres'])]
                if search_lower in genres:
                    matches.append(row['title'])
            except Exception:
                continue
        display_movie_row(matches[:20], header=f'Movies in genre: {search_input.title()}')
    elif search_input in all_titles:
        recommendations = recommend(search_input)
        display_movie_row(recommendations, header=f'Top 5 recommendations for "{search_input}"')
    else:
        st.warning('No matching movie title or genre found. Try another search.')
else:
    selected_movie = st.selectbox('Or choose a movie:', all_titles)
    if st.button('Recommend'):
        recommendations = recommend(selected_movie)
        display_movie_row(recommendations, header=f'Top 5 recommendations for "{selected_movie}"')

st.markdown('---')
st.caption('Developed as a Minor Project | Powered by Streamlit & scikit-learn') 