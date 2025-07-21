import React from 'react';
import { Link } from 'react-router-dom';
import HealthMonitor from './HealthMonitor';

const MainPage = () => {
  const menuItems = [
    { icon: 'images/eye.png', text: 'Student Learning Recommendation System', path: 'http://localhost:8501/' },
    { icon: 'images/online.png', text: 'QUESTION ANSWER EVALUATION', path: 'http://127.0.0.1:5055/' },
    { icon: 'images/3d-resourses.png', text: '3D LEARNING RESOURCES ', path: '/resourse' },
    { icon: 'images/aiboard.png', text: 'AI BOARD ', path: 'http://localhost:5174/' },
    { icon: 'images/codeplay.png', text: 'CODE PLAYGROUND', path: 'https://testcodeplay-adithyavenna-adithyavennas-projects.vercel.app' },
    { icon: 'images/chatbot.png', text: 'CHAT BOT', path: 'http://localhost:8502/' },
    { icon: 'images/eye.png', text: 'STUDENT-FACULTY-ADMIN', path: 'http://127.0.0.1:8000/' },
    // { icon: 'images/health-monitor.png', text: 'HEALTH MONITOR', path: '/health-monit
    // or' }, // New menu item
  ];



  
  return (
    <div className="flex min-h-screen bg-white">
      {/* Left Sidebar */}
      <div className="w-80 bg-white p-6 shadow-lg">
        <div className="mb-12">
          <img src="images/aspiro-icon.png" alt="Aspiro Logo" className="h-8" />
          <span className="text-black text-2xl font-semibold">ASPIRO</span>
        </div>
        
        <nav>
          {menuItems.map((item, index) => (
            <Link
              to={item.path}
              key={index}
            >
              <div
                className="flex items-center space-x-4 mb-6 p-3 hover:bg-blue-50 rounded-lg cursor-pointer transition-all"
              >
                <img src={item.icon} alt="" className="w-6 h-6" />
                <span className="text-sm font-medium text-gray-700">{item.text}</span>
              </div>
            </Link>
          ))}
        </nav>
      </div>

      {/* Main Content */}
      <div className="flex-1 bg-indigo-700 p-12 relative overflow-hidden">
        <div className="max-w-2xl text-white z-10 relative">
          <h1 className="text-5xl font-bold mb-6 leading-tight tracking-wider">
            ALWAYS READY
            <br />
            TO MAKE YOUR
            <br />
            LIFE BETTER
          </h1>
          <p className="text-xl opacity-90">Learn without limits</p>
        </div>
        
        {/* 3D Shape */}
        <div className="absolute right-0 middle-0 transform translate-x-1 translate-y-1">
          <img 
            src="images/main.png"
            alt="Decorative Shape"
            className="w-150 h-150 object-contain opacity-90"
          />
        </div>
      </div>
    </div>
  );
};

export default MainPage;
