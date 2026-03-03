from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests
import os

app = FastAPI()

templates = Jinja2Templates(directory="templates")

OMDB_API_KEY = os.getenv("OMDB_API_KEY")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/search")
def search(query: str):
    url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&s={query}"
    res = requests.get(url)
    return res.json().get("Search", [])

@app.get("/movie/{imdb_id}")
def movie_details(imdb_id: str):
    url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&i={imdb_id}"
    res = requests.get(url)
    return res.json()
