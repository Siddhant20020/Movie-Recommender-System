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
- Sidebar is hidden after search for clean UI.
- Supports showing multiple search results if more than one movie matches.

---



## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/Movie-Recommender-System.git
cd Movie-Recommender-System


python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt

# .streamlit/secrets.toml
TMDB_API_KEY = "your_tmdb_api_key_here"
