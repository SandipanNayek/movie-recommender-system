
import pickle
import pandas as pd
import streamlit as st
import requests

API_KEY = "4c917d074ef6891c685c0c3748f589fd"


def fetch_poster(movie_name):
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_name}"
        data = requests.get(url, timeout=5).json()

        if data['results']:
            poster_path = data['results'][0].get('poster_path')

            if poster_path:
                return "https://image.tmdb.org/t/p/w500/" + poster_path

        return "https://via.placeholder.com/500x750.png?text=No+Image"

    except:
        return "https://via.placeholder.com/500x750.png?text=Error"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_title = movies.iloc[i[0]].title
        recommended_movies.append(movie_title)
        recommended_movies_posters.append(fetch_poster(movie_title))

    return recommended_movies, recommended_movies_posters


# Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

# Page settings
st.set_page_config(page_title="Movie Recommender System", layout="wide")

st.markdown("""
    <style>
        .stApp {
            background-color: #000000;
        }

        input {
            color: black !important;
            background-color: #ffffff !important;
            border: 2px solid red !important;
            border-radius: 8px;
        }

        input:focus {
            outline: none !important;
            box-shadow: none !important;
            border: 2px solid red !important;
        }

        div.stButton > button {
            color: white !important;
            background-color: black !important;
            border: 2px solid red !important;
            border-radius: 8px;
            font-weight: bold;
        }

        div.stButton > button:hover {
            background-color: red !important;
            color: black !important;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🎬 Movie Recommender System")

# Dropdown
selected_movie_name = st.selectbox(
    "Select a movie",
    movies['title'].values
)

# Button
if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(f"<p style='color:#ff4d4d; font-weight:bold; text-align:center;'>{names[0]}</p>", unsafe_allow_html=True)
        st.image(posters[0])

    with col2:
        st.markdown(f"<p style='color:#ff4d4d; font-weight:bold; text-align:center;'>{names[1]}</p>", unsafe_allow_html=True)
        st.image(posters[1])

    with col3:
        st.markdown(f"<p style='color:#ff4d4d; font-weight:bold; text-align:center;'>{names[2]}</p>", unsafe_allow_html=True)
        st.image(posters[2])

    with col4:
        st.markdown(f"<p style='color:#ff4d4d; font-weight:bold; text-align:center;'>{names[3]}</p>", unsafe_allow_html=True)
        st.image(posters[3])

    with col5:
        st.markdown(f"<p style='color:#ff4d4d; font-weight:bold; text-align:center;'>{names[4]}</p>", unsafe_allow_html=True)
        st.image(posters[4])