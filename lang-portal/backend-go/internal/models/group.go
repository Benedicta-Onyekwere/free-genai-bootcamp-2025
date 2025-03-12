package models

import (
	"database/sql"
)

// Group represents a thematic group of words
type Group struct {
	ID   int    `json:"id"`
	Name string `json:"name"`
}

// GroupWithStats includes group information along with word count
type GroupWithStats struct {
	Group
	WordCount int `json:"word_count"`
}

// GetGroups retrieves a paginated list of groups with their word counts
func GetGroups(db *sql.DB, page, perPage int) ([]GroupWithStats, int, error) {
	offset := (page - 1) * perPage

	// Get total count
	var total int
	err := db.QueryRow("SELECT COUNT(*) FROM groups").Scan(&total)
	if err != nil {
		return nil, 0, err
	}

	// Get groups with word counts
	query := `
		SELECT 
			g.id, g.name,
			COUNT(DISTINCT wg.word_id) as word_count
		FROM groups g
		LEFT JOIN words_groups wg ON g.id = wg.group_id
		GROUP BY g.id
		LIMIT ? OFFSET ?
	`

	rows, err := db.Query(query, perPage, offset)
	if err != nil {
		return nil, 0, err
	}
	defer rows.Close()

	var groups []GroupWithStats
	for rows.Next() {
		var g GroupWithStats
		err := rows.Scan(&g.ID, &g.Name, &g.WordCount)
		if err != nil {
			return nil, 0, err
		}
		groups = append(groups, g)
	}

	return groups, total, nil
}

// GetGroupByID retrieves a single group by its ID along with statistics
func GetGroupByID(db *sql.DB, id int) (*GroupWithStats, error) {
	query := `
		SELECT 
			g.id, g.name,
			COUNT(DISTINCT wg.word_id) as word_count
		FROM groups g
		LEFT JOIN words_groups wg ON g.id = wg.group_id
		WHERE g.id = ?
		GROUP BY g.id
	`

	var g GroupWithStats
	err := db.QueryRow(query, id).Scan(&g.ID, &g.Name, &g.WordCount)
	if err != nil {
		return nil, err
	}

	return &g, nil
}

// GetGroupWords retrieves all words associated with a group
func GetGroupWords(db *sql.DB, groupID int, page, perPage int) ([]WordWithStats, int, error) {
	offset := (page - 1) * perPage

	// Get total count
	var total int
	err := db.QueryRow(`
		SELECT COUNT(*) 
		FROM words w
		JOIN words_groups wg ON w.id = wg.word_id
		WHERE wg.group_id = ?
	`, groupID).Scan(&total)
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
		JOIN words_groups wg ON w.id = wg.word_id
		LEFT JOIN word_review_items wri ON w.id = wri.word_id
		WHERE wg.group_id = ?
		GROUP BY w.id
		LIMIT ? OFFSET ?
	`

	rows, err := db.Query(query, groupID, perPage, offset)
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