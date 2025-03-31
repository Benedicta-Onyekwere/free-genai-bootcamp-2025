import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API interfaces
export interface StudyActivity {
  id: number;
  type: string;
  data: any;
  timestamp: string;
}

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

export interface StudySessionResponse {
  data: {
    id: number;
    groupName: string;
    activityName: string;
    startTime: string;
    endTime: string;
    reviewItemCount: number;
  }[];
  total: number;
  page: number;
  per_page: number;
}

// API functions
export const studyActivitiesApi = {
  list: () => 
    api.get<StudyActivity[]>('/study-activities'),
  
  create: (data: any) => 
    api.post<StudyActivity>('/study-activities', data),

  // Specific endpoint for writing practice
  submitWritingPractice: (data: {
    english_sentence: string;
    transcribed_text: string;
    translation: string;
    grade: string;
    feedback: string;
  }) => 
    api.post<StudyActivity>('/writing-practice', data),
};

export const dashboardApi = {
  getLastStudySession: () => 
    api.get<LastStudySession>('/dashboard/last_study_session'),
  
  getStudyProgress: () => 
    api.get<StudyProgress>('/dashboard/study_progress'),
  
  getQuickStats: () => 
    api.get<QuickStats>('/dashboard/quick-stats'),
};

export const studySessionsApi = {
  list: (params: { page: number }) => 
    api.get<StudySessionResponse>('/study-sessions', { params }),
  
  get: (id: number) => 
    api.get(`/study-sessions/${id}`),
  
  create: (data: { group_id: number; study_activity_id: number }) => 
    api.post('/study-sessions', data),
  
  addWordReview: (sessionId: number, wordId: number, correct: boolean) => 
    api.post(`/study-sessions/${sessionId}/words/${wordId}/review`, { correct }),
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