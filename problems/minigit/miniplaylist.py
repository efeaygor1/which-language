"""
mini-playlist v2 — Simplified implementation
Student: Kamil Efe Aygör (251478093)

--- V2 Task List ---
1. Task: Implement 'add' command (Appends a new song with an auto-incremented ID and current date).
2. Task: Implement duplicate check (If the song already exists in the playlist, refuse to add it).
3. Task: Implement 'delete' command (Removes a song by its ID without using Python lists).

--- V1 -> V2 Changes Summary ---
In V1, we added the 'show' command to read and display songs line by line using a while loop.
In V2, the application is now fully functional. We implemented data mutation:
the ability to 'add' new songs (with duplicate protection) and 'delete' existing songs.
Because lists are forbidden, the delete operation is handled by writing non-deleted lines to a temporary file, then replacing the original file.
"""
import sys
import os
import datetime


def initialize():
    """Initializes the main miniplaylist directory."""
    if os.path.exists(".miniplaylist"):
        return "Already initialized"

    os.mkdir(".miniplaylist")
    return "Initialized empty playlist manager in .miniplaylist/"


def create_playlist(playlist_name):
    """Creates a new playlist file (.dat) with the given name."""
    if not os.path.exists(".miniplaylist"):
        return "Not initialized."

    file_path = ".miniplaylist/" + playlist_name + ".dat"

    if os.path.exists(file_path):
        return "Playlist already exists."

    f = open(file_path, "w")
    f.close()
    return "Playlist '" + playlist_name + "' created."


def show_playlist(playlist_name):
    """Reads and displays songs in the given playlist using a while loop."""
    if not os.path.exists(".miniplaylist"):
        return "Not initialized."

    file_path = ".miniplaylist/" + playlist_name + ".dat"

    if not os.path.exists(file_path):
        return "Playlist not found."

    f = open(file_path, "r")
    line = f.readline()

    if not line:
        f.close()
        return "Playlist is empty."

    result = ""

    while line != "":
        first_pipe = line.find("|")
        second_pipe = line.find("|", first_pipe + 1)

        if first_pipe != -1 and second_pipe != -1:
            song_id = line[:first_pipe]
            title = line[first_pipe + 1:second_pipe]
            date_str = line[second_pipe + 1:].strip()

            result = result + "[" + song_id + "] " + title + " (" + date_str + ")\n"

        line = f.readline()

    f.close()
    return result.strip()


def add_song(playlist_name, song_title):
    """Adds a new song to the playlist, checking for duplicates and auto-incrementing ID."""
    if not os.path.exists(".miniplaylist"):
        return "Not initialized."

    file_path = ".miniplaylist/" + playlist_name + ".dat"
    if not os.path.exists(file_path):
        return "Playlist not found."

    # First pass: find the last ID and check for duplicates
    f = open(file_path, "r")
    line = f.readline()
    last_id = 0

    while line != "":
        first_pipe = line.find("|")
        second_pipe = line.find("|", first_pipe + 1)

        if first_pipe != -1 and second_pipe != -1:
            current_id = int(line[:first_pipe])
            title = line[first_pipe + 1:second_pipe]

            # Task 2: Duplicate check
            if title == song_title:
                f.close()
                return "Song already exists."

            last_id = current_id
        line = f.readline()
    f.close()

    # Generate new ID and get today's date
    new_id = last_id + 1
    today = datetime.date.today().strftime("%Y-%m-%d")

    # Append the new song
    f = open(file_path, "a")
    f.write(str(new_id) + "|" + song_title + "|" + today + "\n")
    f.close()

    return "Added '" + song_title + "' to '" + playlist_name + "'."


def delete_song(playlist_name, song_id_to_delete):
    """Deletes a song by ID using a temporary file to avoid using lists."""
    if not os.path.exists(".miniplaylist"):
        return "Not initialized."

    file_path = ".miniplaylist/" + playlist_name + ".dat"
    if not os.path.exists(file_path):
        return "Not found."

    temp_file_path = file_path + ".tmp"

    f_in = open(file_path, "r")
    f_out = open(temp_file_path, "w")

    line = f_in.readline()
    deleted = False

    while line != "":
        first_pipe = line.find("|")
        if first_pipe != -1:
            current_id = line[:first_pipe]
            # If this is NOT the ID we want to delete, write it to the temp file
            if current_id == str(song_id_to_delete):
                deleted = True
            else:
                f_out.write(line)
        line = f_in.readline()

    f_in.close()
    f_out.close()

    # Replace the old file with the new temporary file
    os.remove(file_path)
    os.rename(temp_file_path, file_path)

    if deleted:
        return "Deleted song #" + str(song_id_to_delete) + " from '" + playlist_name + "'."
    else:
        return "Not found."


# --- Main Program ---
if len(sys.argv) < 2:
    print("Usage: python miniplaylist.py <command> [args]")
elif sys.argv[1] == "init":
    print(initialize())
elif sys.argv[1] == "create":
    if len(sys.argv) < 3:
        print("Usage: python miniplaylist.py create <playlist_name>")
    else:
        print(create_playlist(sys.argv[2]))
elif sys.argv[1] == "add":
    if len(sys.argv) < 4:
        print("Usage: python miniplaylist.py add <playlist_name> <song_title>")
    else:
        print(add_song(sys.argv[2], sys.argv[3]))
elif sys.argv[1] == "show":
    if len(sys.argv) < 3:
        print("Usage: python miniplaylist.py show <playlist_name>")
    else:
        print(show_playlist(sys.argv[2]))
elif sys.argv[1] == "delete":
    if len(sys.argv) < 4:
        print("Usage: python miniplaylist.py delete <playlist_name> <song_id>")
    else:
        print(delete_song(sys.argv[2], sys.argv[3]))
else:
    print("Unknown command: " + sys.argv[1])