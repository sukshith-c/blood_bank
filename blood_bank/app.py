from flask import Flask, render_template, request
from db import blood_inventory, blood_banks, donors, requests

app = Flask(__name__)


# ------------------ HOME ------------------
@app.route('/')
def home():
    return render_template('index.html')


# ------------------ ADD BLOOD BANK ------------------
@app.route('/add_bank', methods=['GET', 'POST'])
def add_bank():
    if request.method == 'POST':
        blood_banks.insert_one({
            "name": request.form['name'],
            "location": request.form['location']
        })
        return "<h3>Blood Bank Added Successfully</h3><a href='/'>Go Back</a>"

    return render_template('add_bank.html')


# ------------------ ADD DONAR ------------------
@app.route('/add_donor', methods=['GET', 'POST'])
def add_donor():
    if request.method == 'POST':
        name = request.form['name']
        blood_group = request.form['blood_group']
        location = request.form['location']

        donors.insert_one({
            "name": name,
            "blood_group": blood_group,
            "location": location
        })

        return "<h3>Donor Added Successfully</h3><a href='/'>Go Back</a>"

    return render_template('add_donor.html')

# ------------------ ADD INVENTORY ------------------
@app.route('/add_inventory_page', methods=['GET', 'POST'])
def add_inventory_page():
    if request.method == 'POST':
        blood_inventory.insert_one({
            "blood_group": request.form['blood_group'],
            "units": int(request.form['units']),
            "location": request.form['location']
        })
        return "<h3>Inventory Added Successfully</h3><a href='/'>Go Back</a>"

    return render_template('add_inventory.html')


# ------------------ SEARCH BLOOD ------------------
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        group = request.form['blood_group']
        results = list(blood_inventory.find({"blood_group": group}))

        return render_template('search.html', data=results, group=group)

    return render_template('search.html', data=None)


# ------------------ REQUEST BLOOD ------------------
@app.route('/request', methods=['GET', 'POST'])
def request_blood():
    if request.method == 'POST':
        group = request.form['blood_group']
        units_needed = int(request.form['units'])

        blood = blood_inventory.find_one({"blood_group": group})

        if blood and blood["units"] >= units_needed:

            blood_inventory.update_one(
                {"_id": blood["_id"]},
                {"$set": {"units": blood["units"] - units_needed}}
            )

            requests.insert_one({
                "blood_group": group,
                "units": units_needed,
                "status": "Approved"
            })

            return render_template(
                "result.html",
                blood_group=group,
                units=units_needed,
                status="Approved"
            )

        else:
            requests.insert_one({
                "blood_group": group,
                "units": units_needed,
                "status": "Pending"
            })

            return render_template(
                "result.html",
                blood_group=group,
                units=units_needed,
                status="Pending"
            )

    return render_template('request.html')


# ------------------ RUN SERVER ------------------
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)