from flask import Flask, render_template, request
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__)

with open('../model/movie_recommender.pkl', 'rb') as f:
    model_artifacts = pickle.load(f)

data = model_artifacts['data']
cosine_sim = model_artifacts['cosine_sim']

data['Rating_clean'] = pd.to_numeric(data.get('Rating_clean'), errors='coerce').fillna(0)

if 'Votes_clean' in data.columns:
    data['Votes_clean'] = pd.to_numeric(data['Votes_clean'], errors='coerce').fillna(0)

if 'Duration_minutes' in data.columns:
    data['Duration_minutes'] = pd.to_numeric(data['Duration_minutes'], errors='coerce').fillna(0)


def get_recommendations(title, top_n=12):
    movie_titles = data['Title'].str.lower().tolist()
    title_lower = title.lower()

    if title_lower not in movie_titles:
        return []

    idx = data[data['Title'].str.lower() == title_lower].index[0]

    max_idx = len(cosine_sim) - 1

    if idx > max_idx:
        idx = idx % len(cosine_sim)

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    top_indices = [i[0] for i in sim_scores[1:top_n+1]]

    results = []
    for i, movie_idx in enumerate(top_indices):

        if movie_idx >= len(data):
            continue

        row = data.iloc[movie_idx]

        results.append({
            'title': row.get('Title', 'Unknown'),
            'genres': row.get('Genres', 'Unknown') if pd.notna(row.get('Genres')) else 'Unknown',
            'rating': round(row.get('Rating_clean', 0), 1),
            'duration': int(row.get('Duration_minutes', 0)),
            'director': row.get('Directed by', 'Unknown'),
            'similarity': round(sim_scores[i+1][1], 3)
        })

    return results


def get_movies_by_genre(genre, limit=24):
    """Get top movies in a specific genre."""
    genre_mask = data['Genres'].astype(str).str.contains(genre, case=False, na=False)
    genre_movies = data[genre_mask].copy()

    if 'popularity_score' in genre_movies.columns:
        genre_movies = genre_movies.sort_values('popularity_score', ascending=False)
    elif 'Votes_clean' in genre_movies.columns:
        genre_movies = genre_movies.sort_values('Votes_clean', ascending=False)

    results = []
    for _, row in genre_movies.head(limit).iterrows():
        results.append({
            'title': row.get('Title', 'Unknown'),
            'genres': row.get('Genres', 'Unknown') if pd.notna(row.get('Genres')) else 'Unknown',
            'rating': round(row.get('Rating_clean', 0), 1),
            'duration': int(row.get('Duration_minutes', 0)),
            'director': row.get('Directed by', 'Unknown')
        })

    return results


def search_movies(query, limit=24):
    """Search movies by keyword."""
    query_lower = query.lower()

    title_mask = data['Title'].str.lower().str.contains(query_lower, na=False)
    desc_mask = data['Description'].astype(str).str.lower().str.contains(query_lower, na=False)
    director_mask = data['Directed by'].astype(str).str.lower().str.contains(query_lower, na=False)

    results_df = data[title_mask | desc_mask | director_mask].copy()

    if 'popularity_score' in results_df.columns:
        results_df = results_df.sort_values('popularity_score', ascending=False)
    elif 'Votes_clean' in results_df.columns:
        results_df = results_df.sort_values('Votes_clean', ascending=False)

    results = []
    for _, row in results_df.head(limit).iterrows():
        results.append({
            'title': row.get('Title', 'Unknown'),
            'genres': row.get('Genres', 'Unknown') if pd.notna(row.get('Genres')) else 'Unknown',
            'rating': round(row.get('Rating_clean', 0), 1),
            'duration': int(row.get('Duration_minutes', 0)),
            'director': row.get('Directed by', 'Unknown')
        })

    return results


def get_popular_movies(limit=12):
    """Get most popular movies."""
    if 'popularity_score' in data.columns:
        popular = data.sort_values('popularity_score', ascending=False)
    elif 'Votes_clean' in data.columns:
        popular = data.sort_values('Votes_clean', ascending=False)
    else:
        popular = data.sample(min(limit, len(data)))

    results = []
    for _, row in popular.head(limit).iterrows():
        results.append({
            'title': row.get('Title', 'Unknown'),
            'genres': row.get('Genres', 'Unknown') if pd.notna(row.get('Genres')) else 'Unknown',
            'rating': round(row.get('Rating_clean', 0), 1),
            'duration': int(row.get('Duration_minutes', 0)),
            'director': row.get('Directed by', 'Unknown')
        })

    return results


def get_all_movie_titles():
    """Get all movie titles for the dropdown."""
    return data['Title'].sort_values().tolist()


@app.route('/')
def index():
    popular_movies = get_popular_movies(12)
    all_movies = get_all_movie_titles()
    return render_template('index.html', popular_movies=popular_movies, all_movies=all_movies)


@app.route('/recommend')
def recommend():
    title = request.args.get('title', '')

    if not title:
        return render_template('index.html',
                               error="Please select a movie",
                               popular_movies=get_popular_movies(12),
                               all_movies=get_all_movie_titles())

    if title.startswith("#"):
        genre = title.replace("#", "")
        movies = get_movies_by_genre(genre)
        return render_template('genre.html',
                               genre=genre,
                               movies=movies,
                               all_movies=get_all_movie_titles())

    recommendations = get_recommendations(title)

    if not recommendations:
        return render_template('index.html',
                               error=f'Movie "{title}" not found.',
                               popular_movies=get_popular_movies(12),
                               all_movies=get_all_movie_titles())

    return render_template('recommendations.html',
                           movie_title=title,
                           recommendations=recommendations,
                           all_movies=get_all_movie_titles())


@app.route('/genre/<genre>')
def genre_page(genre):
    movies = get_movies_by_genre(genre, 24)
    return render_template('genre.html', genre=genre, movies=movies, all_movies=get_all_movie_titles())


@app.route('/search')
def search_page():
    query = request.args.get('q', '')

    if not query:
        return render_template('index.html',
                               error="Please enter a search term",
                               popular_movies=get_popular_movies(12),
                               all_movies=get_all_movie_titles())

    results = search_movies(query)

    return render_template('search.html',
                           query=query,
                           results=results,
                           all_movies=get_all_movie_titles())


if __name__ == '__main__':
    app.run(debug=True, port=5000)