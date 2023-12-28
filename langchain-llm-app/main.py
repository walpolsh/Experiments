import langchain_helper as lch
import streamlit as st

st.title("Baby Name Generator")

baby_gender = st.sidebar.selectbox("What babys gender?", ("boy", "girl"))

hair_color = st.sidebar.text_area(
    label=f"What color is the {baby_gender}?",
    max_chars=15
)

if hair_color:
  response = lch.generate_names(baby_gender, hair_color)
  st.text(response['baby_name'])