import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title']== movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_movie_posters = []
    for i in movies_list:
        
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movie_posters.append(fetch_poster(movies.iloc[i[0]].movie_id))
    return recommended_movies, recommended_movie_posters 



movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict) 

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox('Select Movie to get Recommendations', movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    
    
    cols = st.columns(5)

    for i, col in enumerate(cols):
       with col:
          st.text(names[i])
          st.image(posters[i])
