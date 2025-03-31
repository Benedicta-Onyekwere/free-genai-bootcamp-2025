from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import logging
import math
import argparse

# Set up argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--port', type=int, default=5000, help='Port to run the server on')

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": [
            "http://localhost:5173",  # React app
            "http://localhost:5174",  # Alternative React port
            "http://localhost:5175",  # Another alternative React port
            "http://localhost:5176",  # Another alternative React port
            "http://localhost:8501",  # Streamlit app
            "http://localhost:8082"   # Alternative Streamlit port
        ],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Store study activities (in-memory for now, replace with database later)
study_activities = []

# Initialize with some mock study sessions
study_sessions = [
    {
        'id': 1,
        'groupName': 'Core Verbs',
        'activityName': 'Adventure MUD',
        'startTime': '2024-03-20 14:30',
        'endTime': '2024-03-20 15:00',
        'reviewItemCount': 25
    },
    {
        'id': 2,
        'groupName': 'JLPT N5',
        'activityName': 'Typing Tutor',
        'startTime': '2024-03-19 10:15',
        'endTime': '2024-03-19 10:45',
        'reviewItemCount': 30
    }
]

@app.route('/', methods=['GET'])
def home():
    return "Flask server is running!"

@app.route('/api/study-activities', methods=['GET'])
def get_study_activities():
    app.logger.info('Received GET request for study activities')
    return jsonify(study_activities)

@app.route('/api/study-sessions', methods=['GET'])
def get_study_sessions():
    logger.info('Received GET request for study sessions')
    page = int(request.args.get('page', 1))
    per_page = 10
    
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    paginated_sessions = study_sessions[start_idx:end_idx]
    total_sessions = len(study_sessions)
    total_pages = math.ceil(total_sessions / per_page)
    
    logger.info(f'Returning {len(paginated_sessions)} sessions (page {page} of {total_pages})')
    logger.info(f'Total sessions in memory: {len(study_sessions)}')
    
    return jsonify({
        'data': paginated_sessions,
        'total': total_sessions,
        'page': page,
        'per_page': per_page
    })

@app.route('/api/study-activities', methods=['POST'])
def create_study_activity():
    activity = request.json
    activity['id'] = len(study_activities) + 1
    activity['timestamp'] = datetime.now().isoformat()
    study_activities.append(activity)
    return jsonify(activity), 201

@app.route('/api/writing-practice', methods=['POST'])
def save_writing_practice():
    practice_data = request.json
    logger.info('Received writing practice submission')
    
    # Add to study activities for the activity feed
    activity = {
        'id': len(study_activities) + 1,
        'type': 'writing_practice',
        'data': practice_data,
        'timestamp': datetime.now().isoformat()
    }
    study_activities.append(activity)
    
    # Add to study sessions in the expected format
    now = datetime.now()
    end_time = now
    start_time = now - timedelta(minutes=15)  # Assume 15 min duration
    
    session = {
        'id': len(study_sessions) + 1,
        'groupName': 'Writing Practice',
        'activityName': 'Japanese Writing Practice',
        'startTime': start_time.strftime('%Y-%m-%d %H:%M'),
        'endTime': end_time.strftime('%Y-%m-%d %H:%M'),
        'reviewItemCount': 1,  # One word/sentence practiced
        'practiceType': practice_data.get('practice_type', 'Sentence')  # Add practice type
    }
    study_sessions.append(session)
    logger.info(f'Added new session. Total sessions now: {len(study_sessions)}')
    
    return jsonify(activity), 201

@app.route('/api/dashboard/last_study_session', methods=['GET'])
def get_last_study_session():
    if not study_sessions:
        return jsonify(None)
    return jsonify(study_sessions[-1])

@app.route('/api/dashboard/study_progress', methods=['GET'])
def get_study_progress():
    # Calculate study progress for the last 7 days
    now = datetime.now()
    progress = []
    for i in range(7):
        date = now - timedelta(days=i)
        date_str = date.strftime('%Y-%m-%d')
        sessions_count = sum(1 for session in study_sessions 
                           if session['startTime'].startswith(date_str))
        progress.append({
            'date': date_str,
            'sessions': sessions_count
        })
    return jsonify(progress)

@app.route('/api/dashboard/quick-stats', methods=['GET'])
def get_quick_stats():
    total_sessions = len(study_sessions)
    total_items = sum(session['reviewItemCount'] for session in study_sessions)
    avg_items_per_session = total_items / total_sessions if total_sessions > 0 else 0
    
    return jsonify({
        'totalSessions': total_sessions,
        'totalReviewItems': total_items,
        'averageItemsPerSession': round(avg_items_per_session, 2)
    })

if __name__ == '__main__':
    args = parser.parse_args()
    port = args.port
    print("Starting Flask server...")
    print(f"Try accessing:")
    print(f"  - http://127.0.0.1:{port}")
    print(f"  - http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=True) 