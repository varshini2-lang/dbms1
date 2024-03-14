import mysql.connector

mypass = "arrow@7501"
mydatabase = "varshini"

con = mysql.connector.connect(host="localhost", user="root", password=mypass, database=mydatabase)
cur = con.cursor()

def create_tables():
    try:
        # Create Artist Table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS artist (
                id INT AUTO_INCREMENT PRIMARY KEY,
                artist_name VARCHAR(255) UNIQUE
            )
        ''')

        # Create Album Table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS album (
                id INT AUTO_INCREMENT PRIMARY KEY,
                album_name VARCHAR(255) UNIQUE,
                artist_id INT,
                FOREIGN KEY (artist_id) REFERENCES artist(id)
            )
        ''')

        # Create Genre Table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS genre (
                id INT AUTO_INCREMENT PRIMARY KEY,
                genre_name VARCHAR(255) UNIQUE
            )
        ''')

        # Create Track Table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS track (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255),
                album_id INT,
                genre_id INT,
                artist_id INT,
                rlsyr INT,
                FOREIGN KEY (album_id) REFERENCES album(id),
                FOREIGN KEY (genre_id) REFERENCES genre(id),
                FOREIGN KEY (artist_id) REFERENCES artist(id)
            )
        ''')

        # Create Login Table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS login (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE,
                password VARCHAR(255),
                role ENUM('manager', 'user') DEFAULT 'user'
            )
        ''')
        insert_manager('divya', 'password1')

        con.commit()
        print("Tables created successfully.")
    except Exception as e:
        print(f"Error: {str(e)}")

def insert_manager(username, password):
    try:
        cur.execute('''
            INSERT INTO login (username, password, role)
            VALUES (%s, %s, 'manager')
        ''', (username, password))
        print("Manager details inserted successfully.")
    except Exception as e:
        print(f"Error inserting manager details: {str(e)}")

if __name__ == "__main__":
    create_tables()
    cur.close()
    con.close()
