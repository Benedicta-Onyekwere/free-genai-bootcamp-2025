package models

import (
	"database/sql"
	"time"
)

type StudyActivity struct {
	ID           int       `json:"id"`
	Name         string    `json:"name"`
	Description  string    `json:"description"`
	ThumbnailURL string    `json:"thumbnail_url,omitempty"`
	CreatedAt    time.Time `json:"created_at"`
}

// CreateStudyActivity creates a new study activity in the database
func CreateStudyActivity(db *sql.DB, name, description, thumbnailURL string) (*StudyActivity, error) {
	tx, err := db.Begin()
	if err != nil {
		return nil, err
	}
	defer tx.Rollback()

	result, err := tx.Exec(`
		INSERT INTO study_activities (name, description, thumbnail_url)
		VALUES (?, ?, ?)
	`, name, description, thumbnailURL)
	if err != nil {
		return nil, err
	}

	id, err := result.LastInsertId()
	if err != nil {
		return nil, err
	}

	var activity StudyActivity
	err = tx.QueryRow(`
		SELECT id, name, description, thumbnail_url, created_at
		FROM study_activities
		WHERE id = ?
	`, id).Scan(
		&activity.ID,
		&activity.Name,
		&activity.Description,
		&activity.ThumbnailURL,
		&activity.CreatedAt,
	)
	if err != nil {
		return nil, err
	}

	if err = tx.Commit(); err != nil {
		return nil, err
	}

	return &activity, nil
}

// GetStudyActivityByID retrieves a study activity by its ID
func GetStudyActivityByID(db *sql.DB, id int) (*StudyActivity, error) {
	query := `
		SELECT id, name, description, thumbnail_url, created_at
		FROM study_activities
		WHERE id = ?
	`
	
	activity := &StudyActivity{}
	err := db.QueryRow(query, id).Scan(
		&activity.ID,
		&activity.Name,
		&activity.Description,
		&activity.ThumbnailURL,
		&activity.CreatedAt,
	)
	
	if err != nil {
		return nil, err
	}
	
	return activity, nil
}

// GetStudyActivities retrieves all study activities
func GetStudyActivities(db *sql.DB) ([]*StudyActivity, error) {
	query := `
		SELECT id, name, description, thumbnail_url, created_at
		FROM study_activities
		ORDER BY created_at DESC
	`
	
	rows, err := db.Query(query)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	
	var activities []*StudyActivity
	for rows.Next() {
		activity := &StudyActivity{}
		err := rows.Scan(
			&activity.ID,
			&activity.Name,
			&activity.Description,
			&activity.ThumbnailURL,
			&activity.CreatedAt,
		)
		if err != nil {
			return nil, err
		}
		activities = append(activities, activity)
	}
	
	if err = rows.Err(); err != nil {
		return nil, err
	}
	
	return activities, nil
} 