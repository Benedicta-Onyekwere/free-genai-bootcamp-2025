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

const Sessions = () => {
  const [currentTime, setCurrentTime] = useState(new Date())
  const [sessions, setSessions] = useState<Session[]>([])
  const [sortField, setSortField] = useState<keyof Session>('startTime')
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('desc')
  const [currentPage, setCurrentPage] = useState(1)
  const sessionsPerPage = 10

  useEffect(() => {
    // Update time every second
    const timer = setInterval(() => {
      setCurrentTime(new Date())
    }, 1000)

    // Cleanup interval on component unmount
    return () => clearInterval(timer)
  }, [])

  // TODO: Replace with actual API call
  useEffect(() => {
    // Simulated session data
    const mockSessions: Session[] = [
      {
        id: 1,
        groupName: 'Core Verbs',
        activityName: 'Adventure MUD',
        startTime: '2024-03-20 14:30',
        endTime: '2024-03-20 15:00',
        reviewItemCount: 25,
      },
      {
        id: 2,
        groupName: 'Basic Nouns',
        activityName: 'Typing Tutor',
        startTime: '2024-03-19 10:15',
        endTime: '2024-03-19 10:45',
        reviewItemCount: 30,
      },
      {
        id: 3,
        groupName: 'Adjectives',
        activityName: 'Adventure MUD',
        startTime: '2024-03-18 16:00',
        endTime: '2024-03-18 16:30',
        reviewItemCount: 20,
      },
    ]
    setSessions(mockSessions)
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

  const handleSort = (field: keyof Session) => {
    if (field === sortField) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc')
    } else {
      setSortField(field)
      setSortDirection('asc')
    }
  }

  const sortedSessions = [...sessions].sort((a, b) => {
    const aValue = a[sortField]
    const bValue = b[sortField]
    const direction = sortDirection === 'asc' ? 1 : -1
    return aValue < bValue ? -1 * direction : aValue > bValue ? 1 * direction : 0
  })

  const totalPages = Math.ceil(sessions.length / sessionsPerPage)
  const paginatedSessions = sortedSessions.slice(
    (currentPage - 1) * sessionsPerPage,
    currentPage * sessionsPerPage
  )

  const SortIcon = ({ field }: { field: keyof Session }) => (
    <span className="ml-1">
      {sortField === field ? (
        sortDirection === 'asc' ? '↑' : '↓'
      ) : (
        <span className="text-gray-300">↕</span>
      )}
    </span>
  )

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-8">Study Sessions</h1>

      <div className="grid gap-6 mb-8">
        {/* Date and Time Card */}
        <div className="bg-card text-card-foreground rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">Current Date & Time</h2>
          <div className="space-y-2">
            <p className="text-lg">{formatDate(currentTime)}</p>
            <p className="text-3xl font-bold text-primary">{formatTime(currentTime)}</p>
          </div>
        </div>

        {/* Sessions Table */}
        <div className="bg-card text-card-foreground rounded-lg shadow-md">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b">
                  <th 
                    className="px-6 py-3 text-left cursor-pointer hover:bg-muted/50"
                    onClick={() => handleSort('activityName')}
                  >
                    Activity
                    <SortIcon field="activityName" />
                  </th>
                  <th 
                    className="px-6 py-3 text-left cursor-pointer hover:bg-muted/50"
                    onClick={() => handleSort('groupName')}
                  >
                    Group
                    <SortIcon field="groupName" />
                  </th>
                  <th 
                    className="px-6 py-3 text-left cursor-pointer hover:bg-muted/50"
                    onClick={() => handleSort('startTime')}
                  >
                    Start Time
                    <SortIcon field="startTime" />
                  </th>
                  <th 
                    className="px-6 py-3 text-left cursor-pointer hover:bg-muted/50"
                    onClick={() => handleSort('endTime')}
                  >
                    End Time
                    <SortIcon field="endTime" />
                  </th>
                  <th 
                    className="px-6 py-3 text-left cursor-pointer hover:bg-muted/50"
                    onClick={() => handleSort('reviewItemCount')}
                  >
                    Review Items
                    <SortIcon field="reviewItemCount" />
                  </th>
                </tr>
              </thead>
              <tbody>
                {paginatedSessions.map((session) => (
                  <tr key={session.id} className="border-b hover:bg-muted/50">
                    <td className="px-6 py-4">{session.activityName}</td>
                    <td className="px-6 py-4">
                      <Link
                        to={`/groups/${session.id}`}
                        className="text-primary hover:text-primary/80"
                      >
                        {session.groupName}
                      </Link>
                    </td>
                    <td className="px-6 py-4">{session.startTime}</td>
                    <td className="px-6 py-4">{session.endTime}</td>
                    <td className="px-6 py-4">{session.reviewItemCount}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          <div className="flex items-center justify-between px-6 py-4">
            <button
              className="px-4 py-2 text-sm font-medium rounded-md bg-primary text-white hover:bg-primary/80 disabled:opacity-50"
              onClick={() => setCurrentPage(currentPage - 1)}
              disabled={currentPage === 1}
            >
              Previous
            </button>
            <span className="text-sm">
              Page {currentPage} of {totalPages}
            </span>
            <button
              className="px-4 py-2 text-sm font-medium rounded-md bg-primary text-white hover:bg-primary/80 disabled:opacity-50"
              onClick={() => setCurrentPage(currentPage + 1)}
              disabled={currentPage === totalPages}
            >
              Next
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Sessions 