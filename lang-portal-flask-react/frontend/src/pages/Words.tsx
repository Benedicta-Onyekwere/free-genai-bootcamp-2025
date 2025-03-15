import { useState } from 'react'
import { Link } from 'react-router-dom'

interface Word {
  id: number
  japanese: string
  romaji: string
  english: string
  correctCount: number
  wrongCount: number
  audioUrl?: string
}

interface WordsProps {
  groupId?: string
}

const words: Word[] = [
  {
    id: 1,
    japanese: '始める',
    romaji: 'hajimeru',
    english: 'to begin',
    correctCount: 10,
    wrongCount: 2,
    audioUrl: '/audio/hajimeru.mp3',
  },
  {
    id: 2,
    japanese: '食べる',
    romaji: 'taberu',
    english: 'to eat',
    correctCount: 15,
    wrongCount: 1,
    audioUrl: '/audio/taberu.mp3',
  },
]

type SortField = keyof Omit<Word, 'id' | 'audioUrl'>
type SortDirection = 'asc' | 'desc'

export default function Words({ groupId }: WordsProps) {
  const [currentPage, setCurrentPage] = useState(1)
  const [sortField, setSortField] = useState<SortField>('japanese')
  const [sortDirection, setSortDirection] = useState<SortDirection>('asc')

  const itemsPerPage = 50
  const totalPages = Math.ceil(words.length / itemsPerPage)

  const sortedWords = [...words].sort((a, b) => {
    const aValue = a[sortField]
    const bValue = b[sortField]
    const direction = sortDirection === 'asc' ? 1 : -1

    if (typeof aValue === 'string' && typeof bValue === 'string') {
      return direction * aValue.localeCompare(bValue)
    }
    if (typeof aValue === 'number' && typeof bValue === 'number') {
      return direction * (aValue - bValue)
    }
    return 0
  })

  const paginatedWords = sortedWords.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  )

  const handleSort = (field: SortField) => {
    if (field === sortField) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc')
    } else {
      setSortField(field)
      setSortDirection('asc')
    }
  }

  const SortArrow = ({ field }: { field: SortField }) => {
    if (field !== sortField) return null
    return (
      <span className="ml-1">
        {sortDirection === 'asc' ? '↓' : '↑'}
      </span>
    )
  }

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Words</h1>
      <div className="bg-white shadow rounded-lg overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th
                  scope="col"
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                  onClick={() => handleSort('japanese')}
                >
                  Japanese <SortArrow field="japanese" />
                </th>
                <th
                  scope="col"
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                  onClick={() => handleSort('romaji')}
                >
                  Romaji <SortArrow field="romaji" />
                </th>
                <th
                  scope="col"
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                  onClick={() => handleSort('english')}
                >
                  English <SortArrow field="english" />
                </th>
                <th
                  scope="col"
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                  onClick={() => handleSort('correctCount')}
                >
                  # Correct <SortArrow field="correctCount" />
                </th>
                <th
                  scope="col"
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                  onClick={() => handleSort('wrongCount')}
                >
                  # Wrong <SortArrow field="wrongCount" />
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {paginatedWords.map((word) => (
                <tr key={word.id}>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <Link
                        to={`/words/${word.id}`}
                        className="text-primary hover:text-primary/80"
                      >
                        {word.japanese}
                      </Link>
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
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">{word.romaji}</td>
                  <td className="px-6 py-4 whitespace-nowrap">{word.english}</td>
                  <td className="px-6 py-4 whitespace-nowrap">{word.correctCount}</td>
                  <td className="px-6 py-4 whitespace-nowrap">{word.wrongCount}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6">
          <div className="flex-1 flex justify-between sm:hidden">
            <button
              onClick={() => setCurrentPage(currentPage - 1)}
              disabled={currentPage === 1}
              className="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Previous
            </button>
            <button
              onClick={() => setCurrentPage(currentPage + 1)}
              disabled={currentPage === totalPages}
              className="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Next
            </button>
          </div>
          <div className="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
            <div>
              <p className="text-sm text-gray-700">
                Page <span className="font-medium">{currentPage}</span> of{' '}
                <span className="font-medium">{totalPages}</span>
              </p>
            </div>
            <div>
              <nav className="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
                <button
                  onClick={() => setCurrentPage(currentPage - 1)}
                  disabled={currentPage === 1}
                  className="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Previous
                </button>
                <button
                  onClick={() => setCurrentPage(currentPage + 1)}
                  disabled={currentPage === totalPages}
                  className="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Next
                </button>
              </nav>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
} 