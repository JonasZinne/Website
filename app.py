import os
from flask import Flask, render_template, request, redirect, url_for, send_file, session
from export_matches import main

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Startseite
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST" and "export_matches" in request.form:
        url = request.form['url']
        message, file_path = main(url)
        session['message'] = message
        session['file_path'] = file_path
        return redirect(url_for('result'))
    
    return render_template("index.html")

# Ergebnis-Seite
@app.route("/result")
def result():
    message = session.get('message', '')
    file_path = session.get('file_path', None)
    file_ready = file_path is not None
    return render_template("index.html", message=message, file_ready=file_ready, file_path=file_path)

# Download-Route
@app.route("/download")
def download_file():
    file_path = session.get('file_path')
    if file_path and os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "Datei nicht gefunden", 404
    
if __name__ == "__main__":
    app.run(debug=True)