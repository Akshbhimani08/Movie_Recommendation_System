# Movie Recommendation System

> **Content-based movie recommender powered by sentence embeddings and cosine similarity, with a Streamlit web interface and live TMDB poster integration.**

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-F7931E?logo=scikit-learn&logoColor=white)
![TMDB](https://img.shields.io/badge/TMDB-API-01B4E4?logo=themoviedatabase&logoColor=white)

---

## Overview

This project implements a **content-based filtering** recommendation engine that suggests movies similar to a user-selected title. Movie metadata is encoded into dense vector embeddings, and **cosine similarity** is used to rank and return the most semantically related films. A live Streamlit interface displays results as a visual poster grid enriched with metadata.

---

## Features

- 🔍 **Embedding-based similarity** — tag/metadata vectors captured via sentence embeddings for richer semantic matching than keyword overlap
- 🎞️ **Live poster fetching** — real-time TMDB API integration with graceful fallback for missing/unavailable images
- ⚡ **Cached API calls** — `@st.cache_data` prevents redundant network requests and speeds up repeated lookups
- 🔁 **Resilient HTTP layer** — automatic retry with exponential backoff for transient API failures (429, 5xx)
- 🎛️ **Configurable results** — users choose how many recommendations to display (1–20)
- 📱 **Responsive grid layout** — results rendered in a 3-column card grid with title, release year, and tags

---

## Demo

| Select a Movie | Get Recommendations |
|:--------------:|:-------------------:|
| Dropdown with full movie catalog | Poster grid with title, year, and tags |

---

## Project Structure

```
Movie_Recommendation_System/
├── app.py                  # Streamlit web app (UI + recommendation logic)
├── movies.pkl              # Serialized movie metadata DataFrame
├── embeddings.pkl          # Precomputed sentence embeddings (numpy array)
├── no-image.jpg            # Fallback poster for unavailable images
├── requirements.txt        # Python dependencies
└── .python-version         # Python version pin
```

---

## How It Works

```
User selects a movie
        │
        ▼
Look up precomputed embedding for selected movie
        │
        ▼
Compute cosine similarity against all movie embeddings
        │
        ▼
Return top-N most similar movies (excluding self)
        │
        ▼
Fetch poster images from TMDB API
        │
        ▼
Render recommendation cards in Streamlit UI
```

### Key Algorithm

```python
# Cosine similarity between selected movie and entire corpus
scores = cosine_similarity(movie_embedding, embeddings)[0]

# Rank by descending similarity, skip index 0 (the movie itself)
top_indices = np.argsort(scores)[::-1][1:top_n+1]
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- [TMDB API Key](https://developer.themoviedb.org/docs) (free)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Akshbhimani08/Movie_Recommendation_System.git
cd Movie_Recommendation_System

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your TMDB API key as an environment variable
export TMDB_API_KEY=your_api_key_here      # Linux / macOS
set TMDB_API_KEY=your_api_key_here         # Windows CMD

# 4. Run the app
streamlit run app.py
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend / UI** | Streamlit |
| **Similarity Engine** | scikit-learn (`cosine_similarity`) |
| **Numerical Computing** | NumPy, Pandas |
| **Data Serialization** | Pickle |
| **Poster API** | TMDB REST API |
| **HTTP Resilience** | `requests` + `urllib3` Retry |

---

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `top_n` | 5 | Number of recommendations returned |
| `min_value` | 1 | Minimum selectable recommendations |
| `max_value` | 20 | Maximum selectable recommendations |
| `timeout` | 5s | TMDB API request timeout |
| `total retries` | 3 | Max retry attempts on API failure |

API key is loaded via the `TMDB_API_KEY` environment variable — never hardcoded.

---

## Roadmap

- [ ] Switch from pickle embeddings to a vector database (e.g., FAISS, ChromaDB) for scalability
- [ ] Add collaborative filtering for hybrid recommendations
- [ ] User ratings and watch history persistence
- [ ] Deploy to Streamlit Community Cloud / Hugging Face Spaces
- [ ] Support for TV shows and anime via extended TMDB endpoints

---

*Built with Python, scikit-learn, and Streamlit.*
