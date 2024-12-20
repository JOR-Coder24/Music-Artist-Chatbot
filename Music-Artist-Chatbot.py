import requests
import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import tkinter as tk
from tkinter import scrolledtext

# Set up Spotify client with credentials
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=config.CLIENT_ID,
                                                            client_secret=config.CLIENT_SECRET))

def get_artist_data(artist_name):
    # Search for the artist by name
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
    albums = sp.artist_albums(artist_id, album_type='album',)#can add a limit if you want(i.e. "limit = 5")
    album_names = [album['name'] for album in albums['items']]
    return ', '.join(album_names)

def get_top_tracks(artist_id):
    top_tracks = sp.artist_top_tracks(artist_id, country='US')
    track_names = [track['name'] for track in top_tracks['tracks']]
    return ', '.join(track_names)

def answer_question(artist_data, question):
    question = question.lower()
    if "url" in question:
        return f"URL: {artist_data.get('URL', 'Unknown')}"
    elif "follower count" in question:
        return f"Follower count: {artist_data.get('Follower Count', 'Unknown')}"
    elif "genres" in question:
        return f"Genres: {artist_data.get('Genres', 'Unknown')}"
    elif "spotify id" in question:
        return f"Spotify ID: {artist_data.get('Spotify ID', 'Unknown')}"
    elif "albums" in question:
        return f"Albums: {artist_data.get('Albums', 'Unknown')}"
    elif "top tracks" in question:
        return f"Top Tracks: {artist_data.get('Top Tracks', 'Unknown')}"
    elif "full profile" in question:
        full_profile = (
            f"Name: {artist_data.get('Name', 'Unknown')}\n"
            f"URL: {artist_data.get('URL', 'Unknown')}\n"
            f"Follower Count: {artist_data.get('Follower Count', 'Unknown')}\n"
            f"Genres: {artist_data.get('Genres', 'Unknown')}\n"
            f"Spotify ID: {artist_data.get('Spotify ID', 'Unknown')}\n"
            f"Albums: {artist_data.get('Albums', 'Unknown')}\n"
            f"Top Tracks: {artist_data.get('Top Tracks', 'Unknown')}"
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

        match = re.search(r'(what|who) (is|are|\'s|\'| )([\w\s\-]+)', user_input, re.IGNORECASE)
        if match:
            artist_name = match.group(3).strip()
            artist_data = get_artist_data(artist_name)
            extracted_data = extract_artist_data(artist_data)

            if "error" in extracted_data:
                chat_area.insert(tk.END, f"MusicBot: {extracted_data['error']}\n", 'bot')  # Insert bot text with 'bot' tag
            else:
                response = answer_question(extracted_data, user_input)
                chat_area.insert(tk.END, f"MusicBot: {artist_name} - {response}\n", 'bot')
        else:
            chat_area.insert(tk.END, "MusicBot: I didn't understand that. Please ask about an artist's data.\n", 'bot')

        entry.delete(0, tk.END)

    # Set up the GUI
    window = tk.Tk()
    window.title("Music Artist Chatbot")

    # Create a chat area with scroll
    chat_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, state='normal')
    chat_area.grid(column=0, row=0, columnspan=2, sticky='nsew')  # Make the chat area expand

    # Tag configuration for user and bot text
    chat_area.tag_configure('user', foreground='green')  # User text in red
    chat_area.tag_configure('bot', foreground='black')   # Bot text in blue

    # Entry widget for user input
    entry = tk.Entry(window, width=50)
    entry.grid(column=0, row=1, sticky='ew')  # Allow entry to expand

    # Send button to process the user input
    send_button = tk.Button(window, text="Send", command=send_message)
    send_button.grid(column=1, row=1)

    # Configure row and column weights to allow expansion
    window.grid_columnconfigure(0, weight=1)  # Allow column 0 to expand
    window.grid_rowconfigure(0, weight=1)     # Allow row 0 to expand
    window.grid_rowconfigure(1, weight=0)     # Row 1 (where the entry and button are) stays fixed

    window.mainloop()

# Start the GUI chatbot
chatbot_gui()
