🎬 Movie Recommendation System Using Python and Machine Learning

A modern Movie Recommendation Web Application built using Python, FastAPI, Machine Learning, and OMDb API.

This project recommends movies based on content similarity and provides movie details with a clean Netflix-style UI.

🚀 Live Demo

👉 Deployed on Render
https://movie-recommendation-system-using-python.onrender.com/

📌 Features

🔎 Search Movies

🎥 View Movie Details (Poster, Genre, Rating, Plot)

🤖 Content-Based Recommendation System

🌐 FastAPI Backend

🎨 Modern Netflix-Style Frontend

☁️ Deployed on Render

🔐 Secure API Key using Environment Variables

🧠 Machine Learning Model

This project uses a Content-Based Filtering Algorithm.

Steps Used:

Data preprocessing

Feature extraction using:

TF-IDF Vectorization

Cosine similarity calculation

Recommend similar movies based on title input

Libraries used:

Pandas

NumPy

Scikit-learn

Pickle (for model saving)

🛠️ Tech Stack
Backend

Python

FastAPI

Uvicorn

Requests

Frontend

HTML

CSS

JavaScript (Fetch API)

Deployment

Render

API

OMDb API (Free 1000 daily requests)

📂 Project Structure
Movie-Recommendation-System-Using-Python-and-Machine-Learning/
│
├── main.py
├── requirements.txt
├── runtime.txt
├── templates/
│     └── index.html
├── model/
│     ├── tfidf_matrix.pkl
│     ├── indices.pkl
│     └── df.pkl
└── README.md
⚙️ Installation (Run Locally)
1️⃣ Clone Repository
git clone https://github.com/your-username/Movie-Recommendation-System-Using-Python-and-Machine-Learning.git
cd Movie-Recommendation-System-Using-Python-and-Machine-Learning
2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Set Environment Variable

Create .env file:

OMDB_API_KEY=your_api_key_here

OR set environment variable in terminal.

5️⃣ Run App
uvicorn main:app --reload

Open:

[http://127.0.0.1:8000](https://movie-recommendation-system-using-python.onrender.com/)
☁️ Deployment on Render

Create Web Service

Select Python 3.9

Build Command:

pip install -r requirements.txt

Start Command:

uvicorn main:app --host 0.0.0.0 --port 10000

Add Environment Variable:

OMDB_API_KEY=your_api_key_here
📊 How Recommendation Works

When a user selects a movie:

The system finds the movie index

Computes cosine similarity

Sorts similarity scores

Returns top 5 most similar movies

This ensures recommendations are based on movie content similarity.

📸 Screenshots

(Add screenshots of your app here)

🔮 Future Improvements

🎬 Add trailer integration

⭐ Add rating filters

📈 Add collaborative filtering

🧠 Deep learning-based recommendation

📊 User login and personalization

📜 License

This project is open-source and available under the MIT License.

👨‍💻 Author

Aditya Prasad
B.Tech CSE Student
Python & Machine Learning Enthusiast
