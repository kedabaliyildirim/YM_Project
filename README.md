# YM_Project

First and foremost switch to test branch

        git checkout test

if you have local changes look below

you can use

        git pull origin test

or if you are using Vscode you can switch from the bottom left corner to test branch and pull from there

# IMPORTANT

If you have local changes and want to pull from git use

        git stash

first OR YOU WILL LOSE YOUR LOCAL CHANGES
after pulling from git use

        git stash apply

to get your local changes back after that you can merge the changes and push to git

in Github Desktop you can stash and apply from the GUI.

to clone

        git clone https://github.com/kedabaliyildirim/YM_Project.git .

After cloning the repo, create a virtual environment and activate it

        .\w2w\Scripts\activate

to install requirements
use

        pip install -r requirements.txt

# Environment Variables

.env file is in the google drive @vakkaskarakurt shared the files with everyone copy the .env file because it is in the drive its name changes to env put a (.) dot in front of it, copy it to the root directory of the project

# Server

.vercel file is not on github get it from the Google Drive, unzip it paste it to root directory of the project like .env filename

to run locally use

        python manage.py runserver

if installed any new packages use

        pip freeze > requirements.txt

to push to git use

        git add .
        git commit -m "commit message"
        git push origin test

always push to test branch first, merge will be done by @kedabaliyildirim

# The Project

## The project is mainly two parts this part is the backend part

### The backend part is a Django project

The project codes are inside wort2watch folder the other folders are created by Django, vercel, git, or venv

inside the wort2watch folder there are two important py files and 2 folders

## Files

### urls.py file

this file is the main urls file of the project, the front end makes requests to the urls in this file
the urls in this file runs the functions in the views.py file

### views.py file

is entry point of the backend, the urls.py file runs the functions in this file
the functions in this file are the main functions of the backend and uses multiple files and functions the main point is

        @csrf_exempt
        @require_POST

these two lines are important because they allow the front end to make requests to the backend.

# Folders

## Database folder

everything to do with the database is in this folder, the database is a NOSQL database with mongodb

DatabaseInitiation.py file is the file that creates the database and the collections in the database

content folder is the folder that contains various functions of movies, both getting and setting data to the database and getting data from the API is done in this folder

### admin folder

this folder contains the admin panel of the project, the admin panel is used to log in to the project and to add new movies to the database or delete movies from the database ATM

### comment_db

will be the main agent of the project, it will pull comments from web and add them to the database, pre-processing will be done after the comments are added to the database will be done in a different folder

## Users folder

users folder only contains admin folder, admin folder is the login operations of the admins
