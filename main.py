import os
import requests
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

OMDB_API_KEY = os.getenv("OMDB_API_KEY")

if not OMDB_API_KEY:
    raise ValueError("OMDB_API_KEY not set in environment variables")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/popular")
def popular_movies():
    try:
        url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&s=avengers"
        res = requests.get(url, timeout=10)
        data = res.json()

        if data.get("Response") == "True":
            return data.get("Search", [])
        return []

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/search")
def search_movies(query: str):
    try:
        url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&s={query}"
        res = requests.get(url, timeout=10)
        data = res.json()

        if data.get("Response") == "True":
            return data.get("Search", [])
        return []

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/movie/{imdb_id}")
def movie_details(imdb_id: str):
    try:
        url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&i={imdb_id}"
        res = requests.get(url, timeout=10)
        return res.json()

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/recommend")
def recommend(title: str):
    try:
        first_word = title.split()[0]
        url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&s={first_word}"
        res = requests.get(url, timeout=10)
        data = res.json()

        if data.get("Response") == "True":
            return [movie["Title"] for movie in data["Search"][:5]]
        return []

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
