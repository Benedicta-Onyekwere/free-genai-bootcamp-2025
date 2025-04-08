import aiosqlite
from pathlib import Path

DATABASE_PATH = Path("vocabulary.db")

async def init_db():
    """Initialize the database with required tables."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        # Create songs table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS songs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                artist TEXT,
                lyrics TEXT NOT NULL,
                language TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create vocabulary table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS vocabulary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT NOT NULL,
                reading TEXT,  -- For Japanese readings
                meaning TEXT,
                part_of_speech TEXT,
                difficulty_level TEXT,
                song_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (song_id) REFERENCES songs (id)
            )
        """)
        
        await db.commit()

async def add_song_and_vocabulary(title: str, artist: str, lyrics: str, language: str, vocabulary_list: list):
    """Add a song and its vocabulary to the database."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        # Insert song
        cursor = await db.execute(
            "INSERT INTO songs (title, artist, lyrics, language) VALUES (?, ?, ?, ?)",
            (title, artist, lyrics, language)
        )
        song_id = cursor.lastrowid
        
        # Insert vocabulary
        for vocab in vocabulary_list:
            await db.execute("""
                INSERT INTO vocabulary 
                (word, reading, meaning, part_of_speech, difficulty_level, song_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                vocab["word"],
                vocab.get("reading"),
                vocab.get("meaning"),
                vocab.get("part_of_speech"),
                vocab.get("difficulty_level"),
                song_id
            ))
        
        await db.commit()
        return song_id

async def get_song_vocabulary(song_id: int):
    """Get vocabulary for a specific song."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            """
            SELECT v.* FROM vocabulary v
            WHERE v.song_id = ?
            ORDER BY v.word
            """,
            (song_id,)
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows] 