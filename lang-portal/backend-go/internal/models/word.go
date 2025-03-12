package models

import (
	"database/sql"
)

// Word represents a vocabulary word
type Word struct {
	ID       int    `json:"id"`
	Japanese string `json:"japanese"`
	Romaji   string `json:"romaji"`
	English  string `json:"english"`
}

// WordWithStats includes word information along with study statistics
type WordWithStats struct {
	Word
	CorrectCount int `json:"correct_count"`
	WrongCount   int `json:"wrong_count"`
}

// GetWords retrieves a paginated list of words with their study statistics
func GetWords(db *sql.DB, page, perPage int) ([]WordWithStats, int, error) {
	offset := (page - 1) * perPage

	// Get total count
	var total int
	err := db.QueryRow("SELECT COUNT(*) FROM words").Scan(&total)
	if err != nil {
		return nil, 0, err
	}

	// Get words with stats
	query := `
		SELECT 
			w.id, w.japanese, w.romaji, w.english,
			COUNT(CASE WHEN wri.correct = 1 THEN 1 END) as correct_count,
			COUNT(CASE WHEN wri.correct = 0 THEN 1 END) as wrong_count
		FROM words w
		LEFT JOIN word_review_items wri ON w.id = wri.word_id
		GROUP BY w.id
		LIMIT ? OFFSET ?
	`

	rows, err := db.Query(query, perPage, offset)
	if err != nil {
		return nil, 0, err
	}
	defer rows.Close()

	var words []WordWithStats
	for rows.Next() {
		var w WordWithStats
		err := rows.Scan(
			&w.ID, &w.Japanese, &w.Romaji, &w.English,
			&w.CorrectCount, &w.WrongCount,
		)
		if err != nil {
			return nil, 0, err
		}
		words = append(words, w)
	}

	return words, total, nil
}

// GetWordByID retrieves a single word by its ID along with its statistics
func GetWordByID(db *sql.DB, id int) (*WordWithStats, error) {
	query := `
		SELECT 
			w.id, w.japanese, w.romaji, w.english,
			COUNT(CASE WHEN wri.correct = 1 THEN 1 END) as correct_count,
			COUNT(CASE WHEN wri.correct = 0 THEN 1 END) as wrong_count
		FROM words w
		LEFT JOIN word_review_items wri ON w.id = wri.word_id
		WHERE w.id = ?
		GROUP BY w.id
	`

	var w WordWithStats
	err := db.QueryRow(query, id).Scan(
		&w.ID, &w.Japanese, &w.Romaji, &w.English,
		&w.CorrectCount, &w.WrongCount,
	)
	if err != nil {
		return nil, err
	}

	return &w, nil
} 