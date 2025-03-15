import { useState } from 'react';
import { Link } from 'react-router-dom';

interface Activity {
  id: number;
  title: string;
  description: string;
  imageUrl: string;
  skills: string[];
  difficulty: 'Beginner' | 'Intermediate' | 'Advanced';
  estimatedTime: string;
  category: 'Reading' | 'Writing' | 'Listening' | 'Speaking' | 'Grammar' | 'Vocabulary';
}

const activities: Activity[] = [
  {
    id: 1,
    title: 'Adventure MUD',
    description: 'Explore a text-based Japanese world where you interact with NPCs and learn contextual vocabulary.',
    imageUrl: 'https://placehold.co/600x400/3B82F6/FFFFFF/png?text=Adventure+MUD',
    skills: ['Reading', 'Vocabulary', 'Grammar'],
    difficulty: 'Intermediate',
    estimatedTime: '30 min',
    category: 'Reading'
  },
  {
    id: 2,
    title: 'Typing Tutor',
    description: 'Practice typing Japanese characters and improve your input speed with interactive exercises.',
    imageUrl: 'https://placehold.co/600x400/10B981/FFFFFF/png?text=Typing+Tutor',
    skills: ['Writing', 'Reading'],
    difficulty: 'Beginner',
    estimatedTime: '15 min',
    category: 'Writing'
  },
  {
    id: 3,
    title: 'Conversation Practice',
    description: 'Engage in simulated conversations with AI-powered characters to improve speaking skills.',
    imageUrl: 'https://placehold.co/600x400/8B5CF6/FFFFFF/png?text=Conversation',
    skills: ['Speaking', 'Listening'],
    difficulty: 'Intermediate',
    estimatedTime: '20 min',
    category: 'Speaking'
  },
  {
    id: 4,
    title: 'Kanji Recognition',
    description: 'Train your ability to recognize and write kanji characters through interactive exercises.',
    imageUrl: 'https://placehold.co/600x400/EC4899/FFFFFF/png?text=Kanji',
    skills: ['Reading', 'Writing'],
    difficulty: 'Advanced',
    estimatedTime: '25 min',
    category: 'Writing'
  },
  {
    id: 5,
    title: 'Listening Comprehension',
    description: 'Listen to native speakers and practice understanding natural Japanese conversations.',
    imageUrl: 'https://placehold.co/600x400/F59E0B/FFFFFF/png?text=Listening',
    skills: ['Listening'],
    difficulty: 'Intermediate',
    estimatedTime: '15 min',
    category: 'Listening'
  },
  {
    id: 6,
    title: 'Grammar Challenges',
    description: 'Test and improve your grammar knowledge through interactive quizzes and exercises.',
    imageUrl: 'https://placehold.co/600x400/6366F1/FFFFFF/png?text=Grammar',
    skills: ['Grammar'],
    difficulty: 'Advanced',
    estimatedTime: '20 min',
    category: 'Grammar'
  }
];

const categories = ['All', 'Reading', 'Writing', 'Listening', 'Speaking', 'Grammar', 'Vocabulary'] as const;
const difficulties = ['All', 'Beginner', 'Intermediate', 'Advanced'] as const;

const StudyActivities = () => {
  const [selectedCategory, setSelectedCategory] = useState<typeof categories[number]>('All');
  const [selectedDifficulty, setSelectedDifficulty] = useState<typeof difficulties[number]>('All');
  const [searchQuery, setSearchQuery] = useState('');

  const filteredActivities = activities.filter(activity => {
    const matchesCategory = selectedCategory === 'All' || activity.category === selectedCategory;
    const matchesDifficulty = selectedDifficulty === 'All' || activity.difficulty === selectedDifficulty;
    const matchesSearch = activity.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         activity.description.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCategory && matchesDifficulty && matchesSearch;
  });

  const DifficultyBadge = ({ difficulty }: { difficulty: Activity['difficulty'] }) => {
    const colors = {
      Beginner: 'bg-green-100 text-green-800',
      Intermediate: 'bg-yellow-100 text-yellow-800',
      Advanced: 'bg-red-100 text-red-800'
    };

    return (
      <span className={`px-2 py-1 rounded-full text-xs font-medium ${colors[difficulty]}`}>
        {difficulty}
      </span>
    );
  };

  const SkillBadge = ({ skill }: { skill: string }) => {
    const colors: Record<'Reading' | 'Writing' | 'Listening' | 'Speaking' | 'Grammar' | 'Vocabulary', string> = {
      Reading: 'bg-blue-100 text-blue-800',
      Writing: 'bg-green-100 text-green-800',
      Listening: 'bg-yellow-100 text-yellow-800',
      Speaking: 'bg-purple-100 text-purple-800',
      Grammar: 'bg-indigo-100 text-indigo-800',
      Vocabulary: 'bg-pink-100 text-pink-800'
    };

    return (
      <span className={`px-2 py-1 rounded-full text-xs font-medium ${colors[skill as keyof typeof colors] || 'bg-gray-100 text-gray-800'}`}>
        {skill}
      </span>
    );
  };

  return (
    <div className="container mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Study Activities</h1>
        <p className="text-muted-foreground mt-2">Choose an activity to practice your Japanese skills</p>
      </div>

      {/* Current Date & Time Card */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-semibold mb-2">Available Activities</h2>
            <p className="text-muted-foreground">
              {filteredActivities.length} activities match your criteria
            </p>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-8">
        <div className="space-y-4">
          <div className="flex flex-wrap gap-4">
            <div className="flex-1">
              <input
                type="text"
                placeholder="Search activities..."
                className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent dark:bg-gray-700 dark:text-white"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
            <select
              className="px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent dark:bg-gray-700 dark:text-white"
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value as typeof categories[number])}
            >
              {categories.map(category => (
                <option key={category} value={category}>{category}</option>
              ))}
            </select>
            <select
              className="px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent dark:bg-gray-700 dark:text-white"
              value={selectedDifficulty}
              onChange={(e) => setSelectedDifficulty(e.target.value as typeof difficulties[number])}
            >
              {difficulties.map(difficulty => (
                <option key={difficulty} value={difficulty}>{difficulty}</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Activity Cards */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {filteredActivities.map(activity => (
          <div key={activity.id} className="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden">
            <img
              src={activity.imageUrl}
              alt={activity.title}
              className="w-full h-48 object-cover"
            />
            <div className="p-6">
              <h3 className="text-xl font-semibold mb-2">{activity.title}</h3>
              <p className="text-muted-foreground mb-4">{activity.description}</p>
              
              <div className="space-y-4">
                <div className="flex flex-wrap gap-2">
                  {activity.skills.map(skill => (
                    <SkillBadge key={skill} skill={skill} />
                  ))}
                </div>
                
                <div className="flex items-center justify-between">
                  <DifficultyBadge difficulty={activity.difficulty} />
                  <span className="text-sm text-muted-foreground">{activity.estimatedTime}</span>
                </div>

                <div className="flex gap-2 mt-4">
                  <Link
                    to={`/study-activities/${activity.id}`}
                    className="flex-1 px-4 py-2 text-sm font-medium text-center rounded-md bg-primary/10 text-primary hover:bg-primary/20 transition-colors"
                  >
                    View Details
                  </Link>
                  <a
                    href={`http://localhost:8081?group_id=${activity.id}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex-1 px-4 py-2 text-sm font-medium text-center rounded-md bg-primary text-white hover:bg-primary/90 transition-colors"
                  >
                    Launch Activity
                  </a>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {filteredActivities.length === 0 && (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-12 text-center">
          <p className="text-lg text-muted-foreground">No activities found matching your criteria.</p>
        </div>
      )}
    </div>
  );
};

export default StudyActivities; 