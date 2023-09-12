import streamlit as st
import pandas as pd
import pickle
import requests
api_key = '8265bd1679663a7ea12ac168da84d2e8'
def fetch_poster(movie_id):

    url = "https://api.themoviedb.org/3/movie/{}?language=en-US".format(movie_id)
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3NThhZjQ3MTgwOTc0Mzc3YjFkMDEwNmIzOGYzNTMyZSIsInN1YiI6IjY0ZmY4OWM1ZWZlYTdhMDEzN2QxZWEyYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.PCgsWjSpgOcng6VKxEIgUocIsichJGemdyUJr0siAXA"
    }

    response = requests.get(url, headers=headers).json()

    if 'success' in response:
        path = "https://d32qys9a6wm9no.cloudfront.net/images/others/not_available/poster_500x735.png?t=1694458990"
    else:
        path = "https://image.tmdb.org/t/p/original/" + response["poster_path"]
    return path
data = pd.read_csv("data.csv")
vectors = pickle.load(open('similarity.pkl','rb'))

def get_sim_movies(name):
  ind = data[data['original_title'] == name].index[0]
  recom_ind = sorted(list(enumerate(vectors[ind])),key=lambda x:-x[1])[1:6]
  req_list = []
  poster = []
  for i in recom_ind:
    req_list.append(data['original_title'][i[0]])
    poster.append(fetch_poster(data['id'][i[0]]))
  return req_list,poster


st.title("Movie Recommender System")
selected_movie = st.selectbox(
    'Select a movie...',
     (data['original_title'].values))
if st.button('Recommend'):
    movie,poster = get_sim_movies(selected_movie)
    col = st.columns(5)
    for i in range(5):
        with col[i]:
            st.text(movie[i])
            st.image(poster[i])
