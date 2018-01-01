from flask import Flask, render_template, request, url_for
from flask_wtf import FlaskForm
from wtforms import Form, TextAreaField, validators, StringField
import numpy as np
import pandas as pd
import pickle
from sklearn.neighbors import NearestNeighbors

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissecret';

class SearchForm(FlaskForm):
	movie = StringField()

@app.route('/')
def index():
	form = SearchForm();
	if form.validate_on_submit():
		return sorted_list(query(title_to_id(form.movie.data)));
	return render_template('app.html', form=form);

@app.route('/movie_list',methods=['POST'])
def movie_list():
	form = SearchForm();
	if form.validate_on_submit():
		movie_list = sorted_list(title_to_id(form.movie.data))
	return render_template('movie_list.html',movie_list = movie_list) 

def title_to_id(name):
	arr = movies.index[movies["title"] == name].tolist()
	return arr[0]

def sorted_list(id_entry):
	l = query(id_entry)
	l = [s+1 for s in l];
	d = []
	for x in l:
		scores = ratings.loc[ratings["movieId"] == x].rating;
		mean_score = np.mean(scores);
		if mean_score is not None:
			d.append([x-1,mean_score]);
	d = sorted(d, key=lambda x: x[1]);
	u = [];
	for b in d:
		u.append(movies.iloc[b[0]]["title"]);
	return u;

def load_files():
	global X,nbrs,movies,ratings;
	pickle_in = open("nbrs.pickle","rb")
	nbrs = pickle.load(pickle_in)
	pickle_in.close();
	pickle_in = open("movies.pickle","rb")
	movies = pickle.load(pickle_in)
	pickle_in.close();
	pickle_in = open("rating.pickle","rb")
	ratings = pickle.load(pickle_in)
	pickle_in.close();
	pickle_in = open("X.pickle","rb")
	X = pickle.load(pickle_in)
	pickle_in.close();

def query(id_entry):
	xtest = X.iloc[id_entry]
	xtest = xtest.values.reshape(1, -1)
	distances, indices = nbrs.kneighbors(xtest)
	return indices[0][:];

def classifier():
	movies = pd.read_csv("data/movie.csv");
	ratings = pd.read_csv("data/rating.csv",nrows=55491);
	year = []
	titles = []

	for title in movies["title"]:
		x = title.rfind(' (')
		if x is not -1:
			titles.append(title[0:x])
			year.append(title[x+2:-1])
		else:
			titles.append(title)
			year.append("Nan")
	movies.title = titles
	movies['year'] = pd.Series(year)
	pickle_out = open("movies.pickle","wb")
	pickle.dump(movies, pickle_out)
	pickle_out.close()
	pickle_out = open("rating.pickle","wb")
	pickle.dump(ratings, pickle_out)
	pickle_out.close()
	genre_labels = set()
	for s in movies['genres'].str.split('|').values:
		genre_labels = genre_labels.union(set(s))
	genre_labels.remove('(no genres listed)')
	genre_labels = list(genre_labels)
	df = pd.concat([movies,movies['genres'].str.get_dummies(sep='|')],axis=1)
	X = pd.DataFrame(df,columns = genre_labels)
	pickle_out = open("X.pickle","wb")
	pickle.dump(X, pickle_out)
	pickle_out.close()
	nbrs = NearestNeighbors(n_neighbors=20, algorithm='auto', metric='euclidean').fit(X)
	pickle_out = open("nbrs.pickle","wb")
	pickle.dump(nbrs, pickle_out)
	pickle_out.close()

if __name__  == '__main__':
	classifier();
	load_files();
	app.run(debug=True)
