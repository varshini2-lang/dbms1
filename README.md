# Music Library Management System


This project is a Music Library Management System implemented using Flask, a Python web framework. It allows users to manage music tracks, artists, albums, genres, and playlists.

**Features**
User Authentication: Users can register, login, and logout securely. Authentication is implemented using Flask-Login.

CRUD Operations: Users can perform CRUD (Create, Read,Update, Delete) operations on music tracks, artists, albums, and genres.

Search Functionality: Users can search for music tracks by title, artist, album, or genre.

Playlist Management: Users can view playlists and explore tracks based on genres like EDM, Indie, Pop, and Rap.

Error Handling: Comprehensive error handling to provide feedback to users in case of any issues.

**Technologies Used:**

Flask: Web framework used for backend development.
MySQL: Database management system for storing music-related data.
Flask-Login: Extension for handling user authentication.
HTML/CSS: Frontend templates and styling.
Python: Programming language used for backend logic.


**Setup**

Clone the repository:
git clone https://github.com/varshini2-lang/dbms1

**Install dependencies:**

pip install -r requirements.txt

Set up your MySQL database. 

Configure your database connection in app.py:


db_config = {
    'host': 'localhost', 
    'user': 'your_username',
    'password': 'your_password',
    'database': 'your_database_name'
}


**Run the application:**


python app.py
Access the application in your web browser at http://localhost:5000.

## Images
**Login page** :

![loginpage](https://github.com/varshini2-lang/dbms1/assets/145186068/eeae978c-67b9-4c0e-8c70-a361f4a1b158)

**Home Page**:
![home](https://github.com/varshini2-lang/dbms1/assets/145186068/0772fbba-273f-46e2-917b-1ddcb2000c0b) 

**Add Song Page**:
![addsongs](https://github.com/varshini2-lang/dbms1/assets/145186068/63fe40e4-1d82-4498-9b88-bcf4f571f4b4)

**Delete Page**:
![delete](https://github.com/varshini2-lang/dbms1/assets/145186068/4e0c6885-650f-4e8e-be2e-566e0fc641f9)

**View Songs Page**:
![viewsongs](https://github.com/varshini2-lang/dbms1/assets/145186068/22780ea5-cdcb-41ce-9203-cca23ff58b80)


**User Dashboard:**
![userdashboard](https://github.com/varshini2-lang/dbms1/assets/145186068/18a0e4c1-32fd-4ab6-bf39-7f208d1085e4)

**View playlist**:
![viewplaylist](https://github.com/varshini2-lang/dbms1/assets/145186068/1ddd362f-1d07-46d3-b64b-a4d6b9c84e6c)

**Usage**

Upon accessing the application, users will be prompted to register or login.
After logging in, users can add, view, update, or delete music tracks, artists, albums, and genres.
Users can also explore playlists based on different genres.

**Contributors**

* Varshini (@varshini2-lang)
* Prashita
* Shikha(@Shikhaaax)
 
