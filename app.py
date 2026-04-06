from cs50 import SQL
import sqlite3
# import kagglehub
from flask import Flask, flash, redirect, url_for, render_template, request, session
import csv
from helpers import lookup

app = Flask(__name__)
app.secret_key = "Logos4U"
conn = sqlite3.connect("logos.db")
cursor = conn.cursor()
# path = kagglehub.dataset_download("kkhandekar/popular-brand-logos-image-dataset")

logo_database = cursor.execute("CREATE TABLE IF NOT EXISTS logos("
                    "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                    "name TEXT NOT NULL,"
                    "designer TEXT, "
                    "year INTEGER, "
                    "image_path TEXT, "
                    "UNIQUE (name COLLATE NOCASE)"
                    ");")

yd = {}
# dictionary of dictionaries or companies each with its name, designer, year, image_path info
logos = []
name_to_path = {}

# csv file with image path
with open("LogoDatabase.csv", "r", encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        name_to_path[row['logoName']] = row['fileName']

#Populate the database with the needed data (name,design, year, image_path)

#csv file without image path, has the info needed for logos.db in correct format, except id and image_path
with open("Logo_database.csv", "r", newline='') as file:
    reader2 = csv.DictReader(file)
    for logo in reader2:
        logo_name = logo['name']
        image_path = name_to_path.get(logo_name)
        if logo_name in name_to_path:
            yd[logo_name] = {
                'name': logo_name,
                'designer': logo['designer'],
                'year': int(logo['year']),
                'image_path': image_path
            }
logos = [(data['name'], data['designer'], data['year'], data['image_path']) for data in yd.values() if data['name'] not in logos]
cursor.executemany("INSERT INTO logos (name, designer, year, image_path) VALUES (?, ?, ?, ?)", logos)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        logo_name = request.form.get("logo_name") #Get the logo the user requested from the form
        #Checking if the requested logo is available in the list of stored logos. helper function

        #TODO : Look for the name brand in the database
        conn = sqlite3.connect("logos.db")
        cursor = conn.cursor()

        if lookup(logo_name) != None:
            logo_name = lookup(logo_name)
            cursor.execute("SELECT name, designer, year, image_path FROM logos WHERE UPPER(name) LIKE UPPER(?)", (f"%{logo_name}%",))
            result = cursor.fetchone()
            conn.close()


            return render_template("index.html", result=result, logo_name=logo_name)
    return render_template("index.html")


@app.route("/search")
def results():
    return render_template("/search.html", result=None, logo_name="")
    # return render_template("/search.html")


conn.commit()
conn.close()




