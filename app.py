from flask import Flask, render_template, request, redirect, url_for, flash
from flask_pymongo import PyMongo

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a real secret key

# MongoDB Configuration
app.config["MONGO_URI"] = "mongodb+srv://saviosunny48:2TJsNwpNwqJX2aG3@cluster0.0zmwv1l.mongodb.net/donor_database"
mongo = PyMongo(app)
collection = mongo.db.donors  # Access the 'donors' collection

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/donor')
def donor():
    return render_template('donor.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form.get('Name')
        blood_group = request.form.get('Blood Group')
        gender = request.form.get('Sex')
        phone = request.form.get('Phone Number')
        district = request.form.get('District')
        
        # Store data in MongoDB
        collection.insert_one({
            'Name': name,
            'Blood Group': blood_group,
            'Sex': gender,
            'Phone Number': phone,
            'District': district
        })

        # Flash success message
        flash('Your donation information has been submitted successfully!', 'success')
        
        return redirect(url_for('home'))

@app.route('/request-page', methods=['GET', 'POST'])
def requests():
    if request.method == 'POST':
        blood_group = request.form.get('blood-group')
        district = request.form.get('district')
        
        # Query MongoDB
        query = {}
        if blood_group:
            query['Blood Group'] = blood_group
        if district:
            query['District'] = district

        results = collection.find(query)
        
        return render_template('request.html', donors=results)

    return render_template('request.html', donors=None)

if __name__ == '__main__':
    app.run(debug=True)
