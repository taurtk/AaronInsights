from flask import Flask, render_template, request, jsonify, session
from utils.reddit_client import RedditClient
from utils.quora_client import QuoraClient
from utils.deepseek_client import DeepSeekClient
from utils.users import add_user, init_db
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Initialize components
reddit_client = RedditClient()
quora_client = QuoraClient()
deepseek_client = DeepSeekClient()

# Initialize the database
with app.app_context():
    init_db()

@app.route('/')
def index():
    if 'user_email' not in session:
        return render_template('signup.html')
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form.get('email')
    if email:
        add_user(email)
        session['user_email'] = email
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Invalid email'})

@app.route('/generate_ideas', methods=['POST'])
def generate_ideas():
    if 'user_email' not in session:
        return jsonify({'success': False, 'error': 'User not on waitlist'})

    prompt = request.form.get('prompt')
    if not prompt:
        return jsonify({'success': False, 'error': 'Prompt is required'})

    try:
        queries = deepseek_client.generate_search_queries(prompt)
        if not queries['subreddits'] and not queries['quora']:
            return jsonify({'success': False, 'error': 'Failed to generate search queries.'})

        reddit_data = reddit_client.fetch_subreddit_data(queries['subreddits'])
        quora_data = quora_client.fetch_quora_data(queries['quora'])
        combined_data = reddit_data + quora_data

        enriched_ideas = deepseek_client.generate_enriched_ideas(combined_data, 20, prompt)

        if enriched_ideas:
            clusters = {}
            for idea in enriched_ideas:
                key = idea.get('keywords')[0] if idea.get('keywords') else 'general'
                if key not in clusters:
                    clusters[key] = []
                clusters[key].append(idea)
            
            if not clusters:
                clusters = {'business_ideas': enriched_ideas}
            
            return jsonify({'success': True, 'clusters': clusters})
        else:
            return jsonify({'success': False, 'error': 'No data found for the given topic.'})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)