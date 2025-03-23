import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080/api';

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API interfaces
export interface LastStudySession {
  id: number;
  group_id: number;
  created_at: string;
  study_activity_id: number;
  group_name: string;
}

export interface StudyProgress {
  total_words_studied: number;
  total_available_words: number;
}

export interface QuickStats {
  success_rate: number;
  total_study_sessions: number;
  total_active_groups: number;
  study_streak_days: number;
}

// API functions
export const dashboardApi = {
  getLastStudySession: () => 
    api.get<LastStudySession>('/dashboard/last_study_session'),
  
  getStudyProgress: () => 
    api.get<StudyProgress>('/dashboard/study_progress'),
  
  getQuickStats: () => 
    api.get<QuickStats>('/dashboard/quick-stats'),
};

export const studySessionsApi = {
  list: (page = 1) => 
    api.get('/study_sessions', { params: { page } }),
  
  get: (id: number) => 
    api.get(`/study_sessions/${id}`),
  
  create: (data: { group_id: number; study_activity_id: number }) => 
    api.post('/study_sessions', data),
  
  addWordReview: (sessionId: number, wordId: number, correct: boolean) => 
    api.post(`/study_sessions/${sessionId}/words/${wordId}/review`, { correct }),
};

export const wordsApi = {
  list: (page = 1) => 
    api.get('/words', { params: { page } }),
  
  get: (id: number) => 
    api.get(`/words/${id}`),
};

export const groupsApi = {
  list: (page = 1) => 
    api.get('/groups', { params: { page } }),
  
  get: (id: number) => 
    api.get(`/groups/${id}`),
  
  getWords: (id: number, page = 1) => 
    api.get(`/groups/${id}/words`, { params: { page } }),
  
  getStudySessions: (id: number, page = 1) => 
    api.get(`/groups/${id}/study_sessions`, { params: { page } }),
}; 