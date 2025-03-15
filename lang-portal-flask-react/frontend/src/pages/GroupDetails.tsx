import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import Words from './Words'

interface Group {
  id: number
  name: string
  description: string
  wordCount: number
}

export default function GroupDetails() {
  const { id } = useParams()
  const [group, setGroup] = useState<Group | null>(null)

  // TODO: Replace with actual API call
  useEffect(() => {
    setGroup({
      id: Number(id),
      name: 'Core Verbs',
      description: 'Essential Japanese verbs for daily conversation',
      wordCount: 50,
    })
  }, [id])

  if (!group) {
    return <div>Loading...</div>
  }

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">{group.name}</h1>

      {/* Group Information */}
      <div className="bg-white shadow rounded-lg p-6 mb-6">
        <div className="space-y-4">
          <div>
            <h2 className="text-sm font-medium text-gray-500">Description</h2>
            <p className="mt-1">{group.description}</p>
          </div>
          <div>
            <h2 className="text-sm font-medium text-gray-500">Word Count</h2>
            <p className="mt-1 text-2xl font-semibold text-primary">{group.wordCount}</p>
          </div>
        </div>
      </div>

      {/* Words List */}
      <div className="mt-6">
        <h2 className="text-lg font-medium mb-4">Words in this Group</h2>
        <Words groupId={id} />
      </div>
    </div>
  )
} 