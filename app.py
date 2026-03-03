import streamlit as st
import requests

# 🔥 CHANGE AFTER DEPLOYMENT
BACKEND_URL = "https://your-backend-name.onrender.com"

st.set_page_config(
    page_title="Netflix Style Recommender",
    page_icon="🎬",
    layout="wide"
)


st.markdown("""
<style>
body {
    background-color: #141414;
}
.main {
    background-color: #141414;
}
h1, h2, h3, h4 {
    color: white;
}
.movie-card {
    transition: transform 0.3s ease;
}
.movie-card:hover {
    transform: scale(1.08);
}
.stButton>button {
    background-color: #E50914;
    color: white;
    border-radius: 5px;
    border: none;
}
</style>
""", unsafe_allow_html=True)


st.markdown("<h1 style='color:#E50914;'>🎬 Movie Recommender</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:white;'>Discover movies Netflix-style</p>", unsafe_allow_html=True)


query = st.text_input("Search for a movie")

if query:
    with st.spinner("Searching..."):
        try:
            res = requests.get(
                f"{BACKEND_URL}/search",
                params={"query": query},
                timeout=10,
            )
        except:
            st.error("Backend not running.")
            st.stop()

    movies = res.json()

    if not movies:
        st.warning("No movies found.")
    else:
        st.markdown("## 🎥 Search Results")

        cols = st.columns(5)

        for i, movie in enumerate(movies):
            with cols[i % 5]:
                st.markdown("<div class='movie-card'>", unsafe_allow_html=True)

                if movie.get("Poster") and movie["Poster"] != "N/A":
                    st.image(movie["Poster"], use_column_width=True)

                st.markdown(
                    f"<p style='color:white; text-align:center;'><b>{movie['Title']}</b></p>",
                    unsafe_allow_html=True
                )

                if st.button("View", key=movie["imdbID"]):
                    details = requests.get(
                        f"{BACKEND_URL}/movie",
                        params={"imdb_id": movie["imdbID"]},
                        timeout=10,
                    ).json()

                    st.markdown("---")
                    st.markdown(
                        f"<h2 style='color:white;'>{details.get('Title')}</h2>",
                        unsafe_allow_html=True
                    )

                    col1, col2 = st.columns([1, 2])

                    with col1:
                        if details.get("Poster") != "N/A":
                            st.image(details["Poster"])

                    with col2:
                        st.markdown(f"<p style='color:white;'>⭐ IMDb: {details.get('imdbRating')}</p>", unsafe_allow_html=True)
                        st.markdown(f"<p style='color:white;'>📅 Year: {details.get('Year')}</p>", unsafe_allow_html=True)
                        st.markdown(f"<p style='color:white;'>🎭 Genre: {details.get('Genre')}</p>", unsafe_allow_html=True)
                        st.markdown(f"<p style='color:white;'>📝 {details.get('Plot')}</p>", unsafe_allow_html=True)

                    st.markdown("## 🤖 Recommended For You")

                    recs = requests.get(
                        f"{BACKEND_URL}/recommend",
                        params={"title": details.get("Title")},
                        timeout=10,
                    ).json()

                    rec_cols = st.columns(5)

                    for j, rec in enumerate(recs):
                        with rec_cols[j % 5]:
                            st.markdown(
                                f"<p style='color:white; text-align:center;'>{rec}</p>",
                                unsafe_allow_html=True
                            )

                st.markdown("</div>", unsafe_allow_html=True)