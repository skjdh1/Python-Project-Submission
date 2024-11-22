import requests
import pandas as pd
import random

API_KEY = "483a85091ee3808f87cc5ff0aa10a425" #custom API key
BASE_URL = "https://api.themoviedb.org/3"   # data source

def fetch_movies(genre_id=None, year=None): #fetches data from API
    url = f"{BASE_URL}/discover/movie"
    params = {                               #declaring variable
        "api_key": API_KEY,
        "sort_by": "popularity.desc",
        "with_genres": genre_id,
        "primary_release_year": year
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:             #checking if the connection is working. if not then it will output Error message
        return response.json().get("results", [])
    else:
        print("Error fetching data:", response.status_code)
        return []

def clean_data(movies): # formatting of the movies
    df = pd.DataFrame(movies)
    if not df.empty:
        df = df[["title", "release_date", "popularity", "vote_average", "overview"]]
        df["release_date"] = pd.to_datetime(df["release_date"], errors='coerce').dt.year
    return df

def filter_movies(df, year=None, min_popularity=None): #sorts by year and popularity
    if year:
        df = df[df["release_date"] == year]
    if min_popularity:
        df = df[df["popularity"] >= min_popularity]
    return df

def random_suggestion(df): # random movie suggestions
    if df.empty:
        print("No movies available for the selected criteria")
        return None
    return df.sample(1).iloc[0]

#input from users
genre_id = input("Enter Genre ID (ex: Action: 28, Comedy: 35): ")
year = input("Enter Release Year (ex: 2022, 2021, 2020): ")
popularity = input("Enter Popularity (ex: 1,2,3,4): ")

# Fetch and Process Movies
movies = fetch_movies(genre_id, year)
movie_df = clean_data(movies)

# Movie List output
filtered_df = filter_movies(movie_df, year=int(year) if year else None, min_popularity=float(popularity) if popularity else None)
print("Filtered Movies:")
print(filtered_df)

# Random Suggestion output
suggestion = random_suggestion(filtered_df)
if suggestion is not None:
    print("\nRandom Movie Suggestion:")
    print(suggestion.to_dict())
    