// +build mage

package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"
	"sort"
	"strings"

	_ "github.com/mattn/go-sqlite3"
)

const dbPath = "./words.db"

// Word represents a vocabulary word
type Word struct {
	Japanese string `json:"japanese"`
	Romaji   string `json:"romaji"`
	English  string `json:"english"`
}

// SeedFile represents the structure of our seed JSON files
type SeedFile struct {
	GroupName string `json:"group_name"`
	Words     []Word `json:"words"`
}

// Init creates a new SQLite database
func Init() error {
	fmt.Println("Creating database...")
	
	// Remove existing database if it exists
	if _, err := os.Stat(dbPath); err == nil {
		if err := os.Remove(dbPath); err != nil {
			return fmt.Errorf("failed to remove existing database: %v", err)
		}
	}

	// Create new database file
	db, err := sql.Open("sqlite3", dbPath)
	if err != nil {
		return fmt.Errorf("failed to create database: %v", err)
	}
	defer db.Close()

	fmt.Println("Database created successfully!")
	return nil
}

// Migrate runs all migration files in order
func Migrate() error {
	fmt.Println("Running migrations...")

	db, err := sql.Open("sqlite3", dbPath)
	if err != nil {
		return fmt.Errorf("failed to open database: %v", err)
	}
	defer db.Close()

	// Get all migration files
	files, err := filepath.Glob("db/migrations/*.sql")
	if err != nil {
		return fmt.Errorf("failed to read migration files: %v", err)
	}

	// Sort files to ensure order
	sort.Strings(files)

	// Execute each migration file
	for _, file := range files {
		fmt.Printf("Applying migration: %s\n", filepath.Base(file))
		
		content, err := ioutil.ReadFile(file)
		if err != nil {
			return fmt.Errorf("failed to read migration file %s: %v", file, err)
		}

		// Split file into separate statements
		statements := strings.Split(string(content), ";")
		
		// Execute each statement
		for _, stmt := range statements {
			stmt = strings.TrimSpace(stmt)
			if stmt == "" {
				continue
			}

			if _, err := db.Exec(stmt); err != nil {
				return fmt.Errorf("failed to execute migration %s: %v", file, err)
			}
		}
	}

	fmt.Println("Migrations completed successfully!")
	return nil
}

// Seed loads initial data from JSON files
func Seed() error {
	fmt.Println("Seeding database...")

	db, err := sql.Open("sqlite3", dbPath)
	if err != nil {
		return fmt.Errorf("failed to open database: %v", err)
	}
	defer db.Close()

	// Get all seed files
	files, err := filepath.Glob("db/seeds/*.json")
	if err != nil {
		return fmt.Errorf("failed to read seed files: %v", err)
	}

	// Process each seed file
	for _, file := range files {
		fmt.Printf("Processing seed file: %s\n", filepath.Base(file))

		content, err := ioutil.ReadFile(file)
		if err != nil {
			return fmt.Errorf("failed to read seed file %s: %v", file, err)
		}

		var seedData struct {
			GroupName string `json:"group_name"`
			Words     []Word `json:"words"`
		}

		if err := json.Unmarshal(content, &seedData); err != nil {
			return fmt.Errorf("failed to parse seed file %s: %v", file, err)
		}

		// Begin transaction
		tx, err := db.Begin()
		if err != nil {
			return fmt.Errorf("failed to begin transaction: %v", err)
		}

		// Create group
		result, err := tx.Exec("INSERT INTO groups (name) VALUES (?)", seedData.GroupName)
		if err != nil {
			tx.Rollback()
			return fmt.Errorf("failed to insert group: %v", err)
		}

		groupID, err := result.LastInsertId()
		if err != nil {
			tx.Rollback()
			return fmt.Errorf("failed to get group ID: %v", err)
		}

		// Insert words and create associations
		for _, word := range seedData.Words {
			result, err := tx.Exec(
				"INSERT INTO words (japanese, romaji, english) VALUES (?, ?, ?)",
				word.Japanese, word.Romaji, word.English,
			)
			if err != nil {
				tx.Rollback()
				return fmt.Errorf("failed to insert word: %v", err)
			}

			wordID, err := result.LastInsertId()
			if err != nil {
				tx.Rollback()
				return fmt.Errorf("failed to get word ID: %v", err)
			}

			// Create word-group association
			_, err = tx.Exec(
				"INSERT INTO words_groups (word_id, group_id) VALUES (?, ?)",
				wordID, groupID,
			)
			if err != nil {
				tx.Rollback()
				return fmt.Errorf("failed to create word-group association: %v", err)
			}
		}

		// Commit transaction
		if err := tx.Commit(); err != nil {
			return fmt.Errorf("failed to commit transaction: %v", err)
		}
	}

	fmt.Println("Database seeded successfully!")
	return nil
}

// Reset performs a complete reset: drops and recreates the database, runs migrations, and seeds data
func Reset() error {
	if err := Init(); err != nil {
		return err
	}

	if err := Migrate(); err != nil {
		return err
	}

	if err := Seed(); err != nil {
		return err
	}

	return nil
}

// LoadSeedData loads seed data from JSON files into the database
func LoadSeedData() error {
	// Open database connection
	db, err := sql.Open("sqlite3", "./words.db")
	if err != nil {
		return fmt.Errorf("failed to open database: %w", err)
	}
	defer db.Close()

	// Load words from JSON
	wordsData, err := ioutil.ReadFile("db/seeds/words_seed.json")
	if err != nil {
		return fmt.Errorf("failed to read words seed file: %w", err)
	}

	var words []Word

	if err := json.Unmarshal(wordsData, &words); err != nil {
		return fmt.Errorf("failed to unmarshal words data: %w", err)
	}

	// Insert words into database
	for _, word := range words {
		_, err := db.Exec(`INSERT INTO words (japanese, romaji, english) VALUES (?, ?, ?)`,
			word.Japanese, word.Romaji, word.English)
		if err != nil {
			return fmt.Errorf("failed to insert word: %w", err)
		}
	}

	log.Println("Seed data loaded successfully")
	return nil
} 