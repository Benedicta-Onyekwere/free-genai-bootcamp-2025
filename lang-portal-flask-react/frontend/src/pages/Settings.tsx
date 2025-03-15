import { useState } from 'react'
import { useDarkMode } from '../contexts/DarkModeContext'

interface SettingsState {
  dailyGoal: number
  notificationsEnabled: boolean
  soundEnabled: boolean
  theme: 'light' | 'dark' | 'system'
  difficulty: 'beginner' | 'intermediate' | 'advanced'
  primaryLanguage: string
  interfaceLanguage: string
}

const Settings = () => {
  const { isDarkMode, toggleDarkMode } = useDarkMode()
  const [settings, setSettings] = useState<SettingsState>({
    dailyGoal: 30,
    notificationsEnabled: true,
    soundEnabled: true,
    theme: isDarkMode ? 'dark' : 'light',
    difficulty: 'intermediate',
    primaryLanguage: 'Japanese',
    interfaceLanguage: 'English'
  })

  const languages = ['English', 'Japanese', 'Spanish', 'French', 'German', 'Chinese']
  const difficultyLevels = ['beginner', 'intermediate', 'advanced']
  const themes = ['light', 'dark', 'system']

  const handleNumberChange = (field: keyof SettingsState, value: string) => {
    const numValue = parseInt(value)
    if (!isNaN(numValue)) {
      setSettings(prev => ({ ...prev, [field]: numValue }))
    }
  }

  const handleToggle = (field: keyof SettingsState) => {
    setSettings(prev => ({ ...prev, [field]: !prev[field] }))
  }

  const handleSelectChange = (field: keyof SettingsState, value: string) => {
    if (field === 'theme') {
      if (value === 'dark') {
        !isDarkMode && toggleDarkMode()
      } else if (value === 'light') {
        isDarkMode && toggleDarkMode()
      }
      // For 'system', we could add system preference detection here
    }
    setSettings(prev => ({ ...prev, [field]: value }))
  }

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-8">Settings</h1>
      
      <div className="space-y-6">
        {/* Study Settings */}
        <div className="bg-card text-card-foreground rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">Study Settings</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">Daily Study Goal (minutes)</label>
              <input
                type="number"
                min="5"
                max="240"
                value={settings.dailyGoal}
                onChange={(e) => handleNumberChange('dailyGoal', e.target.value)}
                className="w-full max-w-xs px-3 py-2 border rounded-md"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Difficulty Level</label>
              <select
                value={settings.difficulty}
                onChange={(e) => handleSelectChange('difficulty', e.target.value)}
                className="w-full max-w-xs px-3 py-2 border rounded-md capitalize"
              >
                {difficultyLevels.map(level => (
                  <option key={level} value={level} className="capitalize">
                    {level}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Language Settings */}
        <div className="bg-card text-card-foreground rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">Language Settings</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">Primary Learning Language</label>
              <select
                value={settings.primaryLanguage}
                onChange={(e) => handleSelectChange('primaryLanguage', e.target.value)}
                className="w-full max-w-xs px-3 py-2 border rounded-md"
              >
                {languages.map(lang => (
                  <option key={lang} value={lang}>
                    {lang}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Interface Language</label>
              <select
                value={settings.interfaceLanguage}
                onChange={(e) => handleSelectChange('interfaceLanguage', e.target.value)}
                className="w-full max-w-xs px-3 py-2 border rounded-md"
              >
                {languages.map(lang => (
                  <option key={lang} value={lang}>
                    {lang}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Appearance Settings */}
        <div className="bg-card text-card-foreground rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">Appearance</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">Theme</label>
              <select
                value={settings.theme}
                onChange={(e) => handleSelectChange('theme', e.target.value)}
                className="w-full max-w-xs px-3 py-2 border rounded-md capitalize"
              >
                {themes.map(theme => (
                  <option key={theme} value={theme} className="capitalize">
                    {theme}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Notification Settings */}
        <div className="bg-card text-card-foreground rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">Notifications & Sound</h2>
          <div className="space-y-4">
            <div className="flex items-center justify-between max-w-xs">
              <label className="text-sm font-medium">Enable Notifications</label>
              <button
                onClick={() => handleToggle('notificationsEnabled')}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                  settings.notificationsEnabled ? 'bg-primary' : 'bg-gray-200'
                }`}
              >
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                    settings.notificationsEnabled ? 'translate-x-6' : 'translate-x-1'
                  }`}
                />
              </button>
            </div>
            <div className="flex items-center justify-between max-w-xs">
              <label className="text-sm font-medium">Enable Sound Effects</label>
              <button
                onClick={() => handleToggle('soundEnabled')}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                  settings.soundEnabled ? 'bg-primary' : 'bg-gray-200'
                }`}
              >
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                    settings.soundEnabled ? 'translate-x-6' : 'translate-x-1'
                  }`}
                />
              </button>
            </div>
          </div>
        </div>

        {/* Save Button */}
        <div className="flex justify-end">
          <button
            onClick={() => console.log('Settings saved:', settings)}
            className="px-4 py-2 bg-primary text-white rounded-md hover:bg-primary/80 transition-colors"
          >
            Save Changes
          </button>
        </div>
      </div>
    </div>
  )
}

export default Settings 