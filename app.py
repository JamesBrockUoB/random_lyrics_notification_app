# Author: James Brock

import json
import os
import random

import openai
from dotenv import load_dotenv
from lyricsgenius import Genius
from pync import Notifier


def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = os.getenv(var)


def set_env_vars():
    _set_env("OPENAI_API_KEY")
    _set_env("GENIUS_API_ID")
    _set_env("GENIUS_API_SECRET")
    _set_env("GENIUS_ACCESS_TOKEN")


load_dotenv()
set_env_vars()


def get_cache_file(artist):
    cleaned_artist_name = "".join(c if c.isalnum() else "_" for c in artist)
    return f"{cleaned_artist_name}.json"


def fetch_and_cache_songs(artist, cache_file):
    print(f"Fetching all songs for {artist}")
    genius = Genius()

    artist_obj = genius.search_artist(artist, max_songs=250)
    if not artist_obj:
        print(f"No artist found with the name {artist}")
        return None

    songs = []

    for song in artist_obj.songs:
        songs.append({"title": song.title, "lyrics": song.lyrics, "url": song.url})

    # Cache the songs in the JSON file
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(songs, f, indent=4)
    print(f"Cached {len(songs)} songs for {artist} in {cache_file}.")

    return songs


def fetch_random_song(artist):
    cache_file = get_cache_file(artist)

    if os.path.exists(cache_file) and os.path.getsize(cache_file) > 0:
        print(f"Loading cached songs for {artist}")
        with open("song_collections" / cache_file, "r", encoding="utf-8") as f:
            songs = json.load(f)
    else:
        songs = fetch_and_cache_songs(artist, cache_file)

    if not songs:
        print(f"No songs available for {artist}")
        return None, None, None

    random_song = random.choice(songs)
    return random_song["title"], random_song["lyrics"], random_song["url"]


# Analyze lyrics with GPT
def analyse_lyrics(lyrics, theme):
    openai.api_key = os.environ["OPENAI_API_KEY"]
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"""
                    You are a helpful assistant that analyses song lyrics and picks out a line that conveys a certain: {theme}.
                    Avoid ad-libs or random lines. Provide only one of the most meaningful lines.
                    Return the lyrics in plaintext form with normal capitalisation and punctuation.
                    """,
            },
            {
                "role": "user",
                "content": f"Find me some lyrics to ponder from: {lyrics}",
            },
        ],
        max_tokens=50,
    )
    return response.choices[0].message.content.strip()


def sanitise(text):
    return text.replace('"', '\\"').replace("\n", " ").replace("\\", "")


# Send notification
def send_notification(lyrics, song_title, url):
    Notifier.notify(
        lyrics,
        title=song_title,
        open=url,
        timeout=10,
        sound="Ping",
    )


# Main function
def main(artist, theme="meaningful"):
    song_title, lyrics, song_url = fetch_random_song(artist)
    if not song_title or not lyrics or not song_url:
        print("Failed to fetch song or lyrics.")
        return

    meaningful_line = analyse_lyrics(lyrics, theme)

    send_notification(
        sanitise(meaningful_line),
        sanitise(f"{artist}: {song_title}"),
        sanitise(song_url),
    )


if __name__ == "__main__":
    artist_name = "The Front Bottoms"
    theme_choice = "change"  # - Optional
    main(artist_name, theme_choice)
