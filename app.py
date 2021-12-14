import pickle
import streamlit as st
import requests


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    for i in distances[1:6]:
        # fetch the movie poster
        #movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names


st.header('Bangla Movie Recommendation System')
movies = pickle.load(open(r'C:\Users\USER\Desktop\Bangla-Movie-Recommendation-System\movie_list.pkl','rb'))
similarity = pickle.load(open(r'C:\Users\USER\Desktop\Bangla-Movie-Recommendation-System\similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    st.header('Top 5 recommended movies:')
    recommended_movie_names = recommend(selected_movie)
    col1, col2 = st.columns(2)
    with col1:
        st.text(recommended_movie_names[0])
    with col2:
        st.text(recommended_movie_names[1])

    with col1:
        st.text(recommended_movie_names[2])
    with col2:
        st.text(recommended_movie_names[3])
    with col1:
        st.text(recommended_movie_names[4])
