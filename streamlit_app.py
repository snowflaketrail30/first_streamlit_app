import streamlit
import pandas as py
streamlit.title('My Mom\'s New Healthy Diner')
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = py.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# put pick list to select
fruits_selected = streamlit.multiselect("Pick some fruits :", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_show = my_fruit_list.loc[fruits_selected]
# display the table on tha page
streamlit.dataframe(fruits_show)
