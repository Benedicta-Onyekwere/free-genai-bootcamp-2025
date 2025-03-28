from youtube_transcript_api import YouTubeTranscriptApi
from typing import List, Dict, Optional
import re
import os

class YouTubeTranscriptDownloader:
    def __init__(self):
        # Get the absolute path to the backend directory
        self.backend_dir = os.path.dirname(os.path.abspath(__file__))
        self.transcripts_dir = os.path.join(self.backend_dir, "transcripts")
        # Create transcripts directory if it doesn't exist
        os.makedirs(self.transcripts_dir, exist_ok=True)
        
    def extract_video_id(self, url: str) -> str:
        """Extract video ID from YouTube URL."""
        patterns = [
            r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
            r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        raise ValueError("Invalid YouTube URL")

    def get_transcript(self, url: str, languages: List[str] = ['ja']) -> List[Dict]:
        """Get transcript from YouTube video."""
        try:
            video_id = self.extract_video_id(url)
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
            if not transcript:
                raise ValueError("No transcript found for this video")
            return transcript
        except Exception as e:
            raise Exception(f"Error getting transcript: {str(e)}")

    def save_transcript(self, transcript: List[Dict], filename: str) -> bool:
        """
        Save transcript to file
        
        Args:
            transcript (List[Dict]): Transcript data
            filename (str): Output filename
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not transcript:
            raise ValueError("No transcript data to save")
            
        # Use absolute path for saving transcripts
        filepath = os.path.join(self.transcripts_dir, f"{filename}.txt")
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                for entry in transcript:
                    f.write(f"{entry['text']}\n")
            return True
        except Exception as e:
            raise Exception(f"Error saving transcript: {str(e)}")

def main(video_url, print_transcript=False):
    # Initialize downloader
    downloader = YouTubeTranscriptDownloader()
    
    try:
        # Get transcript
        transcript = downloader.get_transcript(video_url)
        
        if transcript:
            # Save transcript
            video_id = downloader.extract_video_id(video_url)
            if downloader.save_transcript(transcript, video_id):
                print(f"Transcript saved successfully to {video_id}.txt")
                # Print transcript if True
                if print_transcript:
                    for entry in transcript:
                        print(f"{entry['text']}")
            return transcript
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

if __name__ == "__main__":
    # Example video URL with Japanese content
    video_url = "https://www.youtube.com/watch?v=sY7L5cfCWno"
    transcript = main(video_url, print_transcript=True)