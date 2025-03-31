import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'

interface Session {
  id: number
  groupName: string
  startTime: string
  endTime: string
  reviewItemCount: number
}

interface StudyActivity {
  id: number
  title: string
  description: string
  thumbnail: string
  launchUrl: string
}

export default function StudyActivityDetails() {
  const { id } = useParams()
  const [activity, setActivity] = useState<StudyActivity | null>(null)
  const [sessions, setSessions] = useState<Session[]>([])

  // TODO: Replace with actual API calls
  useEffect(() => {
    setActivity({
      id: Number(id),
      title: 'Adventure MUD',
      description:
        'An interactive text adventure game that helps you learn Japanese through immersive storytelling and real-world scenarios.',
      thumbnail: '/thumbnails/adventure-mud.jpg',
      launchUrl: 'http://localhost:8501',
    })

    setSessions([
      {
        id: 1,
        groupName: 'Core Verbs',
        startTime: '2024-03-20 14:30',
        endTime: '2024-03-20 15:00',
        reviewItemCount: 25,
      },
      {
        id: 2,
        groupName: 'JLPT N5',
        startTime: '2024-03-19 10:15',
        endTime: '2024-03-19 10:45',
        reviewItemCount: 30,
      },
    ])
  }, [id])

  const handleLaunch = () => {
    if (activity) {
      // TODO: Get selected group ID from user
      const groupId = 4
      window.open(`${activity.launchUrl}?group_id=${groupId}`, '_blank')
    }
  }

  if (!activity) {
    return <div>Loading...</div>
  }

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">{activity.title}</h1>

      {/* Activity Information */}
      <div className="bg-white shadow rounded-lg overflow-hidden mb-6">
        <div className="aspect-w-16 aspect-h-9">
          <img
            src={activity.thumbnail}
            alt={activity.title}
            className="w-full h-full object-cover"
          />
        </div>
        <div className="p-6">
          <p className="text-gray-600 mb-4">{activity.description}</p>
          <button
            onClick={handleLaunch}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
          >
            Launch Activity
          </button>
        </div>
      </div>

      {/* Sessions List */}
      <div className="bg-white shadow rounded-lg overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-medium">Recent Sessions</h2>
        </div>
        <div className="divide-y divide-gray-200">
          {sessions.map((session) => (
            <div key={session.id} className="px-6 py-4">
              <div className="flex justify-between items-center">
                <div>
                  <Link
                    to={`/groups/${session.id}`}
                    className="text-primary hover:text-primary/80 font-medium"
                  >
                    {session.groupName}
                  </Link>
                  <div className="text-sm text-gray-500 mt-1">
                    {session.startTime} - {session.endTime}
                  </div>
                </div>
                <div className="text-sm">
                  <span className="font-medium">{session.reviewItemCount}</span>{' '}
                  <span className="text-gray-500">review items</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
} 