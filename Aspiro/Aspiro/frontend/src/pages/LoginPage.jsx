import { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import Header from '../components/Header';
import Navbar from '../components/Navbar';

// First, add this to your index.html in the public directory:
// <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.3.0/model-viewer.min.js"></script>

export default function LoginPage() {
  const navigate = useNavigate();
  const modelViewerRef = useRef(null);
  
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });

  // Remove the dynamic import since we're loading model-viewer via CDN
  useEffect(() => {
    // You can add any initialization logic for the model viewer here if needed
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch('http://localhost:5173/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      
      if (res.ok) {
        const data = await res.json();
        localStorage.setItem('token', data.token);
        navigate('/main');
      }
    } catch (error) {
      console.error('Login error:', error);
    }
  };

  return (
    <>
     <Navbar />
    
      <div className="min-h-screen bg-gradient-to-r from-pink-300 to-rose-200">
        <div className="container mx-auto px-4 py-8">
          <Header />
          <div className="mt-8 flex flex-col md:flex-row items-center gap-8">
            <motion.div 
              className="flex-1"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
            >
              <h1 className="text-4xl font-bold text-white mb-4">
                Transforming education, making learning engaging and inclusive.
              </h1>
              
              <div className="model-viewer-container w-full max-w-4xl mx-auto aspect-video bg-transparent">
                <model-viewer
                  id="threedd"
                  ref={modelViewerRef}
                  src="images/login.glb"
                  camera-controls
                  auto-rotate
                  rotation-per-second="120deg"
                  shadow-intensity="1"
                  shadow-softness="0.7"
                  exposure="1.2"
                  environment-image="neutral"
                  camera-orbit="0deg 75deg 4m"
                  min-camera-orbit="auto auto auto"
                  max-camera-orbit="auto auto 50m"
                  className="w-full h-full"
                  ar-status="not-presenting"
                  interpolation-decay="200"
                ></model-viewer>
              </div>
            </motion.div>

            <motion.div 
              className="flex-1 bg-white rounded-lg p-8 shadow-lg w-full md:max-w-md"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.5 }}
            >
              <h2 className="text-2xl font-bold mb-6">Login Account</h2>
              <form onSubmit={handleSubmit} className="space-y-4">
                <input
                  type="email"
                  placeholder="Email"
                  className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                  onChange={(e) => setFormData({...formData, email: e.target.value})}
                />
                <input
                  type="password"
                  placeholder="Password"
                  className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                  onChange={(e) => setFormData({...formData, password: e.target.value})}
                />
                <button
                className="w-full mt-4 py-2 border rounded-lg flex items-center justify-center gap-2 hover:bg-gray-50 transition-colors"
              onClick={() => window.location.href = "http://localhost:5173/main"}
                >
                Login
                </button>
              </form>
              
              <button
                className="w-full mt-4 py-2 border rounded-lg flex items-center justify-center gap-2 hover:bg-gray-50 transition-colors"
                onClick={() => {/* Implement Google Login */}}
              >
                <img src="images/google.png" alt="" className="h-5 w-5" />
                Login with Google
              </button>
              
              <p className="mt-4 text-center">
                Don't have an account?{' '}
                <button
                  className="text-blue-600 hover:underline"
                  onClick={() => navigate('/')}
                >
                  Sign up
                </button>
              </p>
            </motion.div>
          </div>
        </div>
      </div>
    </>
  );
}