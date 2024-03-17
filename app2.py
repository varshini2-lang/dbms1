from flask import Flask, render_template, request, redirect, url_for, flash,session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from functools import wraps

import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
login_manager = LoginManager(app)




db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'arrow@7501',
    'database': 'varshini'
}

conn = mysql.connector.connect(**db_config)
cur = conn.cursor()

class User(UserMixin):
    def __init__(self, user_id, username, password):
        self.id = user_id
        self.username = username
        self.password = password

# Replace this with your actual user retrieval logic
def get_user_by_id(user_id):
    # Example: Query the database to get the user by ID
    # This is where you would perform the actual authentication
    users = [
        User(1, 'varshini', 'password'),
        User(2, 'prashita', 'password')
    ]
    for user in users:
        if user.id == user_id:
            return user
    return None

def get_user_by_username(username):
    # Example: Query the database to get the user by username
    # This is where you would perform the actual authentication
    users = [
        User(1, 'varshini', 'password'),
        User(2, 'prashita', 'password'),
        User(1, 'shikha', 'password'),
        User(2, 'divya', 'password')
    ]
    for user in users:
        if user.username == username:
            return user
    return None

@login_manager.user_loader
def load_user(user_id):
    # Retrieve the user by ID
    return get_user_by_id(user_id)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Replace this with your actual authentication logic
        user = get_user_by_username(username)

        if user and user.password == password:
            login_user(user)
            flash(f'Welcome, {username}!', 'success')
            flash(f'Welcome, {username}! You logged in as a manager.', 'success')
            return redirect(url_for('home'))

        flash('Invalid username or password', 'error')
        return redirect(url_for('index')) 

    return render_template('login.html')



@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/updatesong/<string:title>', methods=['GET', 'POST'])
def updatesong(title):
    if request.method == 'POST':
        # Get updated song details from the form
        updated_title = request.form['title']
        updated_album = request.form['album']
        updated_artist = request.form['artist']
        updated_genre = request.form['genre']
        updated_rlsyr = request.form['rlsyr']

        try:
            # Check if the album exists, if not, insert it
            cur.execute('''
                INSERT INTO album (album_name) 
                SELECT %s
                WHERE NOT EXISTS (SELECT 1 FROM album WHERE album_name = %s)
            ''', (updated_album, updated_album))

            # Check if the artist exists, if not, insert it
            cur.execute('''
                INSERT INTO artist (artist_name) 
                SELECT %s
                WHERE NOT EXISTS (SELECT 1 FROM artist WHERE artist_name = %s)
            ''', (updated_artist, updated_artist))

            # Update the song details in the database based on the title
            cur.execute('''
                UPDATE track t
                JOIN album a ON t.album_id = a.id
                JOIN artist ar ON t.artist_id = ar.id
                JOIN genre g ON t.genre_id = g.id
                SET 
                    t.album_id = (SELECT id FROM album WHERE album_name = %s), 
                    t.artist_id = (SELECT id FROM artist WHERE artist_name = %s), 
                    t.genre_id = (SELECT id FROM genre WHERE genre_name = %s), 
                    t.rlsyr = %s
                WHERE 
                    t.title = %s
            ''', (updated_album, updated_artist, updated_genre, updated_rlsyr, title))

            conn.commit()
            flash('Song updated successfully', 'success')
            # Redirect to the view songs page after updating the song
            return redirect(url_for('viewsongs'))
        except Exception as e:
            flash(f"Error: {str(e)}", 'error')

    # Retrieve the existing song details from the database
    try:
        cur.execute('''
            SELECT t.title, a.album_name, ar.artist_name, g.genre_name, t.rlsyr 
            FROM track t
            JOIN album a ON t.album_id = a.id
            JOIN artist ar ON t.artist_id = ar.id
            JOIN genre g ON t.genre_id = g.id
            WHERE t.title = %s
        ''', (title,))
        song_details = cur.fetchone()
        return render_template('updatesong.html', song_details=song_details)
    except Exception as e:
        flash(f"Error: {str(e)}", 'error')
        return redirect(url_for('viewsongs'))

        
@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        title = request.form['title']

        try:
            cur.execute("""
                DELETE track, album, artist
                FROM track
                LEFT JOIN album ON track.album_id = album.id
                LEFT JOIN artist ON track.artist_id = artist.id
                WHERE track.title = %s
            """, (title,))
            conn.commit()
            
            if cur.rowcount > 0:
                flash('Song Record Deleted Successfully', 'success')
            else:
                flash('Song with specified title not found', 'error')

            return redirect(url_for('delete'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')

    return render_template('delete.html')



@app.route('/addsong', methods=['GET', 'POST'])

def addsong():
    if request.method == 'POST':
        title = request.form['title']
        artist = request.form['artist']
        album = request.form['album']
        genre = request.form['genre']
        rlsyr = request.form['rlsyr']

        try:
            cur.execute('INSERT IGNORE INTO artist(artist_name) VALUES (%s)', (artist,))
            cur.execute("SELECT id FROM artist WHERE artist_name = %s;", (artist,))
            artist_id = cur.fetchone()[0]

            cur.execute('INSERT IGNORE INTO album(album_name, artist_id) VALUES (%s, %s)', (album, artist_id))
            cur.execute("SELECT id FROM album WHERE album_name = %s;", (album,))
            album_id = cur.fetchone()[0]

            cur.execute('INSERT IGNORE INTO genre(genre_name) VALUES (%s)', (genre,))
            cur.execute("SELECT id FROM genre WHERE genre_name = %s;", (genre,))
            genre_id = cur.fetchone()[0]

            cur.execute('INSERT IGNORE INTO track(title, album_id, genre_id, artist_id, rlsyr) VALUES (%s, %s, %s, %s, %s)',
                        (title, album_id, genre_id, artist_id, rlsyr))

            conn.commit()
            flash('Song added successfully', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f"Error: {str(e)}", 'error')

    return render_template('addsongs.html')



@app.route('/viewsongs')
def viewsongs():
    search_query = request.args.get('query', '')  # Get the search query from the request parameters
    try:
        if search_query:
            # If search query is provided, filter songs based on the query
            cur.execute("SELECT track.title, artist.artist_name, album.album_name, genre.genre_name, track.rlsyr FROM track JOIN album JOIN artist JOIN genre ON track.artist_id=artist.id AND track.album_id=album.id AND track.genre_id=genre.id WHERE track.title LIKE %s;", ('%' + search_query + '%',))
        else:
            # If no search query is provided, retrieve all songs
            cur.execute("SELECT track.title, artist.artist_name, album.album_name, genre.genre_name, track.rlsyr FROM track JOIN album JOIN artist JOIN genre ON track.artist_id=artist.id AND track.album_id=album.id AND track.genre_id=genre.id ORDER BY track.title;")
        
        rows = cur.fetchall()
        return render_template('viewsongs.html', songs=rows, search_query=search_query)
    except Exception as e:
        flash(f"Error: {str(e)}", 'error')
        return render_template('viewsongs.html', songs=[], search_query=search_query)

def get_playlists():
    # You can modify this function to retrieve the playlists from your database
    # For now, let's assume the playlists are hardcoded
    return ["Edm", "Indie", "Pop", "Rap"]

@app.route('/viewplaylists')
def view_playlists():
    playlists = get_playlists()
    return render_template('viewplaytist.html', playlists=playlists)

@app.route('/viewedm')
def view_edm():
    genre = "EDM"
    try:
        cur.execute("SELECT track.title, artist.artist_name, album.album_name, genre.genre_name, track.rlsyr FROM track JOIN album JOIN artist JOIN genre ON track.artist_id=artist.id AND track.album_id=album.id AND track.genre_id=genre.id WHERE genre.genre_name= %s;", (genre,))
        rows = cur.fetchall()
        conn.commit()
        return render_template('view_songs.html', songs=rows)
    except Exception as e:
        return render_template('error.html', error_message=str(e))

    # Modify this function to retrieve and display EDM playlist items
    

@app.route('/viewindie')
def view_indie():
    genre = "Indie"
    try:
        cur.execute("SELECT track.title, artist.artist_name, album.album_name, genre.genre_name, track.rlsyr FROM track JOIN album JOIN artist JOIN genre ON track.artist_id=artist.id AND track.album_id=album.id AND track.genre_id=genre.id WHERE genre.genre_name=%s;", (genre,))
        rows = cur.fetchall()
        conn.commit()
        return render_template('view_songs.html', songs=rows, genre=genre)
    except Exception as e:
        return f"Error: {str(e)}"
    # Modify this function to retrieve and display Indie playlist items

@app.route('/viewpop')
def view_pop():
    genre = "Pop"
    try:
        cur.execute("SELECT track.title, artist.artist_name, album.album_name, genre.genre_name, track.rlsyr FROM track JOIN album JOIN artist JOIN genre ON track.artist_id=artist.id AND track.album_id=album.id AND track.genre_id=genre.id WHERE genre.genre_name=%s;", (genre,))
        rows = cur.fetchall()
        conn.commit()
        return render_template('view_songs.html', songs=rows, genre=genre)
    except Exception as e:
        return f"Error: {str(e)}"

    # Modify this function to retrieve and display Pop playlist items

@app.route('/viewrap')
def view_rap():
    genre = "Rap"
    try:
        cur.execute("SELECT track.title, artist.artist_name, album.album_name, genre.genre_name, track.rlsyr FROM track JOIN album JOIN artist JOIN genre ON track.artist_id=artist.id AND track.album_id=album.id AND track.genre_id=genre.id WHERE genre.genre_name=%s;", (genre,))
        rows = cur.fetchall()
        conn.commit()
        return render_template('view_songs.html', songs=rows, genre=genre)
    except Exception as e:
        return f"Error: {str(e)}"
# Modify this function to retrieve and display Rap playlist items

if __name__ == '__main__':
    app.run(debug=True)



