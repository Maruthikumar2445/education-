import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import LandingPage from './components/LandingPage';
import SignupPage from './pages/SignupPage';
import LoginPage from './pages/LoginPage';
import MainPage from './pages/MainPage';
import LearningResources from './pages/LearningResources';
import PlantPage from './pages/PlantPage';
import HeartPage from './pages/HeartPage';
import DigestivePage from './pages/DigestivePage';
import MicroPage from './pages/MicroPage';
import HealthMonitor from './pages/HealthMonitor'; // New import

const App = () => {
  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-black via-indigo-900 to-indigo-800 overflow-hidden">
        <div className="relative">
          {/* <Navbar /> */}
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/signup" element={<SignupPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/main" element={<MainPage />} />
            <Route path="/resourse" element={<LearningResources />} />
            <Route path="/plant" element={<PlantPage />} />
            <Route path="/heart" element={<HeartPage />} />
            <Route path="/micro" element={<MicroPage />} />
            <Route path="/digestive" element={<DigestivePage />} />
            <Route path="/health-monitor" element={<HealthMonitor />} /> {/* New route */}
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
