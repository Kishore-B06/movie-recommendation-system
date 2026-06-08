# 🎬 CineMatch AI - Movie Recommendation System

CineMatch AI is a Machine Learning-powered movie recommendation platform that helps users discover movies similar to their favorites. The system uses content-based filtering and cosine similarity to generate personalized recommendations through an interactive Flask web application.

---

## 🚀 Features

* 🎯 Personalized movie recommendations
* 🔍 Search movies by title, description, or director
* 🎭 Browse movies by genre
* ⭐ View ratings, duration, and director information
* 📊 Similarity score-based recommendations
* 🎨 Modern and responsive user interface
* ⚡ Fast recommendation generation using precomputed similarity matrices

---

## 🧠 Machine Learning Concepts Used

* Content-Based Filtering
* TF-IDF Vectorization
* Cosine Similarity
* Feature Engineering
* Text Processing and Data Cleaning
* Similarity-Based Recommendation Systems

---

## ⚙️ How It Works

1. Movie data is collected and cleaned.
2. Important movie attributes are combined into a single feature set.
3. TF-IDF Vectorization converts textual information into numerical vectors.
4. Cosine Similarity calculates relationships between movies.
5. The system identifies and recommends the most similar movies.
6. Recommendations are displayed through an interactive Flask web interface.

---

## 📊 Dataset Information

* Dataset Size: 16,000+ Movies
* Attributes Used:

  * Movie Title
  * Genres
  * Description
  * Director
  * Rating
  * Duration
  * Vote Count

---

## 💻 Tech Stack

### Backend

* Python
* Flask

### Machine Learning

* Pandas
* NumPy
* Scikit-learn
* TF-IDF Vectorizer
* Cosine Similarity

### Frontend

* HTML5
* CSS3
* JavaScript
* Font Awesome

---

## 📂 Project Structure

```text
movie-recommendation-system/
│
├── model/
│   ├── 16k_Movies.csv
│   ├── model_building.ipynb
│   └── movie_recommender.pkl
│
├── website/
│   ├── app.py
│   ├── static/
│   │   └── style.css
│   └── templates/
│       ├── index.html
│       ├── genre.html
│       ├── recommendations.html
│       └── search.html
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 🎯 Application Modules

### Home Page

Browse popular movies and discover recommendations.

### Movie Recommendation Engine

Get similar movies based on content similarity.

### Search System

Search movies using keywords, titles, and directors.

### Genre Explorer

Browse movies by category such as Action, Drama, Comedy, Horror, and more.

### Similarity Analysis

View recommendation match scores generated using cosine similarity.

---

## ▶️ Installation

### Clone Repository

```bash
git clone https://github.com/Kishore-B06/movie-recommendation-system.git
cd movie-recommendation-system
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
cd website
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

## 🔮 Future Enhancements

* Movie poster integration
* User authentication system
* Watchlist functionality
* Hybrid recommendation system
* Cloud deployment
* Personalized user profiles
* Recommendation analytics dashboard

---

## 👨‍💻 Author

**Kishore Balasundaram**

* GitHub: https://github.com/Kishore-B06
* Repository: Movie Recommendation System

---

⭐ If you found this project useful, consider giving the repository a star.
