# Movie Recommendation System

A Netflix-inspired movie recommendation system built with Streamlit, featuring genre-based and content-based recommendations.

## Setup Instructions

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root with your TMDb API credentials:
```
TMDB_API_KEY=your_tmdb_api_key_here
TMDB_BEARER_TOKEN=your_tmdb_bearer_token_here
```

3. Run the application:
```bash
streamlit run app.py
```

## Features

- Netflix-inspired UI with dark theme
- Genre-based movie recommendations
- Content-based movie recommendations
- Movie poster integration via TMDb API
- Responsive design with horizontal scrolling movie cards

## Technologies Used

- Streamlit
- Pandas
- scikit-learn
- TMDb API
- Python-dotenv for environment management 