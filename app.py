from flask import Flask, render_template, request, redirect, url_for, flash
import os
import requests

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'devsecret')
RECOMMENDER_URL = os.environ.get('RECOMMENDER_URL', 'https://job-recommender-fastapi-flask.onrender.com')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    name = request.form.get('name', 'Anonymous')
    skills = request.form.get('skills', '')
    skills_list = [s.strip().lower() for s in skills.split(',') if s.strip()]
    if not skills_list:
        flash('Please enter at least one skill (comma separated).')
        return redirect(url_for('index'))

    payload = {
        'name': name,
        'skills': skills_list
    }
    try:
        resp = requests.post(f'{RECOMMENDER_URL}/recommend', json=payload, timeout=180)
        resp.raise_for_status()
    except Exception as e:
        flash('Failed to get recommendations: ' + str(e))
        return redirect(url_for('index'))

    data = resp.json()
    return render_template('profile.html', profile=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
