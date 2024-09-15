from flask import Flask, render_template, request
from queens_matches import main

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    if request.method == "POST":
        if "button1" in request.form:
            message = main()
    return render_template("index.html", message=message)

if __name__ == "__main__":
    app.run(debug=True)
