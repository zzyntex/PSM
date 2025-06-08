import streamlit as st
import random
import os

# Page configuration
st.set_page_config(page_title="Interactive Virtual Classroom", layout="wide")

# Define the available emojis
emojis = ['😊', '🎉', '👍', '💡', '🤔']

# Display title and instructions
st.title("Welcome to the Interactive Virtual Classroom!")
st.write("""
    This is an interactive educational app where you can zoom, control brightness, and add emojis.
""")

# Zoom feature (using slider)
st.subheader("Zoom")
zoom_level = st.slider("Zoom in/out", min_value=1, max_value=5, value=1)
st.write(f"Zoom level: {zoom_level}")

# Brightness control (using slider)
st.subheader("Brightness Control")
brightness_level = st.slider("Adjust Brightness", min_value=1, max_value=100, value=100)
st.write(f"Brightness: {brightness_level}%")

# Button to toggle volume (simple button)
st.subheader("Volume Control")
volume_on = st.button("Toggle Volume")
if volume_on:
    st.write("🔊 Volume is ON")
else:
    st.write("🔇 Volume is OFF")

# Drag-and-drop-like feature
st.subheader("Drag & Drop Simulation (via click)")
click = st.button("Add an Item")
if click:
    st.write("You added an item to the classroom!")

# Add emojis dynamically
st.subheader("Add Emojis")
emoji_to_add = random.choice(emojis)
if st.button(f"Add {emoji_to_add}"):
    st.write(f"You added the emoji: {emoji_to_add}")

# Display the current zoom, brightness, and other interactive features
st.write(f"Current Zoom Level: {zoom_level}")
st.write(f"Current Brightness: {brightness_level}%")
askdjbaskjdbasda