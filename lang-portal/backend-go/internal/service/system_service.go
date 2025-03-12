package service

import (
	"database/sql"
	"fmt"
	"os"
	"path/filepath"
)

// SystemService handles system-wide operations
type SystemService struct {
	*BaseService
}

// NewSystemService creates a new system service
func NewSystemService(base *BaseService) *SystemService {
	return &SystemService{BaseService: base}
}

// ResetHistory deletes all study sessions and word review items
func (s *SystemService) ResetHistory() error {
	tx, err := s.db.Begin()
	if err != nil {
		return fmt.Errorf("failed to begin transaction: %v", err)
	}

	// Delete all word review items
	if _, err := tx.Exec("DELETE FROM word_review_items"); err != nil {
		tx.Rollback()
		return fmt.Errorf("failed to delete word review items: %v", err)
	}

	// Delete all study sessions
	if _, err := tx.Exec("DELETE FROM study_sessions"); err != nil {
		tx.Rollback()
		return fmt.Errorf("failed to delete study sessions: %v", err)
	}

	return tx.Commit()
}

// FullReset performs a complete system reset
func (s *SystemService) FullReset() error {
	// Close the current database connection
	if err := s.db.Close(); err != nil {
		return fmt.Errorf("failed to close database connection: %v", err)
	}

	// Remove the database file
	dbPath := "./words.db"
	if err := os.Remove(dbPath); err != nil && !os.IsNotExist(err) {
		return fmt.Errorf("failed to remove database file: %v", err)
	}

	// Run migrations
	files, err := filepath.Glob("db/migrations/*.sql")
	if err != nil {
		return fmt.Errorf("failed to read migration files: %v", err)
	}

	// Create new database connection
	s.db, err = InitDB(dbPath)
	if err != nil {
		return fmt.Errorf("failed to initialize database: %v", err)
	}

	// Execute migrations
	for _, file := range files {
		content, err := os.ReadFile(file)
		if err != nil {
			return fmt.Errorf("failed to read migration file %s: %v", file, err)
		}

		if _, err := s.db.Exec(string(content)); err != nil {
			return fmt.Errorf("failed to execute migration %s: %v", file, err)
		}
	}

	return nil
}

// InitDB initializes a new SQLite database
func InitDB(dbPath string) (*sql.DB, error) {
	db, err := sql.Open("sqlite3", dbPath)
	if err != nil {
		return nil, fmt.Errorf("failed to open database: %v", err)
	}

	if err := db.Ping(); err != nil {
		return nil, fmt.Errorf("failed to ping database: %v", err)
	}

	return db, nil
} 