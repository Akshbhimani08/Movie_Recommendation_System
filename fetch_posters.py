import requests
import pandas as pd
import pickle
import time

API_KEY = "469ff5f10c3bf122ecf3f5922da1f4ab"

def fetch_poster(title):
    url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": API_KEY,
        "query": title
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        if data.get("results"):
            poster_path = data["results"][0].get("poster_path")
            if poster_path:
                return "https://image.tmdb.org/t/p/w500" + poster_path

        return None

    except:
        return None


# Load your existing pickle file
movies = pickle.load(open("movies.pkl", "rb"))
movies = pd.DataFrame(movies)

posters = []

print("Fetching posters...")

for title in movies["title"]:
    poster_url = fetch_poster(title)
    posters.append(poster_url)

    time.sleep(0.3)   # VERY IMPORTANT → avoids rate limit

movies["poster_url"] = posters

# Save new file
pickle.dump(movies, open("movies_with_posters.pkl", "wb"))

print("Done! New file saved as movies_with_posters.pkl")
