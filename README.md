# Magic Recommender

Magic Recommender is a Python application that allows Spotify users to create a playlist based on their top tracks. The application uses the Spotify API to extract user's top tracks and generate a playlist with recommended songs.

## Features

- Extract top tracks from a user's Spotify profile
- Generate a playlist with a specified length
- Add recommended songs to the playlist

## Before you install

Before you can use MagicRecommender, you need to create a Spotify Developer application to get your `client_id`, `client_secret`, and `redirect_uri`. Here's how you can do it:

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
2. Log in with your Spotify account.
3. Click on 'Create an App'.
4. Fill in the 'Name', 'Description' and redirect_uri (I recommend using http://localhost:3000/) for your new app, then click 'Create'.
5. On the next page, you will see your `client_id` and `client_secret`. You will need these to authenticate your application.
6. Click on 'Edit Settings'.
7. In the 'Redirect URIs' field, enter the URI where you want Spotify to redirect you after a successful login.
8. Click 'Save'.

## Installation

1. Go to the release section of this repository. [Current release.](https://github.com/PanPeryskop/Magic-Recommender/releases/tag/v1.0)
2. Click on **MagicRecommender.zip**. Download will start automatically.
3. Extract the zip file.
4. Open the extracted folder and run `MagicRecommender.exe`.

## Usage

1. Run the `MagicRecommender.exe` to start the application.
2. The application will ask you to enter your `client_id`, `client_secret`, and `redirect_uri`. Enter the values from the Spotify Developer Dashboard.
3. The application will ask you how long you want the playlist to be. You can enter a number between 1 and 50.
4. Next, you will be asked to enter a name for your playlist.
5. The application will then create a playlist with your specified name and length, filled with recommended songs based on your top tracks.
6. Once the playlist is created, a message will be displayed confirming the successful creation of the playlist.

Enjoy your music!
