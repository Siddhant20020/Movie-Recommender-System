# 🎬 Movie Recommender System

A **Movie Recommender System** built with **Streamlit** and **Python**, using content-based filtering with movie similarity and TMDB API for posters. Users can search movies, filter by genre, view details, and get recommendations.

---

## Features

- Search movies by **title**.
- Filter movies by **genre**.
- View detailed movie information:
  - Poster
  - Overview
  - Genres
  - Cast
  - Director
  - Popularity score
- Get **recommended movies** based on similarity.
- Click on any recommended movie to view its details immediately.
- Sidebar is hidden after search for a clean UI.
- Supports showing multiple search results if more than one movie matches.

---

## Dataset

This project uses the [TMDB 5000 Movies and Credits datasets](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata):

1. `tmdb_5000_movies.csv` – contains movie metadata such as:
   - `title`, `genres`, `overview`, `popularity`, `vote_average`, `release_date`
2. `tmdb_5000_credits.csv` – contains cast and crew information:
   - `cast`, `crew` columns

These datasets are used to create a **movie dictionary** for similarity computation.

---

## Model / Similarity Computation

- **Feature Extraction**:
  - Combine `genres`, `keywords`, `overview`, `cast`, and `crew` into a single text feature for each movie.
  - Clean the text (lowercase, remove spaces, punctuation, etc.).
- **Vectorization**:
  - Use `CountVectorizer`  from `sklearn` to convert text features into numeric vectors.
- **Similarity Computation**:
  - Compute **cosine similarity** between all movies to generate a `similarity.pkl` file.
- **Output**:
  - `movie_dict.pkl` – dictionary containing all movie metadata for fast lookup.
  - `similarity.pkl` – precomputed similarity matrix for recommendations.

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Siddhant20020/Movie-Recommender-System.git cd Movie-Recommender-System

# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

TMDB_API_KEY = "your_tmdb_api_key_here"
Datasets / Model Files

tmdb_5000_movies.csv

tmdb_5000_credits.csv

movie_dict.pkl – preprocessed movie dictionary

similarity.pkl – precomputed similarity matrix (~176 MB)

You can download similarity.pkl here:

Download similarity.pkl
https://drive.google.com/file/d/1S3xg2thVGLdjAiE_9oSDaFC_kZ5wB8og/view?usp=sharing
Important: Since similarity.pkl is large (~176 MB), GitHub LFS is required to track it if you push to a repository.

