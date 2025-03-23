import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { dashboardApi, LastStudySession, StudyProgress, QuickStats } from '../lib/api'

const Dashboard = () => {
  const [currentTime, setCurrentTime] = useState(new Date())

  const { 
    data: lastSession,
    isLoading: isLoadingSession 
  } = useQuery<LastStudySession>({
    queryKey: ['lastStudySession'],
    queryFn: () => dashboardApi.getLastStudySession().then(res => res.data)
  })

  const {
    data: studyProgress,
    isLoading: isLoadingProgress
  } = useQuery<StudyProgress>({
    queryKey: ['studyProgress'],
    queryFn: () => dashboardApi.getStudyProgress().then(res => res.data)
  })

  const {
    data: quickStats,
    isLoading: isLoadingStats
  } = useQuery<QuickStats>({
    queryKey: ['quickStats'],
    queryFn: () => dashboardApi.getQuickStats().then(res => res.data)
  })

  useEffect(() => {
    // Update time every second
    const timer = setInterval(() => {
      setCurrentTime(new Date())
    }, 1000)

    // Cleanup interval on component unmount
    return () => clearInterval(timer)
  }, [])

  const formatDate = (date: Date) => {
    return new Intl.DateTimeFormat('en-US', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    }).format(date)
  }

  const formatTime = (date: Date) => {
    return new Intl.DateTimeFormat('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
    }).format(date)
  }

  if (isLoadingSession || isLoadingProgress || isLoadingStats) {
    return <div className="flex justify-center items-center h-screen">Loading...</div>
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Dashboard</h1>
        <p className="text-gray-600">
          {formatDate(currentTime)} - {formatTime(currentTime)}
        </p>
      </div>

      {/* Last Study Session */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">Last Study Session</h2>
        {lastSession ? (
          <div>
            <p className="mb-2">
              <span className="font-medium">Group:</span>{' '}
              <Link to={`/groups/${lastSession.group_id}`} className="text-blue-600 hover:underline">
                {lastSession.group_name}
              </Link>
            </p>
            <p className="mb-2">
              <span className="font-medium">Date:</span>{' '}
              {new Date(lastSession.created_at).toLocaleDateString()}
            </p>
          </div>
        ) : (
          <p>No recent study sessions</p>
        )}
      </div>

      {/* Study Progress */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">Study Progress</h2>
        {studyProgress && (
          <div>
            <div className="mb-4">
              <div className="flex justify-between mb-1">
                <span>Total Words</span>
                <span>{studyProgress.total_words_studied}/{studyProgress.total_available_words}</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2.5">
                <div
                  className="bg-blue-600 h-2.5 rounded-full"
                  style={{
                    width: `${(studyProgress.total_words_studied / studyProgress.total_available_words) * 100}%`
                  }}
                ></div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Quick Stats */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold mb-4">Quick Stats</h2>
        {quickStats && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center">
              <p className="text-2xl font-bold text-blue-600">{quickStats.success_rate}%</p>
              <p className="text-gray-600">Success Rate</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-blue-600">{quickStats.total_study_sessions}</p>
              <p className="text-gray-600">Study Sessions</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-blue-600">{quickStats.total_active_groups}</p>
              <p className="text-gray-600">Active Groups</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-blue-600">{quickStats.study_streak_days}</p>
              <p className="text-gray-600">Day Streak</p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default Dashboard