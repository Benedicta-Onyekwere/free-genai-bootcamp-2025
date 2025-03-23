# Free GenAI Bootcamp 2025

## Project Overview
This repository contains the projects and assignments completed during the Free GenAI Bootcamp 2025. The main project is a Japanese Language Learning Platform that combines AI-powered vocabulary generation with an interactive learning interface.

## Projects

### 1. Vocabulary Importer
A Streamlit-based tool for generating Japanese vocabulary using OpenAI's GPT-3.5. This tool helps populate the language learning platform with properly formatted vocabulary words and groups.

[View Vocabulary Importer Documentation](./vocab-importer/README.md)

### 2. Language Learning Portal
An interactive web application for learning Japanese, built with:
- Frontend: React + TypeScript + Vite
- Backend: Go + Gin
- Database: PostgreSQL
- State Management: TanStack Query (React Query)

## Technical Stack
- **Frontend**: React 19, TypeScript, Vite, TailwindCSS
- **Backend**: Go 1.21, Gin Framework
- **Database**: PostgreSQL with GORM
- **AI Integration**: OpenAI GPT-3.5
- **Tools**: Streamlit, Docker
- **Testing**: RSpec, React Testing Library

## Project Structure
```
free-genai-bootcamp-2025/
├── vocab-importer/         # Vocabulary generation tool
├── lang-portal/            # Main language learning application
│   ├── assets/            # Screenshots and images
│   ├── backend-go/        # Go backend service
│   └── frontend/          # React frontend application
└── README.md              # This file
```

## Frontend and Backend Integration

After successfully implementing both the frontend and backend components separately, we integrated them to create a complete language learning platform. You can find detailed documentation for each component here:

- [Frontend Implementation Documentation](./lang-portal/frontend/README.md)
- [Backend Implementation Documentation](./lang-portal/backend-go/README.md)

### Integration Journey

Here's a detailed walkthrough of our integration process:

### 1. API Client Setup
- Installed required dependencies:
  ```bash
  npm install axios @tanstack/react-query
  ```
- Created API client configuration:
  ```typescript
  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8082/api';
  export const api = axios.create({
    baseURL: API_URL,
    headers: { 'Content-Type': 'application/json' },
  });
  ```

### 2. Environment Configuration
- Created `.env` file for API configuration:
  ```
  VITE_API_URL=http://localhost:8082/api
  ```
- Verified environment variable loading in development

### 3. Test Data Setup
- Created seed data for testing:
  ```sql
  -- Insert test groups
  INSERT INTO groups (name) VALUES 
  ('Basic Japanese'),
  ('JLPT N5 Vocabulary');

  -- Insert test words
  INSERT INTO words (japanese, romaji, english) VALUES 
  ('犬', 'inu', 'dog'),
  ('猫', 'neko', 'cat');
  ```
- Verified data insertion with curl:
  ```bash
  curl http://localhost:8082/api/dashboard/quick-stats
  # Response:
  {
    "success_rate": 85.71,
    "total_study_sessions": 17,
    "total_active_groups": 2,
    "study_streak_days": 2
  }
  ```

### 4. React Query Implementation
- Added React Query provider in main.tsx:
  ```typescript
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 1000 * 60 * 5, // 5 minutes
        retry: 1,
      },
    },
  });
  ```
- Implemented data fetching in Dashboard component:
  ```typescript
  const { 
    data: lastSession,
    isLoading: isLoadingSession 
  } = useQuery<LastStudySession>({
    queryKey: ['lastStudySession'],
    queryFn: () => dashboardApi.getLastStudySession()
  });
  ```

### 5. Integration Testing
1. Backend Health Verification:
   - All endpoints returning 200 status codes
   - Response times consistently under 10ms
   - Example log:
     ```
     [GIN] 2025/03/22 - 17:28:33 | 200 | 215.084µs | ::1 | GET "/api/dashboard/last_study_session"
     ```

2. Frontend Integration Verification:
   - Confirmed API calls in Network tab
   - Validated data display in UI components
   - Tested loading states functionality
   - Verified error handling

### 6. Challenges and Solutions
1. **CORS Configuration**
   - Challenge: Frontend couldn't access backend API
   - Solution: Added CORS middleware in Go backend:
     ```go
     r.Use(func(c *gin.Context) {
       c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
       // ... other CORS headers
     })
     ```

2. **Data Type Synchronization**
   - Challenge: Mismatched types between frontend and backend
   - Solution: Created TypeScript interfaces matching Go structs:
     ```typescript
     interface LastStudySession {
       id: number;
       group_id: number;
       created_at: string;
       study_activity_id: number;
       group_name: string;
     }
     ```

### 7. Final Verification
- Tested complete data flow:
  1. Backend serving data correctly
  2. Frontend making successful API calls
  3. UI updating with real data
  4. Loading states working as expected
  5. Error states handled properly

## Screenshots

### Dashboard Integration
Below is the dashboard visualization after integrating mock data through the API, displaying the three main components: Quick Stats for overall metrics, Study Sessions timeline, and Study Progress tracking:

![Dashboard Integration](./lang-portal/assets/dashboard-output.png)

### API Testing Results
Here's a demonstration of testing the API endpoints using curl commands, verifying the correct handling of requests and responses:

![API Test Results](./lang-portal/assets/api-test-results.png)