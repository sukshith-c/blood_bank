from flask import Flask, render_template, request
from db import collection

app = Flask(__name__)

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Add blood data
@app.route('/add', methods=['POST'])
def add():
    blood_group = request.form['blood_group']
    units = request.form['units']
    location = request.form['location']

    collection.insert_one({
        "blood_group": blood_group,
        "units": int(units),
        "location": location
    })

    return "Blood data added successfully! <br><a href='/'>Go Back</a>"

# Search blood
@app.route('/search', methods=['POST'])
def search():
    group = request.form['blood_group']

    results = collection.find({"blood_group": group})

    return render_template('search.html', data=results)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)