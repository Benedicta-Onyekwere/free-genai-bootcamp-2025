"""Tool for generating unique song IDs."""

import hashlib
import re
from typing import Optional

def normalize_string(s: str) -> str:
    """Normalize a string by removing special characters and converting to lowercase."""
    # Remove special characters and convert to lowercase
    return re.sub(r'[^\w\s]', '', s.lower())

def generate_song_id(title: str, artist: str, language: Optional[str] = None) -> str:
    """Generate a unique ID for a song based on title and artist.
    
    Args:
        title: The song title
        artist: The artist name
        language: Optional language code (e.g., 'ja' for Japanese)
    
    Returns:
        A unique string identifier for the song
    """
    # Normalize inputs
    normalized_title = normalize_string(title)
    normalized_artist = normalize_string(artist)
    
    # Create base string for hashing
    base_string = f"{normalized_title}:{normalized_artist}"
    if language:
        base_string = f"{base_string}:{language}"
    
    # Generate hash
    hash_obj = hashlib.sha256(base_string.encode('utf-8'))
    full_hash = hash_obj.hexdigest()
    
    # Return first 12 characters as ID
    return full_hash[:12] 