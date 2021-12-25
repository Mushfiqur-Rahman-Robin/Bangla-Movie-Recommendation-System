import pickle
import streamlit as st
import requests
import pandas as pd
import razorpay
from order import *
import webbrowser
import streamlit.components.v1 as stc
import pandas as pd
from paymentID import cursor, create_idtable


HTML_BANNER = """
    <div style="background-color:#464e5f;padding:5px;border-radius:5px">
    <h1 style="color:white;text-align:center;">Bangla Movie Recommendation App</h1>
    </div>
    """

from PIL import Image
image0 = Image.open(r'Movie Covers/bangla_movie_recommendation_banner.jpg')
image1 = Image.open(r'Movie Covers/Dhaka Dream.png')
image2 = Image.open(r'Movie Covers/Rickshaw Girl.png')
image3 = Image.open(r'Movie Covers/Khachar Bhitor Ochin Pakhi.png')
image4 = Image.open(r'Movie Covers/The Broker.png')
image5 = Image.open(r'Movie Covers/August 1975.png')
image6 = Image.open(r'Movie Covers/Rehana Maryam Noor.png')
image7 = Image.open(r'Movie Covers/Piprabidya.png')
image8 = Image.open(r'Movie Covers/Goopy Gyne Bagha Byne.png')
image9 = Image.open(r'Movie Covers/Paromitar Ekdin.png')
image10 = Image.open(r'Movie Covers/Heerak Rajar Deshe.png')
image11 = Image.open(r'Movie Covers/Pather Panchali.png')
image12 = Image.open(r'Movie Covers/Padma Nadir Majhi.png')



import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False

# DB Management
import sqlite3 
conn = sqlite3.connect('data.db', check_same_thread=False)
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

def view_all_users(username):
	c.execute('SELECT * FROM userstable WHERE username =?', (username,))
	data = c.fetchall()
	return data

def id_user(order_id,payment_id):
	cursor.execute('SELECT * FROM idtable WHERE order_id =? AND payment_id = ?',(order_id,payment_id))
	data = cursor.fetchall()
	return data


def recommend(movie):
    movies = pickle.load(open(r'movie_list.pkl','rb'))
    similarity = pickle.load(open(r'similarity.pkl','rb'))
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    for i in distances[1:6]:
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names


def main():

	menu = ["Home","Login","SignUp", "Subscription", "Watch", "Logout"]
	choice = st.sidebar.selectbox("Menu",menu)
	stc.html(HTML_BANNER)

	if choice == "Home":
		st.header("Welcome to the Bangla Movie Recommendation System application.")
		st.image(image0, caption= 'Traditional Bangla cinema poster behind a rickshaw.')

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
				task = st.selectbox("Task",["Recommend", "Profile"])

				if task == "Recommend":
					st.header("Bangla Movie Recommendation System")
					movies = pickle.load(open(r'movie_list.pkl','rb'))
					similarity = pickle.load(open(r'similarity.pkl','rb'))
					
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


				elif task == "Profile":
					st.subheader("User Profile")
					user_result = view_all_users(username)
					clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
					st.dataframe(clean_db)


			else:
				st.warning("Incorrect Username/Password")

	elif choice == "Logout":
					st.header("Thank you for using our application. Login again for more recommendations.")


	elif choice == "SignUp":
		st.subheader("Create New Account")
		new_user = st.text_input("Username")
		new_password = st.text_input("Password",type='password')

		if st.button("Signup"):
			create_usertable()
			add_userdata(new_user,make_hashes(new_password))
			st.success("You have successfully created a valid Account")
			st.info("Go to Login Menu to login")

	elif choice == "Subscription":
		fi = open('payment.html', 'r')
		fi.close()
		webbrowser.open_new_tab('payment.html')
		st.header('Subscribe to this application for more recommendations. Choose your payment options from the payment gateway. To pay for subscription click the button below.')
		st.button("Pay for subscription.")


	elif choice == "Watch":
		orderID = st.sidebar.text_input("Enter your orderID")
		paymentID = st.sidebar.text_input("Enter your paymentID")

		if st.sidebar.button("Confirm"):

			result = id_user(orderID, paymentID)
			if result:
				st.success("Successfully entered.")

				col1, col2, col3 = st.columns(3)
				with col1:
					st.image(image1)
					st.write("[Click to watch](https://www.imdb.com/title/tt5331886/)")
				with col2:
					st.image(image2)
					st.write("[Click to watch](https://www.imdb.com/title/tt4853244/)")

				with col3:
					st.image(image3)
					st.write("[Click to watch](https://www.imdb.com/title/tt15756034/)")
				with col1:
					st.image(image4)
					st.write("[Click to watch](https://www.imdb.com/title/tt15547790/)")
				with col2:
					st.image(image5)
					st.write("[Click to watch](https://www.imdb.com/title/tt13770656/)")

				with col3:
					st.image(image6)
					st.write("[Click to watch](https://www.imdb.com/title/tt14775748/)")
				with col1:
					st.image(image7)
					st.write("[Click to watch](https://www.imdb.com/title/tt3461908/)")

				with col2:
					st.image(image8)
					st.write("[Click to watch](https://www.imdb.com/title/tt0063023/)")
				with col3:
					st.image(image9)
					st.write("[Click to watch](https://www.imdb.com/title/tt0249866/)")
				with col1:
					st.image(image10)
					st.write("[Click to watch](https://www.imdb.com/title/tt0080856/)")

				with col2:
					st.image(image11)
					st.write("[Click to watch](https://www.imdb.com/title/tt0048473/)")
				with col3:
					st.image(image12)
					st.write("[Click to watch](https://www.imdb.com/title/tt0107767/)")


if __name__ == '__main__':
	main()