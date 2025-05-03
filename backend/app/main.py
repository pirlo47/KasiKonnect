import webbrowser
from flask import Flask, render_template    

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("login.html")  # Change this to "signup.html" if you prefer

if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000")  # Opens browser automatically
    app.run(debug=True)