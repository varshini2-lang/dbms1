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

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        title = request.form['title']

        try:
            cur.execute("DELETE FROM track, album, artist USING track JOIN album JOIN artist ON track.artist_id=artist.id AND track.album_id=album.id WHERE track.title = %s;", (title,))
            conn.commit()
            if cur.rowcount > 0:
                conn.commit()
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
    try:
        cur.execute("SELECT track.title, artist.artist_name, album.album_name, genre.genre_name, track.rlsyr FROM track JOIN album JOIN artist JOIN genre ON track.artist_id=artist.id AND track.album_id=album.id AND track.genre_id=genre.id ORDER BY track.title;")
        rows = cur.fetchall()
        return render_template('viewsongs.html', songs=rows)
    except Exception as e:
        flash(f"Error: {str(e)}", 'error')
        return render_template('viewsongs.html', songs=[])

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



