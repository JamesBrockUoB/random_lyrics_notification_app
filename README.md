
# Repo overview
This is a fun little pet project of mine that aims to brighten your day by serving you theme related lyrics from artists you choose.

It works by taking in an input artist name and theme.

The first time you run the code for a new artist, the lyrics genius library will scrape all of the songs for that artist and store them in a json file for caching.
- On subsequent runs, the code will only use the cached file for reference, with the file storing the song name, song url, and lyrics

A random song will then be picked from the cached file, and the LLM model will analyse the lyrics to find those that agree most with the provided theme
- If no theme is chosen, it will try to find the lyrics with the most meaning, which may be subjective
- The model is instructed to avoid choosing lyrics that lack substance or is primarily of adlibs


This song will then be served as a notification on your laptop, and by clicking on it, you will be taken to the lyrics genius page for the song in which you can listen to it, and explore the explanations people have provided for the lyrics

# Setup and usage

Create a virtual environment and install the project dependencies with `pip install -r requirements.txt`

Create a .env file with the following:
- OPENAI_API_KEY
- GENIUS_API_ID
- GENIUS_API_SECRET
- GENIUS_ACCESS_TOKEN

The Genius API Key can be fetched from here: https://docs.genius.com/

It will ask you to provide a website address, any can be used here, so just plug in a random link

# Todos

- Make it more commandline dependent, providing the theme and artist as arguments

- Set this up with a cron job scheduler such that it can run every day at times you wish to specify

- Search over all songs in the collection to look for lyrics containing the desired theme, rather than picking a song at random

- Keep a history of the lyrics previously served to reduce the chance they will be given again too soon - could provide a discount value that updates each day

- Play around with different models - integrating in a local model to reduce costs
