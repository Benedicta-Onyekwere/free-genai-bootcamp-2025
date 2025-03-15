import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'

interface Session {
  id: number
  groupName: string
  activityName: string
  startTime: string
  endTime: string
  reviewItemCount: number
}

const Dashboard = () => {
  const [currentTime, setCurrentTime] = useState(new Date())
  const [lastSession, setLastSession] = useState<Session | null>(null)

  // TODO: Replace with actual API call
  useEffect(() => {
    setLastSession({
      id: 1,
      groupName: 'Core Verbs',
      activityName: 'Adventure MUD',
      startTime: '2024-03-20 14:30',
      endTime: '2024-03-20 15:00',
      reviewItemCount: 25,
    })
  }, [])

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
      hour12: true,
    }).format(date)
  }

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-8">Dashboard</h1>
      
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {/* Date and Time Card */}
        <div className="bg-card text-card-foreground rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">Current Date & Time</h2>
          <div className="space-y-2">
            <p className="text-lg">{formatDate(currentTime)}</p>
            <p className="text-3xl font-bold text-primary">{formatTime(currentTime)}</p>
          </div>
        </div>

        {/* Last Session Card */}
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-lg font-medium mb-4">Last Session</h2>
          {lastSession ? (
            <div className="space-y-4">
              <div className="flex justify-between">
                <div>
                  <p className="text-sm text-gray-500">Activity</p>
                  <p className="font-medium">{lastSession.activityName}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Group</p>
                  <Link
                    to={`/groups/${lastSession.id}`}
                    className="font-medium text-primary hover:text-primary/80"
                  >
                    {lastSession.groupName}
                  </Link>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Review Items</p>
                  <p className="font-medium">{lastSession.reviewItemCount}</p>
                </div>
              </div>
              <div className="flex justify-between">
                <div>
                  <p className="text-sm text-gray-500">Start Time</p>
                  <p className="font-medium">{lastSession.startTime}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">End Time</p>
                  <p className="font-medium">{lastSession.endTime}</p>
                </div>
              </div>
            </div>
          ) : (
            <p className="text-gray-500">No sessions recorded yet.</p>
          )}
        </div>

        {/* Progress Summary Card - Placeholder */}
        <div className="bg-card text-card-foreground rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">Progress Summary</h2>
          <p className="text-muted-foreground">Start your learning journey</p>
        </div>
      </div>
    </div>
  )
}

export default Dashboard 