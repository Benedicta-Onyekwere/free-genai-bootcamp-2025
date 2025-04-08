"""Tool for saving song lyrics and vocabulary to the database."""

from typing import List, Dict, Any
import aiosqlite
import json
from datetime import datetime
import logging

logger = logging.getLogger('song_vocab')

async def save_results(song_id: str, lyrics: str, vocabulary: List[Dict[str, Any]]) -> bool:
    """Save song lyrics and vocabulary to the database.
    
    Args:
        song_id: Unique identifier for the song
        lyrics: Complete lyrics text
        vocabulary: List of vocabulary items with their details
    
    Returns:
        bool: True if save was successful, False otherwise
    """
    try:
        async with aiosqlite.connect('vocabulary.db') as db:
            # Save lyrics
            await db.execute("""
                INSERT OR REPLACE INTO songs (
                    id,
                    lyrics,
                    last_updated
                ) VALUES (?, ?, ?)
            """, (song_id, lyrics, datetime.now().isoformat()))
            
            # Save vocabulary items
            for item in vocabulary:
                await db.execute("""
                    INSERT OR REPLACE INTO vocabulary (
                        song_id,
                        word,
                        reading,
                        meaning,
                        part_of_speech,
                        difficulty_level,
                        metadata
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    song_id,
                    item['word'],
                    item.get('reading', ''),
                    item.get('meaning', ''),
                    item.get('part_of_speech', ''),
                    item.get('difficulty_level', ''),
                    json.dumps(item.get('metadata', {}))
                ))
            
            await db.commit()
            logger.info(f"Successfully saved song {song_id} with {len(vocabulary)} vocabulary items")
            return True
            
    except Exception as e:
        logger.error(f"Error saving results to database: {e}")
        return False 