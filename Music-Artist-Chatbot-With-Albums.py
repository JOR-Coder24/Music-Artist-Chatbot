import requests
import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import tkinter as tk
from tkinter import scrolledtext

# Set up Spotify client with credentials
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id='f2972bf2318c4586a77600d836fd4d00',
                                                            client_secret='a0228a18e2474624b869d28a31fe5d06'))

# Functions to fetch artist and album data
def get_artist_data(artist_name):
    result = sp.search(q='artist:' + artist_name, type='artist', limit=1)
    if result['artists']['items']:
        artist = result['artists']['items'][0]
        return artist
    return None

def extract_artist_data(artist):
    if artist:
        return {
            "Name": artist['name'],
            "URL": artist['external_urls']['spotify'],
            "Follower Count": artist['followers']['total'],
            "Genres": ', '.join(artist['genres']),
            "Spotify ID": artist['id'],
            "Albums": get_artist_albums(artist['id']),
            "Top Tracks": get_top_tracks(artist['id']),
        }
    return {"error": "Artist not found"}

def get_artist_albums(artist_id):
    albums = sp.artist_albums(artist_id, album_type='album')
    album_names = [album['name'] for album in albums['items']]
    return ', '.join(album_names)

def get_top_tracks(artist_id):
    top_tracks = sp.artist_top_tracks(artist_id, country='US')
    track_names = [track['name'] for track in top_tracks['tracks']]
    return ', '.join(track_names)


def get_album_data(album_name):
    try:
        # Normalize the album name for better search accuracy
        normalized_album_name = re.sub(r'\s+', ' ', album_name.strip().lower())

        # Search for the album in Spotify
        result = sp.search(q=f'album:"{normalized_album_name}"', type='album', limit=1)
        if result['albums']['items']:
            album = result['albums']['items'][0]
            return extract_album_data(album)
    except Exception as e:
        print(f"Error fetching album data: {e}")
    return {"error": f"Album '{album_name}' not found"}


def extract_album_data(album):
    if album:
        return {
            "Name": album['name'],
            "Type": album['album_type'],
            "Total Tracks": album['total_tracks'],
            "Available Markets": ', '.join(album['available_markets']),
            "Release Date": album['release_date'],
            "Artists": ', '.join(artist['name'] for artist in album['artists']),
            "Label": album.get('label', 'Unknown')
        }
    return {"error": "Album data could not be extracted"}

# Function to answer questions
def answer_question(data, question, is_album=False):
    question = question.lower()
    if is_album:
        if "type" in question:
            return f"Type: {data.get('Type', 'Unknown')}"
        elif "total tracks" in question:
            return f"Total Tracks: {data.get('Total Tracks', 'Unknown')}"
        elif "available markets" in question:
            return f"Available Markets: {data.get('Available Markets', 'Unknown')}"
        elif "release date" in question:
            return f"Release Date: {data.get('Release Date', 'Unknown')}"
        elif "artists" in question:
            return f"Artists: {data.get('Artists', 'Unknown')}"
        elif "label" in question:
            return f"Label: {data.get('Label', 'Unknown')}"
        elif "full profile" in question:
            full_profile = (
                f"Name: {data.get('Name', 'Unknown')}\n"
                f"Type: {data.get('Type', 'Unknown')}\n"
                f"Total Tracks: {data.get('Total Tracks', 'Unknown')}\n"
                f"Available Markets: {data.get('Available Markets', 'Unknown')}\n"
                f"Release Date: {data.get('Release Date', 'Unknown')}\n"
                f"Artists: {data.get('Artists', 'Unknown')}\n"
                f"Label: {data.get('Label', 'Unknown')}"
            )
            return f"Full Profile:\n{full_profile}"
        else:
            return "I don't understand the question. Please ask about specific album data."
    else:
        if "url" in question:
            return f"URL: {data.get('URL', 'Unknown')}"
        elif "follower count" in question:
            return f"Follower count: {data.get('Follower Count', 'Unknown')}"
        elif "genres" in question:
            return f"Genres: {data.get('Genres', 'Unknown')}"
        elif "spotify id" in question:
            return f"Spotify ID: {data.get('Spotify ID', 'Unknown')}"
        elif "albums" in question:
            return f"Albums: {data.get('Albums', 'Unknown')}"
        elif "top tracks" in question:
            return f"Top Tracks: {data.get('Top Tracks', 'Unknown')}"
        elif "full profile" in question:
            full_profile = (
                f"Name: {data.get('Name', 'Unknown')}\n"
                f"URL: {data.get('URL', 'Unknown')}\n"
                f"Follower Count: {data.get('Follower Count', 'Unknown')}\n"
                f"Genres: {data.get('Genres', 'Unknown')}\n"
                f"Spotify ID: {data.get('Spotify ID', 'Unknown')}\n"
                f"Albums: {data.get('Albums', 'Unknown')}\n"
                f"Top Tracks: {data.get('Top Tracks', 'Unknown')}"
            )
            return f"Full Profile:\n{full_profile}"
        else:
            return "I don't understand the question. Please ask about specific artist data."

# GUI function
def chatbot_gui():
    def send_message():
        user_input = entry.get()

        chat_area.insert(tk.END, f"You: {user_input}\n", 'user')  # Insert user text with 'user' tag

        if user_input.lower() == 'exit':
            window.quit()

        if "album" in user_input.lower():
            match = re.search(r'(what|who|tell me about) (is|are|\'s|\'| )([\w\s\-]+)', user_input, re.IGNORECASE)
            if match:
                album_name = match.group(3).strip()
                album_data = get_album_data(album_name)

                if "error" in album_data:
                    chat_area.insert(tk.END, f"MusicBot: {album_data['error']}\n", 'bot')
                else:
                    response = answer_question(album_data, user_input, is_album=True)
                    chat_area.insert(tk.END, f"MusicBot: {response}\n", 'bot')
        else:
            match = re.search(r'(what|who) (is|are|\'s|\'| )([\w\s\-]+)', user_input, re.IGNORECASE)
            if match:
                artist_name = match.group(3).strip()
                artist_data = get_artist_data(artist_name)
                extracted_data = extract_artist_data(artist_data)

                if "error" in extracted_data:
                    chat_area.insert(tk.END, f"MusicBot: {extracted_data['error']}\n", 'bot')
                else:
                    response = answer_question(extracted_data, user_input)
                    chat_area.insert(tk.END, f"MusicBot: {response}\n", 'bot')
            else:
                chat_area.insert(tk.END, "MusicBot: I didn't understand that. Please ask about an artist's data.\n", 'bot')

        entry.delete(0, tk.END)

    # Set up the GUI
    window = tk.Tk()
    window.title("Music Artist Chatbot")

    chat_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, state='normal')
    chat_area.grid(column=0, row=0, columnspan=2, sticky='nsew')

    chat_area.tag_configure('user', foreground='green')
    chat_area.tag_configure('bot', foreground='black')

    entry = tk.Entry(window, width=50)
    entry.grid(column=0, row=1, sticky='ew')

    send_button = tk.Button(window, text="Send", command=send_message)
    send_button.grid(column=1, row=1)

    window.grid_columnconfigure(0, weight=1)
    window.grid_rowconfigure(0, weight=1)

    window.mainloop()

# Start the GUI chatbot
chatbot_gui()
