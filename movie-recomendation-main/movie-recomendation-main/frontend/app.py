import streamlit as st
import requests

BACKEND_URL = "http://localhost:5000"

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
    st.subheader("Search for Movies (Autocomplete)")

    prefix = st.text_input("Start typing movie name")

    if prefix.strip():
        response = requests.get(f"{BACKEND_URL}/search/autautocomplete?prefix={prefix}")
        data = response.json()
        suggestions = data.get("suggestions", [])

        if suggestions:
            selected = st.selectbox("Suggestions", suggestions)
            st.write(f"### You selected: **{selected}**")
        else:
            st.info("No suggestions found.")


elif mode == "Add Watched Movie":
    st.subheader("Add a Movie to Watched List")
    user_id = st.number_input("User ID", min_value=1, step=1)
    movie_id = st.number_input("Movie ID", min_value=1, step=1)
    rating = st.number_input("Your Rating (1–10)", min_value=1, max_value=10, step=1)

    if st.button("Add Watched Movie"):
        response = requests.post(f"{BACKEND_URL}/user/watched", json={
            "user_id": user_id,
            "movie_id": movie_id,
            "rating": rating
        })

        if response.status_code == 200:
            st.success("Movie added to watched list!")
        else:
            st.error(response.json().get("error", "Unknown error"))


elif mode == "Get Recommendations":
    st.subheader("Get Movie Recommendations")
    user_id = st.number_input("User ID", min_value=1, step=1)

    if st.button("Get Recommendations"):
        response = requests.get(f"{BACKEND_URL}/recommend/{user_id}")
        movies = response.json().get("movies", [])

        if movies:
            st.write("### Recommended Movies:")
            for title in movies:
                st.write(f"- **{title}**")
        else:
            st.warning("No recommendations available.")
