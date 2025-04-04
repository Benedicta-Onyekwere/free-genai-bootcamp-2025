import { Outlet } from 'react-router-dom'
import Navigation from './Navigation'
import Breadcrumbs from './Breadcrumbs'

export default function Layout() {
  return (
    <div className="min-h-screen bg-gray-100">
      <Navigation />
      <Breadcrumbs />
      <main className="py-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <Outlet />
        </div>
      </main>
    </div>
  )
} 