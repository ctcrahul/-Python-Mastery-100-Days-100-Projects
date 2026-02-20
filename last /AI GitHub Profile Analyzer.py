import requests
from flask import Flask, request, jsonify
import statistics

app = Flask(__name__)

GITHUB_API = "https://api.github.com/users/"

def get_user_data(username):
    user = requests.get(GITHUB_API + username).json()
    repos = requests.get(GITHUB_API + username + "/repos").json()
    return user, repos

def analyze_profile(user, repos):

    repo_count = len(repos)

    stars = [repo['stargazers_count'] for repo in repos]
    forks = [repo['forks_count'] for repo in repos]
    languages = [repo['language'] for repo in repos if repo['language']]

    total_stars = sum(stars)
    total_forks = sum(forks)
    unique_languages = len(set(languages))

    avg_stars = statistics.mean(stars) if stars else 0

    consistency_score = min(repo_count * 2, 100)
    complexity_score = min(total_stars + total_forks, 100)
    diversity_score = min(unique_languages * 10, 100)

    final_score = (consistency_score + complexity_score + diversity_score) / 3
