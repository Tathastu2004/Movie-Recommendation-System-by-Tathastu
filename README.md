# 🎬 Movie Recommendation System

**[👉 Try the Live App on Streamlit Cloud](https://movie-recommendation-system-by-tathastu-wayhmoxsbv6cryubndmnyh.streamlit.app/?embed_options=show_toolbar,show_padding,show_footer,show_colored_line,light_theme,dark_theme)**

A Netflix-inspired, interactive movie recommendation web app built with **Streamlit** and **scikit-learn**. Instantly get personalized movie suggestions based on your favorite titles or genres, powered by content-based filtering on the TMDb 5000 Movie Dataset.

---

## Features

- **Netflix-like UI:** Modern, responsive design with genre buttons and horizontal movie carousels.
- **Content-Based Recommendations:** Suggests similar movies using NLP and cosine similarity on movie metadata.
- **Genre Browsing:** Instantly explore movies by genre with a single click.
- **Search Functionality:** Find recommendations by movie title, genre, or keyword.
- **Movie Details:** See posters, genres, and overviews for each recommended movie.
- **Powered by TMDb:** Fetches up-to-date posters and movie info using the TMDb API.

---

## Demo

![Demo Screenshot](Demo1.png)
![Demo Screenshot](Demo2.png)
![Demo Screenshot](Demo3.png)

---

## How It Works

1. **Data Preparation:**  
   - Loads and merges `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv`.
   - Extracts and processes genres, keywords, cast, crew, and overview for each movie.
   - Creates a "tags" field for each movie by combining all relevant text features.
   - Applies stemming and vectorization (Bag-of-Words) for efficient similarity search.

2. **Recommendation Engine:**  
   - Computes cosine similarity between movies based on their tags.
   - Given a movie title, returns the top 5 most similar movies.

3. **Web App (Streamlit):**  
   - Users can search by title, genre, or keyword.
   - Genre buttons allow quick browsing.
   - Movie posters and details are fetched live from TMDb.

---

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Tathastu2004/Movie-Recommendation-System-by-Tathastu.git
   cd Movie-Recommendation-System-by-Tathastu
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file in the project root with your TMDb API credentials:**
   ```
   TMDB_API_KEY=your_tmdb_api_key_here
   TMDB_BEARER_TOKEN=your_tmdb_bearer_token_here
   ```

4. **Download the datasets:**  
   Place `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv` in the project root.  
   *(You can find these on [Kaggle TMDb 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata))*.

5. **Run the application:**
   ```bash
   streamlit run app.py
   ```

---

## Usage

- **Genre Browsing:** Click any genre button at the top to see movies in that genre.
- **Search:** Use the search box to find recommendations by movie title or genre.
- **Direct Recommendation:** Select a movie from the dropdown and click "Recommend" for similar movies.

---

## File Structure

```
.
├── app.py                  # Streamlit web app
├── movie_recommender.py    # Recommendation engine and data processing
├── requirements.txt        # Python dependencies
├── tmdb_5000_movies.csv    # Movie metadata (from Kaggle)
├── tmdb_5000_credits.csv   # Cast and crew data (from Kaggle)
├── .env                    # Environment variables (create this file)
└── Images/                 # Demo screenshots
```

---

## Technologies Used

- **Streamlit** - Web app framework
- **Pandas** - Data manipulation
- **scikit-learn** - Machine learning and similarity calculations
- **TMDb API** - Movie posters and metadata
- **Python-dotenv** - Environment variable management
- **NLTK** - Natural language processing

---

## API Keys

This app uses the TMDb API for fetching posters.  
For production or heavy use, [get your own TMDb API key](https://www.themoviedb.org/documentation/api).

**Note:** Create a `.env` file with your API credentials to keep them secure and out of version control.

---

## Acknowledgements

- [TMDb 5000 Movie Dataset (Kaggle)](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)
- [Streamlit](https://streamlit.io/)
- [scikit-learn](https://scikit-learn.org/)
- [NLTK](https://www.nltk.org/)

---

## License

This project is for educational purposes.

---

**Developed by Tathastu Mishra | Minor Project**
