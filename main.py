import os
import requests
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Template folder
templates = Jinja2Templates(directory="templates")

# API KEY from Render Environment Variable
OMDB_API_KEY = os.getenv("OMDB_API_KEY")

if not OMDB_API_KEY:
    raise ValueError("OMDB_API_KEY not set in environment variables")

# ---------------- HOME PAGE ----------------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ---------------- SEARCH MOVIES ----------------
@app.get("/search")
def search_movies(query: str):
    try:
        url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&s={query}"
        res = requests.get(url, timeout=10)
        data = res.json()

        if data.get("Response") == "True":
            return data.get("Search", [])
        else:
            return []

    except Exception as e:
        return {"error": str(e)}


# ---------------- MOVIE DETAILS ----------------
@app.get("/movie/{imdb_id}")
def movie_details(imdb_id: str):
    try:
        url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&i={imdb_id}"
        res = requests.get(url, timeout=10)
        return res.json()

    except Exception as e:
        return {"error": str(e)}


# ---------------- RECOMMEND (Simple Demo Logic) ----------------
@app.get("/recommend")
def recommend(title: str):
    """
    Simple recommendation logic:
    It searches movies with same first word.
    Replace this with your ML model logic later.
    """
    try:
        first_word = title.split()[0]

        url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&s={first_word}"
        res = requests.get(url, timeout=10)
        data = res.json()

        if data.get("Response") == "True":
            recs = [movie["Title"] for movie in data["Search"][:5]]
            return recs
        else:
            return []

    except Exception as e:
        return {"error": str(e)}
