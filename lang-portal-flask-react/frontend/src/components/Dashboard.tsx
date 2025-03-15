import { useState, useEffect } from 'react';

const Dashboard = () => {
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    // Update time every second
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    // Cleanup interval on component unmount
    return () => clearInterval(timer);
  }, []);

  const formatDate = (date: Date) => {
    return new Intl.DateTimeFormat('en-US', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    }).format(date);
  };

  const formatTime = (date: Date) => {
    return new Intl.DateTimeFormat('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: true,
    }).format(date);
  };

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-8">Dashboard</h1>
      
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {/* Date and Time Card */}
        <div className="bg-card text-card-foreground rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">Current Date & Time</h2>
          <div className="space-y-2">
            <p className="text-lg">{formatDate(currentTime)}</p>
            <p className="text-3xl font-bold text-primary">{formatTime(currentTime)}</p>
          </div>
        </div>

        {/* Last Session Card - Placeholder */}
        <div className="bg-card text-card-foreground rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">Last Session</h2>
          <p className="text-muted-foreground">No recent sessions</p>
        </div>

        {/* Progress Summary Card - Placeholder */}
        <div className="bg-card text-card-foreground rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">Progress Summary</h2>
          <p className="text-muted-foreground">Start your learning journey</p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 