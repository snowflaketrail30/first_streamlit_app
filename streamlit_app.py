import streamlit as st
import pandas as py
import requests
import snowflake.connector as sf
from urllib.error import URLError

def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get('https://fruityvice.com/api/fruit/'+fruit_choice)
    #beautify reponse
  fruityvice_normalized = py.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall()
  
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values('"+new_fruit+"')")
    return "Thanks for adding " + new_fruit  
  
st.title('My Mom\'s New Healthy Diner')
st.header('Breakfast Favorites')
st.text('🥣 Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard-Boiled Free-Range Egg')
st.text('🥑🍞 Avocado Toast')
st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = py.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# put pick list to select
fruits_selected = st.multiselect("Pick some fruits :", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_show = my_fruit_list.loc[fruits_selected]
# display the table on tha page
st.dataframe(fruits_show)
st.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = st.text_input('What fruit would you like information about?', 'Kiwi')
  if not fruit_choice:
    st.error('Please select a fruit to get information.')
  else:
    fruityvice_normalized = get_fruityvice_data(fruit_choice)
    st.dataframe(fruityvice_normalized)
except URLError as e:
  st.error()

#Add a button to load list  
st.header("View Our Fruit List - Add Your Favorites!")
if st.button('Get Fruit List'):
  my_cnx = sf.connect(**st.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  st.dataframe(my_data_rows)

add_my_fruit = st.text_input('What fruit would you like add?')
if st.button('Add a Fruit to the List'):
  my_cnx = sf.connect(**st.secrets["snowflake"])
  back_from_function = insert_row_snowflake(add_my_fruit)
  st.text(back_from_function)

