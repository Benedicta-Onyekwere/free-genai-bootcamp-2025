import os
import json
from datetime import datetime
from typing import Dict, List, Optional

class QuestionStore:
    def __init__(self, base_dir: str = "backend/data/generated_questions"):
        """Initialize the question store with a base directory."""
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)
    
    def save_questions(self, data: Dict, video_id: str) -> str:
        """Save generated questions with timestamp and video ID."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{video_id}_{timestamp}.json"
        filepath = os.path.join(self.base_dir, filename)
        
        # Add metadata to the questions
        metadata = {
            "video_id": video_id,
            "timestamp": timestamp,
            "practice_type": data.get("practice_type", "Unknown Practice"),
            "topic": data.get("topic", "Unknown Topic"),
            "questions": data.get("questions", data)  # Fallback to entire data if no questions key
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        return filename
    
    def delete_questions(self, filename: str) -> bool:
        """Delete a question file."""
        try:
            filepath = os.path.join(self.base_dir, filename)
            if os.path.exists(filepath):
                os.remove(filepath)
                return True
            return False
        except Exception as e:
            print(f"Error deleting questions: {str(e)}")
            return False
    
    def load_questions(self, filename: str) -> Optional[Dict]:
        """Load questions from a specific file."""
        filepath = os.path.join(self.base_dir, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Ensure the data has the expected structure
                if isinstance(data, dict):
                    return {
                        "video_id": data.get("video_id", "unknown"),
                        "timestamp": data.get("timestamp", ""),
                        "practice_type": data.get("practice_type", "Unknown Practice"),
                        "topic": data.get("topic", "Unknown Topic"),
                        "questions": data.get("questions", {})
                    }
                return None
        except Exception as e:
            print(f"Error loading questions: {str(e)}")
            return None
    
    def list_saved_questions(self) -> List[Dict]:
        """List all saved question files with metadata."""
        saved_questions = []
        
        for filename in os.listdir(self.base_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.base_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        saved_questions.append({
                            "filename": filename,
                            "video_id": data.get("video_id", "unknown"),
                            "timestamp": data.get("timestamp", ""),
                            "practice_type": data.get("practice_type", "Unknown Practice"),
                            "topic": data.get("topic", "Unknown Topic")
                        })
                except Exception as e:
                    print(f"Error reading {filename}: {str(e)}")
        
        # Sort by timestamp descending (newest first)
        saved_questions.sort(key=lambda x: x["timestamp"], reverse=True)
        return saved_questions 