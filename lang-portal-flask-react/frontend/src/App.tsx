import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { DarkModeProvider } from './contexts/DarkModeContext'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import StudyActivities from './pages/StudyActivities'
import StudyActivityDetails from './pages/StudyActivityDetails'
import Words from './pages/Words'
import WordDetails from './pages/WordDetails'
import Groups from './pages/Groups'
import GroupDetails from './pages/GroupDetails'
import Sessions from './pages/Sessions'
import Settings from './pages/Settings'

export default function App() {
  return (
    <DarkModeProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<Navigate to="/dashboard" replace />} />
            <Route path="dashboard" element={<Dashboard />} />
            <Route path="study-activities" element={<StudyActivities />} />
            <Route path="study-activities/:id" element={<StudyActivityDetails />} />
            <Route path="words" element={<Words />} />
            <Route path="words/:id" element={<WordDetails />} />
            <Route path="groups" element={<Groups />} />
            <Route path="groups/:id" element={<GroupDetails />} />
            <Route path="sessions" element={<Sessions />} />
            <Route path="settings" element={<Settings />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </DarkModeProvider>
  )
}
