from flask import Flask, session, request, Response, g, redirect, url_for, abort, render_template, flash, make_response
from pathlib import Path
from werkzeug.utils import secure_filename
from datetime import datetime
import sqlite3 as sql
import os

app = Flask(__name__)
app.config.from_pyfile('config.py')

def allowed_image(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

def allowed_image_filesize(filesize):
    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False

def upload_image(request):
    if not allowed_image_filesize(request.cookies["filesize"]):
        print("Filesize exceeded maximum limit")
        return "ERR_FileSize", None
    
    image = request.files["image"]

    if image.filename == "":
        print("No filename")
        # Return "ERR_NoFile" if required
        return "SUCCES", None

    if allowed_image(image.filename):
        now = datetime.now()
        filename = now.strftime('%Y%m%d%H%M%S%f%z.png')
        image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
        print("Image saved")
        return "SUCCES", filename

    else:
        print("That file extension is not allowed")
        return "ERR_FileInvalid", None

@app.route('/view/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='img/uploads/' + filename), code=301)


def error_messages(i):
    switcher={
        "ERR_FileSize":"Filesize exceeded maximum limit",
        "ERR_NoFile":"No filename",
        "ERR_FileInvalid":"That file extension is not allowed",
        "ERR_DB_Insert":"An error occurred in the Insert operation",
        "ERR_Required_Not_Filled":"Not all required fields are filled"
    }
    return switcher.get(i,"Unknown error")

# PAGES
@app.route('/')
def index():

    return render_template('home/home.html')

@app.route('/test')
def test():

    return render_template('test.html')

@app.route('/posts')
def posts():
    try:
        con = sql.connect("database.db")
        con.row_factory = sql.Row

        cur = con.cursor()
        cur.execute("SELECT * FROM posts ORDER BY id DESC")

        rows = cur.fetchall()
    except:
        rows = None
    finally:
        return render_template('posts/post_overview.html', rows = rows)

@app.route("/posts/new", methods=["GET", "POST"])
def postnew():
    errormessage = ""
    if request.method == "POST":
        try:
            title = request.form['title']
            content = request.form['content']

            if title == "" or content == "":
                feedback = "ERR_Required_Not_Filled"
                errormessage = error_messages(feedback)
                return render_template("posts/post_new.html", error = errormessage)

            if request.files:
                (feedback,filename) = upload_image(request)
            else:
                feedback = "SUCCES"
            
            if feedback == "SUCCES":
                with sql.connect("database.db") as con:
                    cur = con.cursor()
                    cur.execute("INSERT INTO posts (title,content,img) VALUES (?,?,?)",(title,content,filename) )

                    con.commit()
                    print("Record successfully added")
                    cur.close()
                return redirect(url_for('posts'))
            else:
                errormessage = error_messages(feedback)
                return render_template("posts/post_new.html", error = errormessage)
        except:
            con.rollback()
            print("error in insert operation")
            feedback = "ERR_DB_Insert"
        finally:
            try:
                con.close()
            except:
                print("Connection already closed")
            
            errormessage = error_messages(feedback)

    return render_template("posts/post_new.html", error = errormessage)

# ERROR PAGES
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404

@app.errorhandler(403)
def page_forbidden(e):
    return render_template('error/403.html'), 403

@app.errorhandler(410)
def page_gone(e):
    return render_template('error/410.html'), 410

@app.errorhandler(500)
def page_internal_server_error(e):
    return render_template('error/500.html'), 500

@app.route('/404')
def page_not_found_test():
    return render_template('error/404.html')

@app.route('/403')
def page_forbidden_test():
    return render_template('error/403.html')

@app.route('/410')
def page_gone_test():
    return render_template('error/410.html')

@app.route('/500')
def page_internal_server_error_test():
    return render_template('error/500.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)