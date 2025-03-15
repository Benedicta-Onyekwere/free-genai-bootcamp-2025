import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'

interface Word {
  id: number
  japanese: string
  romaji: string
  english: string
  correctCount: number
  wrongCount: number
  audioUrl?: string
  groups: string[]
}

interface ReviewItem {
  id: number
  activityName: string
  timestamp: string
  isCorrect: boolean
}

export default function WordDetails() {
  const { id } = useParams()
  const [word, setWord] = useState<Word | null>(null)
  const [reviewItems, setReviewItems] = useState<ReviewItem[]>([])

  // TODO: Replace with actual API calls
  useEffect(() => {
    setWord({
      id: Number(id),
      japanese: '始める',
      romaji: 'hajimeru',
      english: 'to begin',
      correctCount: 10,
      wrongCount: 2,
      audioUrl: '/audio/hajimeru.mp3',
      groups: ['Core Verbs', 'JLPT N5'],
    })

    setReviewItems([
      {
        id: 1,
        activityName: 'Adventure MUD',
        timestamp: '2024-03-20 14:35',
        isCorrect: true,
      },
      {
        id: 2,
        activityName: 'Typing Tutor',
        timestamp: '2024-03-19 10:20',
        isCorrect: false,
      },
    ])
  }, [id])

  if (!word) {
    return <div>Loading...</div>
  }

  const accuracy = word.correctCount + word.wrongCount > 0
    ? ((word.correctCount / (word.correctCount + word.wrongCount)) * 100).toFixed(1)
    : 0

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">{word.japanese}</h1>

      {/* Word Information */}
      <div className="bg-white shadow rounded-lg p-6 mb-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <div className="mb-4">
              <h2 className="text-sm font-medium text-gray-500">Japanese</h2>
              <p className="mt-1 text-lg">
                {word.japanese}
                {word.audioUrl && (
                  <button
                    className="ml-2 text-gray-400 hover:text-gray-600"
                    onClick={() => {
                      const audio = new Audio(word.audioUrl)
                      audio.play()
                    }}
                  >
                    🔊
                  </button>
                )}
              </p>
            </div>
            <div className="mb-4">
              <h2 className="text-sm font-medium text-gray-500">Romaji</h2>
              <p className="mt-1 text-lg">{word.romaji}</p>
            </div>
            <div>
              <h2 className="text-sm font-medium text-gray-500">English</h2>
              <p className="mt-1 text-lg">{word.english}</p>
            </div>
          </div>
          <div>
            <div className="mb-4">
              <h2 className="text-sm font-medium text-gray-500">Groups</h2>
              <div className="mt-1 space-x-2">
                {word.groups.map((group) => (
                  <span
                    key={group}
                    className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary/10 text-primary"
                  >
                    {group}
                  </span>
                ))}
              </div>
            </div>
            <div>
              <h2 className="text-sm font-medium text-gray-500">Review Stats</h2>
              <div className="mt-1 grid grid-cols-3 gap-4">
                <div>
                  <p className="text-2xl font-semibold text-green-600">{word.correctCount}</p>
                  <p className="text-sm text-gray-500">Correct</p>
                </div>
                <div>
                  <p className="text-2xl font-semibold text-red-600">{word.wrongCount}</p>
                  <p className="text-sm text-gray-500">Wrong</p>
                </div>
                <div>
                  <p className="text-2xl font-semibold text-primary">{accuracy}%</p>
                  <p className="text-sm text-gray-500">Accuracy</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Review History */}
      <div className="bg-white shadow rounded-lg overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-medium">Review History</h2>
        </div>
        <div className="divide-y divide-gray-200">
          {reviewItems.map((item) => (
            <div key={item.id} className="px-6 py-4">
              <div className="flex justify-between items-center">
                <div>
                  <span className="font-medium">{item.activityName}</span>
                  <div className="text-sm text-gray-500 mt-1">{item.timestamp}</div>
                </div>
                <div
                  className={`text-sm font-medium ${
                    item.isCorrect ? 'text-green-600' : 'text-red-600'
                  }`}
                >
                  {item.isCorrect ? 'Correct' : 'Wrong'}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
} 