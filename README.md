# lezeckybazar.cz

Hello there! Welcome in my repository.This is my fully working prototype of online second hand insert Web App made for climbing community.
I created also page for public API, which can be used for example to create mobile APP. 
I was looking for a new project and i found out, there is no insert web app for climbing in Czech republic, so i decided to create it. 

<p>Users are able to insert their climbing equipment(including photos) and delete them (after selling) - USER WANTS TO SELL </p>
<p>Users are able to view and filter offers of users, who wants to sell. You can filter by near city and category. Multiple combinations possible - USER WANTS TO BUY </p>

Used technologies: Python, Flask, SqlAlchemy, SQLite, HTML, CSS


Requirements to run project:

1. Python installed - https://www.python.org/downloads/
2. Flask installed - pip(3) install Flask (terminal)
3. SQLAlchemy - pip(3) install flask-sqlalchemy (terminal)

How to run:

0. Go to bazar.py and go to line 29 and then relocate your UPLOAD FOLDER (you need to write location, where is folder in your computer)
1. go to your terminal and go for project folder
2. enter this to your terminal and confirm: FLASK_APP=bazar.py flask run
3. terminal will show you local host adress and you are able to run APP in your browser
