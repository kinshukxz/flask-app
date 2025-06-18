from flask import Flask, jsonify, render_template, request, redirect, url_for
import json
import pymongo
from bson import json_util

app = Flask(__name__)

# ✅ MongoDB Atlas Connection (correct URI inserted)
client = pymongo.MongoClient("mongodb+srv://kinshuksriv9191:5XzuUyvpg8Y3JMdN@kinshuk-cluster.jxhbz9a.mongodb.net/?retryWrites=true&w=majority")
db = client["mydatabase"]
collection = db["users"]

# ✅ API Route - Serves local JSON data
@app.route('/api', methods=['GET'])
def api():
    with open('data.json') as f:
        data = json.load(f)
    return jsonify(data)

# ✅ Form Page + Form Handling
@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        try:
            name = request.form['name']
            city = request.form['city']
            if name and city:
                collection.insert_one({"name": name, "city": city})
                return redirect(url_for('success'))
            else:
                error = "Please fill all fields."
        except Exception as e:
            error = str(e)
    return render_template('form.html', error=error)

# ✅ Success Page
@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
