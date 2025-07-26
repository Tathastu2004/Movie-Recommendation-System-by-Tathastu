import ast
import pandas as pd
import numpy as np
import nltk
nltk.download('punkt')
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 1. Load datasets
movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')

# 2. Merge on 'title'
data = movies.merge(credits, left_on='title', right_on='title')

# 3. Select relevant features
df = data[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]

# 4. Drop rows with missing values
df.dropna(inplace=True)

# 5. Helper functions to parse stringified lists/dicts
def parse_names(text):
    try:
        return [i['name'] for i in ast.literal_eval(text)]
    except Exception:
        return []

def parse_cast(text):
    try:
        return [i['name'] for i in ast.literal_eval(text)][:3]  # Top 3 cast
    except Exception:
        return []

def parse_director(text):
    try:
        return [i['name'] for i in ast.literal_eval(text) if i.get('job') == 'Director']
    except Exception:
        return []

# 6. Apply parsing functions
df['genres'] = df['genres'].apply(parse_names)
df['keywords'] = df['keywords'].apply(parse_names)
df['cast'] = df['cast'].apply(parse_cast)
df['crew'] = df['crew'].apply(parse_director)

# 7. Preprocess overview (split into words)
df['overview'] = df['overview'].apply(lambda x: x.split())

# 8. Create 'tags' feature
df['tags'] = df['overview'] + df['genres'] + df['keywords'] + df['cast'] + df['crew']
df['tags'] = df['tags'].apply(lambda x: ' '.join(x))

# 9. Text preprocessing (stemming, lowercasing)
ps = PorterStemmer()
def text_preprocess(text):
    return ' '.join([ps.stem(i.lower()) for i in text.split()])

df['tags'] = df['tags'].apply(text_preprocess)

# 10. Final dataframe for recommendation
final_data = df[['movie_id', 'title', 'tags']]
print('Final DataFrame Overview:')
print(final_data.head())

# 11. BOW encoding
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(final_data['tags']).toarray()

# 12. Cosine similarity
similarity = cosine_similarity(vectors)

# 13. Recommendation function
def recommend(movie_title):
    if movie_title not in final_data['title'].values:
        return []
    idx = final_data[final_data['title'] == movie_title].index[0]
    distances = similarity[idx]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    return [final_data.iloc[i[0]].title for i in movie_list]

def get_movie_overview_and_genres(title):
    row = data[data['title'] == title]
    if row.empty:
        return '', []
    overview = row.iloc[0]['overview']
    genres = [g['name'] for g in ast.literal_eval(row.iloc[0]['genres'])]
    return overview, genres

# Example usage:
# recommend('Avatar') 
