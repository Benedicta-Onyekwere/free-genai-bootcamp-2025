# Language Learning Portal Backend

## Implementing Backend API Endpoints Using Cursor

This project is a backend server for a language learning portal, built using Go. It serves as an inventory of vocabulary, a learning record store, and a launchpad for various learning apps.

## Business Goals

- Inventory of possible vocabulary that can be learned.
- Act as a Learning Record Store (LRS), providing correct and wrong scores on practice vocabulary.
- A unified launchpad to launch different learning apps.

## Technical Specifications
- **Backend Language:** Go
- **Database:** SQLite3
- **API Framework:** Gin
- **Task Runner:** Mage
- **Authentication:** None (single user)

## Project Setup

### Initial Steps

1. **Read Frontend-Technical-Specs.md:** 
   - The frontend specifications provided a detailed outline of the user interface and the necessary API endpoints required for each page. This served as a backdrop for designing the backend API to ensure seamless integration with the frontend.

2. **Read Backend-Technical-Specs.md:**
   - The specifications provided the blueprint for the backend architecture, including the API endpoints, database schema, and technical requirements.

3. **Create Project Structure:**
   - Set up the directory structure as outlined in the specs:
     ```
     backend_go/
     ├── cmd/
     │   └── server/
     ├── internal/
     │   ├── models/     # Data structures and database operations
     │   ├── handlers/   # HTTP handlers organized by feature (dashboard, words, groups, etc.)
     │   └── service/    # Business logic
     ├── db/
     │   ├── migrations/
     │   └── seeds/      # For initial data population
     ├── magefile.go
     ├── go.mod
     └── words.db
     ```

     ### Implementation

4. **Set Up Database:**
   - Created `words.db` as the SQLite database.
   - Defined tables for words, groups, study sessions, etc., based on the schema in the specs.

5. **Develop API Endpoints:**
   - Implemented endpoints for managing words, groups, study sessions, and dashboard statistics.
   - Used the Gin framework to handle HTTP requests and responses.

6. **Implement Business Logic:**
   - Created services for handling business logic, such as `WordService`, `GroupService`, `StudySessionService`, etc.
   - Used a `CompositeService` to combine these services for easier management.

7. **Testing:**
   - Tested API endpoints using `curl` and Postman to ensure they return the expected responses.
   - Verified database interactions and ensured correct API responses.
   - Here are some example `curl` commands and their outputs:
 
 ![Curl Commands Output](assets/Curl-commands.png)

### Running the Server

1. **Install Dependencies:**
   Ensure you have Go installed. Then, run:
   ```bash
   go mod tidy
   ```

2. **Start the Server:**
   Run the server using:
   ```bash
   go run cmd/server/main.go
   ```

### API Endpoints

- **Dashboard Endpoints:**
  - `GET /api/dashboard/last_study_session`
  - `GET /api/dashboard/study_progress`
  - `GET /api/dashboard/quick_stats`

  - **Study Activities Endpoints:**
  - `GET /api/study_activities`
  - `GET /api/study_activities/:id`
  - `POST /api/study_activities`

- **Words Endpoints:**
  - `GET /api/words`
  - `GET /api/words/:id`

- **Groups Endpoints:**
  - `GET /api/groups`
  - `GET /api/groups/:id`

- **Study Sessions Endpoints:**
  - `GET /api/study_sessions`
  - `GET /api/study_sessions/:id`

- **Reset Endpoints:**
  - `POST /api/reset_history`
  - `POST /api/full_reset`
  