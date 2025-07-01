from flask import Flask, render_template, request
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

app = Flask(__name__)

# Sample job listings and user profiles
jobs = [
    {"id": 1, "title": "Software Engineer", "skills": ["Python", "Django", "JavaScript"]},
    {"id": 2, "title": "Data Scientist", "skills": ["Python", "Machine Learning", "Statistics"]},
    {"id": 3, "title": "Web Developer", "skills": ["HTML", "CSS", "JavaScript"]},
]

@app.route('/')
def index():
    return render_template('index.html', jobs=jobs)

@app.route('/match', methods=['POST'])
def match():
    user_skills = request.form.get('skills').split(',')
    user_vector = np.array([1 if skill.strip() in user_skills else 0 for job in jobs for skill in job['skills']])
    
    job_vectors = []
    for job in jobs:
        job_vector = np.array([1 if skill in job['skills'] else 0 for skill in job['skills']])
        job_vectors.append(job_vector)
    
    job_vectors = np.array(job_vectors)
    similarities = cosine_similarity([user_vector], job_vectors)[0]
    
    matched_jobs = sorted(zip(jobs, similarities), key=lambda x: x[1], reverse=True)
    
    return render_template('index.html', jobs=matched_jobs)

if __name__ == '__main__':
    app.run(debug=True)
