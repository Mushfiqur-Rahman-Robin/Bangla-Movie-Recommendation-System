import pickle
import streamlit as st
import requests
import pandas as pd


import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False
# DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data


def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data


def recommend(movie):
    movies = pickle.load(open(r'C:\Users\USER\Desktop\Bangla-Movie-Recommendation-System\movie_list.pkl','rb'))
    similarity = pickle.load(open(r'C:\Users\USER\Desktop\Bangla-Movie-Recommendation-System\similarity.pkl','rb'))
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    for i in distances[1:6]:
        # fetch the movie poster
        #movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names


def main():

	menu = ["Home","Login","SignUp"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		st.header("Welcome to the Bangla Movie Recommendation System application.")

	elif choice == "Login":
		st.subheader("Log in with your name and password to get your movie recommendation.")

		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password",type='password')
		
		if st.sidebar.checkbox("Login"):
			create_usertable()
			hashed_pswd = make_hashes(password)

			result = login_user(username,check_hashes(password,hashed_pswd))
			if result:
				st.success("Logged In as {}".format(username))
				task = st.selectbox("Task",["Recommend", "Profiles"])

				if task == "Recommend":
					st.header("Bangla Movie Recommendation System")
					movies = pickle.load(open(r'C:\Users\USER\Desktop\Bangla-Movie-Recommendation-System\movie_list.pkl','rb'))
					similarity = pickle.load(open(r'C:\Users\USER\Desktop\Bangla-Movie-Recommendation-System\similarity.pkl','rb'))
					
					movie_list = movies['title'].values
					selected_movie = st.selectbox(
						"Type or select a movie from the dropdown",
						movie_list
					)
					
					if st.button('Show Recommendation'):
						st.header('Top 5 recommended movies:')
						recommended_movie_names = recommend(selected_movie)
						col1, col2 = st.columns(2)
						with col1:
							st.text(recommended_movie_names[0])
						with col2:
							st.text(recommended_movie_names[1])

						with col1:
							st.text(recommended_movie_names[2])
						with col2:
							st.text(recommended_movie_names[3])
						with col1:
							st.text(recommended_movie_names[4])

				elif task == "Profiles":
					st.subheader("User Profiles")
					user_result = view_all_users()
					clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
					st.dataframe(clean_db)
			else:
				st.warning("Incorrect Username/Password")

	elif choice == "SignUp":
		st.subheader("Create New Account")
		new_user = st.text_input("Username")
		new_password = st.text_input("Password",type='password')

		if st.button("Signup"):
			create_usertable()
			add_userdata(new_user,make_hashes(new_password))
			st.success("You have successfully created a valid Account")
			st.info("Go to Login Menu to login")



if __name__ == '__main__':
	main()