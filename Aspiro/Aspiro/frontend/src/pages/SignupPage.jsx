import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import Header from '../components/Header';
import Navbar from '../components/Navbar';

export default function SignupPage() {
  const navigate = useNavigate();
  const modelViewerRef = useRef(null);

  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    password: ''
  });

  useEffect(() => {
    // Load model-viewer script dynamically
    const script = document.createElement('script');
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/model-viewer/3.1.1/model-viewer.min.js';
    script.async = true;
    document.body.appendChild(script);

    return () => {
      document.body.removeChild(script);
    };
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch('http://localhost:5006/api/auth/register', {
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
      console.error('Registration error:', error);
    }
  };

  return (
    <>
     <Navbar />
      <div className="min-h-screen bg-gradient-to-r from-pink-300 to-rose-200">
        <div className="container mx-auto px-4 py-8">
          <Header />
          <div className="mt-8 flex flex-col lg:flex-row items-center gap-8">
            <motion.div 
              className="flex-1"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6 }}
            >
              <h1 className="text-4xl font-bold text-white mb-4">
                Transforming education, making learning engaging and inclusive.
              </h1>
              <div className="model-viewer-container w-full aspect-square lg:aspect-video bg-transparent">
                <model-viewer
                  id="classroom-model"
                  ref={modelViewerRef}
                  src="images/signup.glb"
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
              className="flex-1 w-full max-w-md bg-white rounded-lg p-8 shadow-lg"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6 }}
            >
              <h2 className="text-2xl font-bold mb-6">Create Account</h2>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <input
                    type="text"
                    placeholder="First Name"
                    className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                    onChange={(e) => setFormData({...formData, firstName: e.target.value})}
                  />
                  <input
                    type="text"
                    placeholder="Last Name"
                    className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                    onChange={(e) => setFormData({...formData, lastName: e.target.value})}
                  />
                </div>
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
                  type="submit"
                  className="w-full py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Create New Account
                </button>
              </form>
              <button
                className="w-full mt-4 py-2 border rounded-lg flex items-center justify-center gap-2 hover:bg-gray-50 transition-colors"
              onClick={() => window.location.href = "http://localhost:5173/main"}
                >
                Login
                </button>

              <p className="mt-4 text-center">
                Already have an account?{' '}
                <button
                  className="text-blue-600 hover:underline"
                  onClick={() => navigate('/login')}
                >
                  Login
                </button>
              </p>
            </motion.div>
          </div>
        </div>
      </div>
    </>
  );
}