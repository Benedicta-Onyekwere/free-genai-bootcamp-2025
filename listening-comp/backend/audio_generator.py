import os
import json
import boto3
from typing import List, Dict
import openai
from dotenv import load_dotenv
import subprocess
import tempfile
from pathlib import Path

# Load environment variables
load_dotenv()

class AudioGenerator:
    def __init__(self):
        """Initialize the audio generator with AWS Polly and OpenAI clients"""
        self.polly = boto3.client('polly')
        self.openai = openai
        self.openai.api_key = os.getenv('OPENAI_API_KEY')
        
        # Create audio output directory if it doesn't exist
        self.audio_dir = Path("backend/data/generated_audio")
        self.audio_dir.mkdir(parents=True, exist_ok=True)
        
        # Define voice mappings
        self.voice_mappings = {
            "male": ["Takumi", "Tomoko"],  # Japanese male voices
            "female": ["Mizuki", "Kazuha"],  # Japanese female voices
            "announcer": "Takumi"  # Default announcer voice
        }
    
    def _get_voice_for_speaker(self, speaker: str, used_voices: List[str]) -> str:
        """Get an appropriate voice for a speaker based on their role and gender"""
        if speaker.lower() == "announcer":
            return self.voice_mappings["announcer"]
        
        # Determine gender from speaker name or role
        gender = "male"
        if any(term in speaker.lower() for term in ["woman", "girl", "female", "mother", "sister", "ms.", "mrs.", "miss"]):
            gender = "female"
        
        # Get available voices for the gender
        available_voices = [v for v in self.voice_mappings[gender] if v not in used_voices]
        if not available_voices:
            available_voices = self.voice_mappings[gender]  # Reuse voices if all are taken
        
        selected_voice = available_voices[0]
        used_voices.append(selected_voice)
        return selected_voice

    def _text_to_speech(self, text: str, voice_id: str, output_path: str) -> bool:
        """Convert text to speech using Amazon Polly"""
        try:
            response = self.polly.synthesize_speech(
                Text=text,
                OutputFormat='mp3',
                VoiceId=voice_id,
                Engine='neural'
            )
            
            # Save the audio stream to a file
            if "AudioStream" in response:
                with open(output_path, 'wb') as file:
                    file.write(response['AudioStream'].read())
                return True
        except Exception as e:
            print(f"Error in text_to_speech: {str(e)}")
            return False
        return False

    def _combine_audio_files(self, audio_files: List[str], output_path: str) -> bool:
        """Combine multiple audio files into one using ffmpeg"""
        try:
            # Create a file list for ffmpeg
            with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as f:
                for audio_file in audio_files:
                    f.write(f"file '{audio_file}'\n")
                file_list = f.name

            # Combine audio files
            subprocess.run([
                'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
                '-i', file_list,
                '-c', 'copy',
                output_path
            ], check=True)

            # Clean up the temporary file list
            os.unlink(file_list)
            
            # Clean up individual audio files
            for file in audio_files:
                os.unlink(file)
                
            return True
        except Exception as e:
            print(f"Error in combine_audio_files: {str(e)}")
            return False

    def generate_audio(self, question_data: Dict) -> str:
        """Generate audio for a question set"""
        try:
            # Create a temporary directory for intermediate files
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_dir = Path(temp_dir)
                audio_files = []
                used_voices = []
                
                # Generate intro
                intro_text = f"Welcome to this {question_data['practice_type']} practice session about {question_data['topic']}."
                intro_path = temp_dir / "intro.mp3"
                self._text_to_speech(intro_text, self.voice_mappings["announcer"], str(intro_path))
                audio_files.append(str(intro_path))
                
                # Generate scenario introduction
                scenario_text = question_data['questions']['scenario']
                scenario_path = temp_dir / "scenario.mp3"
                self._text_to_speech(scenario_text, self.voice_mappings["announcer"], str(scenario_path))
                audio_files.append(str(scenario_path))
                
                # Generate dialogue
                for i, line in enumerate(question_data['questions']['dialogue']):
                    voice = self._get_voice_for_speaker(line['speaker'], used_voices)
                    line_path = temp_dir / f"line_{i}.mp3"
                    self._text_to_speech(line['text'], voice, str(line_path))
                    audio_files.append(str(line_path))
                
                # Generate question
                question_path = temp_dir / "question.mp3"
                self._text_to_speech(question_data['questions']['question'], self.voice_mappings["announcer"], str(question_path))
                audio_files.append(str(question_path))
                
                # Generate options
                for i, option in enumerate(question_data['questions']['options']):
                    option_text = f"Option {i + 1}: {option}"
                    option_path = temp_dir / f"option_{i}.mp3"
                    self._text_to_speech(option_text, self.voice_mappings["announcer"], str(option_path))
                    audio_files.append(str(option_path))
                
                # Combine all audio files
                timestamp = question_data.get('timestamp', '')
                output_filename = f"{question_data['video_id']}_{timestamp}_audio.mp3"
                output_path = self.audio_dir / output_filename
                
                if self._combine_audio_files(audio_files, str(output_path)):
                    return str(output_path)
                
        except Exception as e:
            print(f"Error in generate_audio: {str(e)}")
        
        return "" 