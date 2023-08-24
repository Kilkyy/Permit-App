from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Sample data for work permit requests
permit_requests = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' in session:
        if request.method == 'POST':
            name = request.form['name']
            permit_requests.append({"name": name, "timestamp": datetime.now(), "status": "Pending"})
        return render_template('request.html')
    return redirect(url_for('login'))

@app.route('/responses', methods=['GET', 'POST'])
def responses():
    if 'username' in session:
        if request.method == 'POST':
            name = request.form['name']
            status = request.form['status']
            for request in permit_requests:
                if request['name'] == name:
                    request['status'] = status
                    request['response_timestamp'] = datetime.now()
                    break
        return render_template('responses.html', permit_requests=permit_requests)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
