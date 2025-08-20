# Local Setup Instructions

## Prerequisites
- Python 3.11 or higher
- pip (Python package installer)

## Required Packages
```bash
# Core dependencies
streamlit==1.31.1
pandas==2.2.0
nltk==3.8.1
plotly==5.18.0
praw==7.7.1
openai==1.12.0

# Additional dependencies
python-dotenv==1.0.0
```

## Setup Steps

1. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in your project root with the following variables:
```
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
```

To get Reddit API credentials:
1. Go to https://www.reddit.com/prefs/apps
2. Create a new application
3. Select "script" as the application type
4. Note down the client ID and client secret

## Running the Application

1. Make sure your virtual environment is activated (if using one)

2. Start the Streamlit server:
```bash
streamlit run app.py
```

3. Open your browser and navigate to:
```
http://localhost:8501
```

4. Login credentials:
- Username: aaron
- Password: 

## Directory Structure
```
├── app.py                 # Main application file
├── components/           # UI components
├── utils/               # Utility modules
└── .streamlit/          # Streamlit configuration
```

## Troubleshooting

1. If you encounter NLTK data errors, run these commands in Python:
```python
import nltk
nltk.download('punkt')
nltk.download('vader_lexicon')
nltk.download('stopwords')
```

2. If you see DeepSeek API errors, ensure you're using the correct base URL and API key in the DeepSeek client configuration.

3. For Reddit API rate limiting issues, try reducing the number of posts fetched in the sidebar settings.
