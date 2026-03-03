import os
import pickle
from typing import Optional, List, Dict, Any, Tuple

import numpy as np
import pandas as pd
import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv



load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")

if not OMDB_API_KEY:
    raise RuntimeError("OMDB_API_KEY missing in .env")

OMDB_BASE = "http://www.omdbapi.com/"



app = FastAPI(title="Movie Recommender API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DF_PATH = os.path.join(BASE_DIR, "df.pkl")
INDICES_PATH = os.path.join(BASE_DIR, "indices.pkl")
TFIDF_MATRIX_PATH = os.path.join(BASE_DIR, "tfidf_matrix.pkl")

df = None
TITLE_TO_IDX = None
tfidf_matrix = None


@app.on_event("startup")
def load_pickles():
    global df, TITLE_TO_IDX, tfidf_matrix

    with open(DF_PATH, "rb") as f:
        df = pickle.load(f)

    with open(INDICES_PATH, "rb") as f:
        indices = pickle.load(f)

    with open(TFIDF_MATRIX_PATH, "rb") as f:
        tfidf_matrix = pickle.load(f)

    TITLE_TO_IDX = {str(k).lower(): int(v) for k, v in indices.items()}



class MovieCard(BaseModel):
    imdb_id: str
    title: str
    year: Optional[str] = None
    poster: Optional[str] = None



async def omdb_get(params: dict):
    params["apikey"] = OMDB_API_KEY

    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(OMDB_BASE, params=params)

    if r.status_code != 200:
        raise HTTPException(status_code=502, detail="OMDb error")

    return r.json()



@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/search", response_model=List[MovieCard])
async def search(query: str = Query(...)):
    data = await omdb_get({"s": query})

    if data.get("Response") == "False":
        return []

    return [
        MovieCard(
            imdb_id=m["imdbID"],
            title=m["Title"],
            year=m.get("Year"),
            poster=m.get("Poster"),
        )
        for m in data.get("Search", [])
    ]


@app.get("/movie/{imdb_id}")
async def movie_details(imdb_id: str):
    data = await omdb_get({"i": imdb_id, "plot": "full"})

    if data.get("Response") == "False":
        raise HTTPException(status_code=404, detail="Movie not found")

    return data


@app.get("/recommend")
async def recommend(title: str = Query(...), top_n: int = 8):
    title_key = title.lower()

    if title_key not in TITLE_TO_IDX:
        return []

    idx = TITLE_TO_IDX[title_key]
    qv = tfidf_matrix[idx]
    scores = (tfidf_matrix @ qv.T).toarray().ravel()

    order = np.argsort(-scores)
    results = []

    for i in order:
        if i == idx:
            continue

        movie_title = df.iloc[int(i)]["title"]
        results.append({"title": movie_title})

        if len(results) >= top_n:
            break

    return results