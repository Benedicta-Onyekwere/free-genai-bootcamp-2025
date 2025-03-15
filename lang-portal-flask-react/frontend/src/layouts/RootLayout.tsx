import { Link, Outlet, useLocation } from 'react-router-dom'

const navigation = [
  { name: 'Dashboard', href: '/dashboard' },
  { name: 'Study Activities', href: '/study-activities' },
  { name: 'Words', href: '/words' },
  { name: 'Word Groups', href: '/groups' },
  { name: 'Sessions', href: '/sessions' },
  { name: 'Settings', href: '/settings' },
] as const

export default function RootLayout() {
  const location = useLocation()
  const pathSegments = location.pathname.split('/').filter(Boolean)

  return (
    <div className="min-h-screen bg-background">
      {/* Navigation */}
      <nav className="bg-white shadow">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 justify-between">
            <div className="flex">
              <div className="flex flex-shrink-0 items-center">
                <span className="text-xl font-bold text-primary">Japanese Learning Portal</span>
              </div>
              <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                {navigation.map((item) => (
                  <Link
                    key={item.name}
                    to={item.href}
                    className={`inline-flex items-center border-b-2 px-1 pt-1 text-sm font-medium ${
                      location.pathname.startsWith(item.href)
                        ? 'border-primary text-gray-900'
                        : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
                    }`}
                  >
                    {item.name}
                  </Link>
                ))}
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Breadcrumbs */}
      <nav className="bg-white border-b" aria-label="Breadcrumb">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex h-10 items-center space-x-4">
            <ol className="flex">
              {pathSegments.map((segment: string, index: number) => {
                const path = `/${pathSegments.slice(0, index + 1).join('/')}`
                const isLast = index === pathSegments.length - 1

                return (
                  <li key={path} className="flex items-center">
                    {index > 0 && (
                      <svg
                        className="h-5 w-5 flex-shrink-0 text-gray-300"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                        aria-hidden="true"
                      >
                        <path d="M5.555 17.776l8-16 .894.448-8 16-.894-.448z" />
                      </svg>
                    )}
                    <Link
                      to={path}
                      className={`ml-4 text-sm font-medium ${
                        isLast
                          ? 'text-gray-500'
                          : 'text-gray-700 hover:text-primary'
                      }`}
                      aria-current={isLast ? 'page' : undefined}
                    >
                      {segment.charAt(0).toUpperCase() + segment.slice(1)}
                    </Link>
                  </li>
                )
              })}
            </ol>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
        <Outlet />
      </main>
    </div>
  )
} 