import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
import pickle
import requests
import json
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

movies_list=pickle.load(open("movies.pkl","rb"))
movies_list=pd.DataFrame(movies_list)
embeddings=pickle.load(open("embeddings.pkl","rb"))

def movie_id_helper(movie):
    return movies_list[movies_list["title"]==movie].index[0]


session = requests.Session()

retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
)

adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)
session.mount("http://", adapter)


@st.cache_data(show_spinner=False)
def movie_poster(title):

    default_image = "no-image.jpg"

    try:
        url = "https://api.themoviedb.org/3/search/movie"

        params = {
            "api_key": "469ff5f10c3bf122ecf3f5922da1f4ab",
            "query": title
        }

        response = session.get(
            url,
            params=params,
            timeout=5
        )

        # If API limit exceeded
        if response.status_code != 200:
            return default_image

        data = response.json()

        if not data.get("results"):
            return default_image

        poster_path = data["results"][0].get("poster_path")

        if not poster_path:
            return default_image

        return "https://image.tmdb.org/t/p/w500" + poster_path

    except requests.exceptions.ConnectionError:
        return default_image

    except requests.exceptions.Timeout:
        return default_image

    except requests.exceptions.RequestException:
        return default_image

    except Exception:
        return default_image



def recommendation(movie, top_n=5):
    idx = movies_list[movies_list["title"]==movie].index[0]

    movie_embedding = embeddings[idx].reshape(1, -1)
    
    scores = cosine_similarity(movie_embedding, embeddings)[0]
    
    top_indices = np.argsort(scores)[::-1][1:top_n+1]
    
    return movies_list.iloc[top_indices][["title", "release_year","tags"]].values



st.title("Movie Recommendation System")

option1=st.selectbox("Choose the Movie that for you need the recommendation : ",movies_list["title"].values)
option2=st.number_input("Choose no. of recommendation : ", min_value=1, max_value=20, value="min", step=None, format=None)


if st.button("Recommend"):

    details_arr = recommendation(option1, option2)

    default_image = "no-image.webp"

    for row_start in range(0, option2, 3):

        cols = st.columns(3)

        for col_index in range(3):

            if row_start + col_index < option2:

                i = row_start + col_index

                with cols[col_index]:

                    poster_url = movie_poster(details_arr[i][0])

                    # Use default image if poster not found
                    if poster_url:
                        st.image(poster_url, use_container_width=True)
                    else:
                        st.image(default_image, use_container_width=True)

                    # Card container
                    st.markdown(
                        f"""
                        <div style="
                            border:1px solid #2E4053;
                            padding:15px;
                            border-radius:10px;
                            min-height:200px;
                            margin-bottom:20px;
                        ">
                            <h4 style="margin-bottom:8px;">{i+1}. {details_arr[i][0]}</h4>
                            <p style="margin:4px;"><b>Release Year:</b> {details_arr[i][1]}</p>
                            <p style="margin:4px;"><b>Tags:</b> {details_arr[i][2]}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                                    