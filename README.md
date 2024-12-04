# Music Artist Chatbot

This project is a Python-based chatbot that uses the Spotify Web API to retrieve and display data about music artists. The bot can answer questions related to an artist's profile, albums, top tracks, and more. It features a simple and interactive graphical user interface (GUI) built using the Tkinter library.

## Features

- **Search Music Artists**: Ask the bot about an artist’s profile, top tracks, albums, genres, follower count, and Spotify ID.
- **Interactive GUI**: The chatbot is embedded in a GUI using Tkinter, which displays both user and bot messages with different colors for clarity.
- **Spotify Data**: The chatbot pulls data from Spotify through the Spotipy library, using artist search and API endpoints to fetch information.

## Setup Instructions

### Prerequisites

1. Python 3.x installed on your machine.
2. Required Python libraries:
   - `requests`
   - `spotipy`
   - `tkinter`
   
You can install the required libraries using pip:

```bash
pip install requests spotipy
Getting Started
Clone or download the repository to your local machine.
Replace the client_id and client_secret in the code with your own credentials from the Spotify Developer Dashboard.
Run the Python script:
bash
Copy code
python music_artist_chatbot.py
This will open the chatbot GUI where you can interact with the bot and ask questions related to any artist.

Example Questions
"What is Taylor Swift's URL?"
"What are Drake's top tracks?"
"Tell me about Ed Sheeran's albums."
"What is the follower count for Ariana Grande?"
Exiting the Chatbot
To exit the chatbot, simply type exit in the chat window.

Limitations
The bot fetches a limited number of albums (5) and tracks (5) per artist.
It works only for the data available on Spotify.
