# Music-Artist-Chatbot

This project is a Python-based chatbot that uses the Spotify Web API to retrieve and display data about music artists. The bot can answer questions related to an artist's profile, albums, top tracks, and more. It features a simple and interactive graphical user interface (GUI) built using the Tkinter library. It's inspired by a previous project of mine "SuperBot"

"Music-Artist-Chatbot-With-Albums.py" is an additional program which does the same as the orginal but also gives data about an album(Name, Type, Total Tracks(no. tracks), Available Markets, Release Date, Artists, Label). NOTE-When running, must specify that it is an album in the question.

## Features

- **Search Music Artists**: Ask the bot about an artist’s profile, top tracks, albums, genres, follower count, and Spotify ID.
- **Interactive GUI**: The chatbot is embedded in a GUI using Tkinter, which displays both user and bot messages with different colors for clarity.
- **Spotify Data**: The chatbot pulls data from Spotify through the Spotipy library, using artist search and API endpoints to fetch information.

## Setup Instructions

### Prerequisites

1. Python 3.x installed on your machine.
2. Required Python libraries(You can install them using pip):
   - `requests`
   - `spotipy`
   - `tkinter`
   
Need a "Spotify for Developers" account and your own Client ID and Client Secret numbers


## Getting Started
Clone or download the repository to your local machine.
Replace the client_id and client_secret in the code with your own credentials from the Spotify Developer Dashboard.


Example Questions
"What is Taylor Swift's URL?"
"What are Drake's top tracks?"
"What are album World War Joy's available markets?"  

Exiting the Chatbot-To exit the chatbot, simply type exit in the chat window.

Limitations:
- The bot fetches a limited number of top tracks (5) per artist.
- It works only for the data available on Spotify.
