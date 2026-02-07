import streamlit as st
import pickle
import pandas as pd
import requests
import os

st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

TMDB_API_KEY = st.secrets.get("TMDB_API_KEY", "")
FALLBACK_IMAGE = "cover-not-found.jpg"
POSTER_FOLDER = "posters"

@st.cache_data
def load_data():
    movie_dict = pickle.load(open("movie_dict.pkl", "rb"))
    similarity = pickle.load(open("similarity.pkl", "rb"))
    df = pd.DataFrame(movie_dict).fillna("")
    if 'genres' not in df.columns:
        df['genres'] = [[] for _ in range(len(df))]
    return df, similarity

movies, similarity = load_data()
movies['popularity_score'] = similarity.sum(axis=1)

def fetch_poster_local(movie_id):
    if not os.path.exists(POSTER_FOLDER):
        os.makedirs(POSTER_FOLDER)
    local_path = os.path.join(POSTER_FOLDER, f"{movie_id}.jpg")
    if os.path.exists(local_path):
        return local_path
    elif os.path.exists(FALLBACK_IMAGE):
        return FALLBACK_IMAGE
    else:
        return "https://via.placeholder.com/300x450?text=No+Image"

@st.cache_data
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}"
        params = {"api_key": TMDB_API_KEY, "language": "en-US"}
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        poster_path = response.json().get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    except Exception:
        pass
    return fetch_poster_local(movie_id)

def recommend(movie_title, n=10, genre=None):
    if movie_title not in movies['title'].values:
        return [], [], []
    filtered = movies[movies['genres'].apply(lambda x: genre in x)] if genre and genre != "All" else movies
    idx = filtered[filtered['title'] == movie_title].index[0]
    distances = similarity[idx]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:n+1]
    names, ids = [], []
    for i in movies_list:
        names.append(filtered.iloc[i[0]]["title"])
        ids.append(filtered.iloc[i[0]]["movie_id"])
    posters = [fetch_poster(mid) for mid in ids]
    return names, posters, ids

def movie_card(name, poster, movie_id, section=""):
    st.markdown(f"""
    <div class="movie-card">
        <img src="{poster}" style="width:150px;height:220px;border-radius:10px;object-fit:cover;">
        <p style="font-size:14px;margin:2px 0;"><b>{name}</b></p>
    </div>
    """, unsafe_allow_html=True)

    btn_key = f"{section}_{movie_id}"
    if st.button("View Details", key=btn_key):
        st.session_state.current_movie = movie_id
        st.session_state.page = "detail"

def show_movie_section(title, movie_list):
    st.subheader(title)
    cols = st.columns(5)
    for i, (name, poster, mid) in enumerate(movie_list):
        with cols[i % 5]:
            movie_card(name, poster, mid, section=title)

st.session_state.setdefault("page", "home")
st.session_state.setdefault("current_movie", None)
st.session_state.setdefault("search_results", [])

def home():
    st.title("🎬 Movie Recommender")

    with st.sidebar:
        st.header("Search & Filter")
        query = st.text_input("Search a movie by name:")
        all_genres = sorted({g for sublist in movies['genres'] for g in sublist})
        genre = st.selectbox("Or pick a genre:", ["All"] + all_genres)
        search = st.button("🔍 Search")

    if search and query:
        matches = movies[movies['title'].str.contains(query, case=False)]
        if not matches.empty:
            # Directly show the first match's details
            st.session_state.current_movie = matches.iloc[0]['movie_id']
            st.session_state.page = "detail"

    if st.session_state.page == "detail":
        detail()
        return

    if st.session_state.search_results:
        st.subheader("Recommended Movies")
        cols = st.columns(4)
        for i, (name, poster, mid) in enumerate(st.session_state.search_results):
            with cols[i % 4]:
                movie_card(name, poster, mid, section="search")
    else:
        top = movies.sort_values("popularity_score", ascending=False).head(10)
        top_list = list(zip(top['title'], [fetch_poster(mid) for mid in top['movie_id']], top['movie_id']))
       
        genres = sorted({g for sublist in movies['genres'] for g in sublist})
        for g in genres[:6]:
            genre_movies = movies[movies['genres'].apply(lambda x: g in x)].sort_values("popularity_score", ascending=False).head(8)
            genre_list = list(zip(genre_movies['title'], [fetch_poster(mid) for mid in genre_movies['movie_id']], genre_movies['movie_id']))
            show_movie_section(f"🎬 Popular in {g}", genre_list)

def detail():
    movie_id = st.session_state.current_movie
    if movie_id is None:
        movie_row = movies.sample(1).iloc[0]
        movie_id = movie_row["movie_id"]
    else:
        movie_row = movies[movies['movie_id'] == movie_id].iloc[0]

    if st.button("⬅ Back"):
        st.session_state.page = "home"
        st.session_state.current_movie = None

    st.header(movie_row["title"])
    st.image(fetch_poster(movie_id), width=250)
    st.subheader("🎬 Movie Details")  
    st.markdown(f"**Overview:** {' '.join(movie_row.get('overview', [])) if movie_row.get('overview') else 'N/A'}")
    st.markdown(f"**Genres:** {', '.join(movie_row.get('genres', [])) if movie_row.get('genres') else 'N/A'}")
    st.markdown(f"**Cast:** {', '.join(movie_row.get('cast', [])) if movie_row.get('cast') else 'N/A'}")
    st.markdown(f"**Director:** {', '.join(movie_row.get('crew', [])) if movie_row.get('crew') else 'N/A'}")
    st.markdown(f"**Popularity Score:** {movie_row.get('popularity_score', 0):.2f}")

    names, posters, ids = recommend(movie_row["title"], n=10)
    if names:
        st.subheader("🍿 You may also like")
        cols = st.columns(5)
        for i, (name, poster, mid) in enumerate(zip(names, posters, ids)):
            with cols[i % 5]:
                movie_card(name, poster, mid, section="recommendation")

if st.session_state.page == "home":
    home()
else:
    detail()
