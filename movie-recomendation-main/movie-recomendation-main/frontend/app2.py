import streamlit as st
import requests

BACKEND_URL = "http://localhost:5000"
st.markdown("""
    <style>
    /* Center title */
    .css-10trblm {
        text-align: center;
    }

    /* Search Box Styling */
    .stTextInput > div > div > input {
        border: 2px solid #555 !important;
        border-radius: 12px;
        padding: 10px;
        font-size: 18px;
    }

    /* Dropdown styling */
    .stSelectbox > div > div {
        border-radius: 12px;
    }

    /* Movie cards */
    .movie-card {
        background-color: #1e1e1e;
        padding: 15px;
        border-radius: 12px;
        margin: 10px 0px;
        border: 1px solid #444;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎬 Movie Recommendation System")

mode = st.sidebar.selectbox(
    "Select an action",
    ["Register User", "Search Movie", "Add Watched Movie", "Get Recommendations"]
)

st.write(f"### Selected: {mode}")
if mode == "Register User":
    st.subheader("Register a New User")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        response = requests.post(f"{BACKEND_URL}/user/register", json={
            "username": username,
            "email": email,
            "password": password
        })

        if response.status_code == 201:
            st.success("User registered successfully!")
            st.json(response.json())
        else:
            st.error(response.json().get("error", "Unknown error"))


elif mode == "Search Movie":
    st.subheader("🔍 Search Movies")
    prefix = st.text_input("Start typing...", placeholder="Type a movie name...")

    if prefix.strip():
        with st.spinner("Searching..."):
            response = requests.get(f"{BACKEND_URL}/search/autocomplete?prefix={prefix}")
            suggestions = response.json().get("suggestions", [])

        if suggestions:
            selected = st.selectbox("Suggestions", suggestions)

            st.markdown(f"""
                <div class="movie-card">
                <h3>🎬 {selected}</h3>
                <p>Click the next tab to mark this movie as watched.</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("No suggestions found.")


elif mode == "Add Watched Movie":
    st.subheader("📺 Add a Movie to Watched List")

    col1, col2 = st.columns(2)

    with col1:
        user_id = st.number_input("User ID", min_value=1, step=1)

    with col2:
        movie_id = st.number_input("Movie ID", min_value=1, step=1)

    rating = st.slider("Your Rating", 1, 10)

    if st.button("Add", use_container_width=True):
        with st.spinner("Updating..."):
            response = requests.post(f"{BACKEND_URL}/user/watched", json={
                "user_id": user_id,
                "movie_id": movie_id,
                "rating": rating
            })

        if response.status_code == 200:
            st.success("Movie added to watched list ✔")
        else:
            st.error(response.json().get("error", "Unknown error"))

elif mode == "Get Recommendations":
    st.subheader("🎯 Personalized Movie Recommendations")

    user_id = st.number_input("Enter User ID", min_value=1, step=1)

    if st.button("Show Recommendations", use_container_width=True):
        with st.spinner("Generating..."):
            response = requests.get(f"{BACKEND_URL}/recommend/{user_id}")
            movies = response.json().get("movies", [])

        if movies:
            st.write("### 🎥 Recommended for You:")
            for title in movies:
                st.markdown(f"""
                    <div class="movie-card">
                        <h3>⭐ {title}</h3>
                        <p>Recommended based on your watched history.</p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No recommendations available.")
