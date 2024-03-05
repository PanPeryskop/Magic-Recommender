import customtkinter as tk
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random
import threading
import os
import configparser

playlist_count = 0


def update_slider(event, slider):
    value = event.widget.get()
    if value.isdigit():
        slider.set(int(value))


def slider_activity(value, user_input):
    user_input.delete(0, 'end')
    user_input.insert(0, int(value))


def get_top_tracks(count):
    top_tracks = sp.current_user_top_tracks(limit=count, time_range='medium_term')
    top_tracks_ids = []
    for track in top_tracks['items']:
        top_tracks_ids.append(track['id'])
    random.shuffle(top_tracks_ids)
    return top_tracks_ids


def get_name(name_frame):
    name_frame.pack(fill=tk.BOTH, expand=True)
    s_label = tk.CTkLabel(master=name_frame, text="Enter playlist name.", font=("Roboto", 18, "bold"))
    s_label.pack(pady=(30, 0), anchor='s')
    user_input = tk.CTkEntry(name_frame)
    user_input.pack(pady=15)
    submit_button = tk.CTkButton(input_frame, text="Submit", command=lambda: process_playlist_name(user_input.get(), user_input, submit_button, input_frame))
    submit_button.place(relx=0.5, rely=0.5, anchor='center')


def create_playlist(name, wait_label):
    global playlist_count
    playlist = sp.user_playlist_create(sp.me()['id'], name)
    playlist_id = playlist['id']
    tracks = get_recommended(playlist_count)
    track_ids = []
    for track in tracks['tracks']:
        track_ids.append(track['id'])
    sp.playlist_add_items(playlist_id, track_ids)
    wait_label.destroy()


def end_program():
    end_label = tk.CTkLabel(app, text="Playlist created successfully!", font=("Roboto", 20, "bold"), text_color="green")
    end_label.place(relx=0.5, rely=0.5, anchor='center')
    app.after(5000, app.quit)


def get_recommended(length):
    global playlist_count
    top_tracks = get_top_tracks(20)
    top_tracks = random.sample(top_tracks, 5)
    recommended_tracks = sp.recommendations(seed_tracks=top_tracks, limit=playlist_count)
    return recommended_tracks


def process_playlist_name(input, user_input, submit_button, input_frame):
    playlist_name = input
    user_input.destroy()
    for widget in input_frame.winfo_children():
        widget.destroy()
    submit_button.destroy()
    wait_label = tk.CTkLabel(app, text="Please wait while we create your playlist...", font=("Roboto", 20, "bold"), text_color="cyan")
    wait_label.place(relx=0.5, rely=0.5, anchor='center')
    thread = threading.Thread(target=create_playlist, args=(playlist_name, wait_label))
    thread.start()
    check_thread(thread, wait_label)


def check_thread(thread, wait_label):
    if thread.is_alive():
        app.after(100, check_thread, thread, wait_label)
    else:
        wait_label.destroy()
        end_program()


def process_user_input(input, user_input, input_frame):
    global playlist_count
    if input.isdigit() and int(input) > 0:
        playlist_count = int(input)
        user_input.destroy()
        for widget in input_frame.winfo_children():
            widget.destroy()
        get_name(input_frame)
    elif input > 50:
        error_label = tk.CTkLabel(app, text="Please enter a number between 1 and 50.")
        error_label.pack()
        app.after(5000, error_label.destroy)
    else:
        error_label = tk.CTkLabel(app, text="Please enter a number.")
        error_label.pack()
        app.after(5000, error_label.destroy)


def get_user_input(input_frame):
    input_frame.pack(fill=tk.BOTH, expand=True)
    s_label = tk.CTkLabel(master=input_frame, text="How long do you want the playlist to be?", font=("Roboto", 18, "bold"))
    s_label.pack(pady=(30, 0), anchor='s')
    user_input = tk.CTkEntry(input_frame)
    user_input.pack(pady=15)
    user_input.bind('<KeyRelease>', lambda event: update_slider(event, slider))
    slider = tk.CTkSlider(input_frame, from_=1, to=50, number_of_steps=49, command=lambda value: slider_activity(value, user_input))
    slider.pack(pady=15)
    submit_button = tk.CTkButton(input_frame, text="Submit", command=lambda: process_user_input(user_input.get(), user_input, input_frame))
    submit_button.place(relx=0.5, rely=0.5, anchor='center')
    app.mainloop()


def get_user_input_config():
    input_frame = tk.CTkFrame(app)
    input_frame.pack(fill=tk.BOTH, expand=True)

    client_id_label = tk.CTkLabel(input_frame, text="Enter your client_id:", font=("Roboto", 16, "bold"), text_color="white")
    client_id_label.pack(pady=(40, 0))
    client_id_entry = tk.CTkEntry(input_frame)
    client_id_entry.pack(pady=5)

    client_secret_label = tk.CTkLabel(input_frame, text="Enter your client_secret:", font=("Roboto", 16, "bold"), text_color="white")
    client_secret_label.pack(pady=(30, 0))
    client_secret_entry = tk.CTkEntry(input_frame)
    client_secret_entry.pack(pady=5)

    redirect_uri_label = tk.CTkLabel(input_frame, text="Enter your redirect_uri:", font=("Roboto", 16, "bold"), text_color="white")
    redirect_uri_label.pack(pady=(30, 0))
    redirect_uri_entry = tk.CTkEntry(input_frame)
    redirect_uri_entry.pack(pady=5)

    submit_button = tk.CTkButton(input_frame, text="Submit", font=("Roboto", 10), text_color="white", command=lambda: process_user_input_config(client_id_entry.get(), client_secret_entry.get(), redirect_uri_entry.get(), input_frame))
    submit_button.place(relx=0.5, rely=0.9, anchor='s')
    app.mainloop()


def process_user_input_config(client_id, client_secret, redirect_uri, input_frame):
    config['SPOTIFY'] = {'client_id': client_id, 'client_secret': client_secret, 'redirect_uri': redirect_uri}

    with open(config_file, 'w') as configfile:
        config.write(configfile)

    input_frame.destroy()
    app.quit()


def end_all():
    app.quit()
    quit()


app = tk.CTk()
app.title("Magic Recommender")
app.geometry("420x600")
app.protocol("WM_DELETE_WINDOW", end_all)

#Dane autoryzacyjne
config_file = 'config.sg'
config = configparser.ConfigParser()

if not os.path.exists(config_file):
    get_user_input_config()
    config.read(config_file)
    client_id = config.get('SPOTIFY', 'client_id')
    client_secret = config.get('SPOTIFY', 'client_secret')
    redirect_uri = config.get('SPOTIFY', 'redirect_uri')
else:
    config.read(config_file)
    client_id = config.get('SPOTIFY', 'client_id')
    client_secret = config.get('SPOTIFY', 'client_secret')
    redirect_uri = config.get('SPOTIFY', 'redirect_uri')

scope = 'playlist-read-private user-modify-playback-state playlist-modify-public playlist-modify-private user-top-read'
auth_manager = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)
sp = spotipy.Spotify(auth_manager=auth_manager)

input_frame = tk.CTkFrame(app)
get_user_input(input_frame)


