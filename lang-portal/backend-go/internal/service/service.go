package service

// Service represents the interface for all business operations
type Service interface {
	// Word operations
	GetWords(page, perPage int) (interface{}, int, error)
	GetWordByID(id int) (interface{}, error)
	
	// Group operations
	GetGroups(page, perPage int) (interface{}, int, error)
	GetGroupByID(id int) (interface{}, error)
	GetGroupWords(groupID, page, perPage int) (interface{}, int, error)
	
	// Study session operations
	GetStudySessions(page, perPage int) (interface{}, int, error)
	GetStudySessionByID(id int) (interface{}, error)
	GetStudySessionWords(sessionID, page, perPage int) (interface{}, int, error)
	CreateStudySession(groupID, activityID int) (interface{}, error)
	AddWordReview(sessionID, wordID int, correct bool) error
	GetStudySessionsByGroup(groupID, page, perPage int) (interface{}, int, error)
	
	// Dashboard operations
	GetLastStudySession() (interface{}, error)
	GetStudyProgress() (interface{}, error)
	GetQuickStats() (interface{}, error)
	
	// System operations
	ResetHistory() error
	FullReset() error
} 