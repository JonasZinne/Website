import os
from flask import Flask, render_template, request, redirect, url_for, send_file, session
from export_matches import main

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Dashboard (Index)
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# Export Matches
@app.route("/export_matches", methods=["GET", "POST"])
def export_matches():
    message = None
    file_path = None
    
    if request.method == "POST":
        url = request.form['url']
        message, file_path = main(url)
        
        session['message'] = message
        session['file_path'] = file_path
    
    return render_template("export_matches.html", message=message, file_ready=(file_path is not None))

# Download der Datei
@app.route("/download_matches")
def download_matches():
    file_path = session.get('file_path')
    
    if file_path and os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "Datei nicht gefunden", 404

# Turnier anlegen
@app.route("/create_tournament", methods=["GET"])
def create_tournament():
    return render_template("create_tournament.html")

if __name__ == "__main__":
    app.run(debug=True)