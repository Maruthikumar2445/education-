import { motion } from 'framer-motion'
import { useEffect, useState, useRef } from 'react'
import AboutUs from './AboutUs';
import Features from './Features';
import Hallmark from './Hallmark';
import Solid from './Solid';
import Contact from './Contact';
import Navbar from './Navbar';

const LandingPage = () => {
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 })
  const modelViewerRef = useRef(null)

  useEffect(() => {
    const modelViewer = document.querySelector('#threedd')
    if (modelViewer) {
      modelViewerRef.current = modelViewer

      modelViewer.addEventListener('load', () => {
        // Increase the camera distance to zoom out (adjust 4m value as needed)
        modelViewer.cameraOrbit = '0deg 75deg 4m'
        modelViewer.cameras.defaults.orbit.minPolarAngle = 60
        modelViewer.cameras.defaults.orbit.maxPolarAngle = 90
        modelViewer.autoRotate = false
      })

      // Mouse move handler
      const handleMouseMove = (event) => {
        const { clientX, clientY } = event
        const { innerWidth, innerHeight } = window

        // Calculate mouse position as percentage of window size
        const xPercentage = (clientX / innerWidth - 0.5) * 2 // -1 to 1
        const yPercentage = (clientY / innerHeight - 0.5) * 2 // -1 to 1

        setMousePosition({ x: xPercentage, y: yPercentage })

        // Update model viewer camera rotation based on mouse movement
        modelViewer.cameraTarget = '0m 0m 0m'
        modelViewer.cameraOrbit = `${xPercentage * 90}deg ${yPercentage * 90}deg 4m`
      }

      window.addEventListener('mousemove', handleMouseMove)

      return () => {
        window.removeEventListener('mousemove', handleMouseMove)
      }
    }
  }, [])

  return (
    <>
      <Navbar />
      <div className="container mx-auto px-4 pt-12 pb-20">
        <div className="relative">
          {/* 3D Model Container - Positioned in background */}
          <div className="absolute inset-0 z-0">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
            >
              <div className="model-viewer-container w-full max-w-4xl mx-auto aspect-video bg-transparent">
                <model-viewer
                  id="threedd"
                  ref={modelViewerRef}
                  src="images/homepage.glb"
                  camera-controls
                  auto-rotate
                  rotation-per-second="30deg"
                  shadow-intensity="1"
                  shadow-softness="0.7"
                  exposure="1.2"
                  environment-image="neutral"
                  camera-orbit="0deg 75deg 4m"
                  min-camera-orbit="auto auto auto"
                  max-camera-orbit="auto auto 50m"
                  class="w-full h-full"
                  ar-status="not-presenting"
                  interpolation-decay="200"
                ></model-viewer>
              </div>
            </motion.div>
          </div>

          {/* Content Overlay - Positioned in foreground */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="relative z-10 flex flex-col items-center text-center"
            style={{
              transform: `perspective(1000px) translateX(${mousePosition.x * 20}px) translateY(${mousePosition.y * 20}px)`
            }}
          >
            <h1 className="text-7xl font-serif text-white mb-16 tracking-wide leading-tight">
              ONLINE LEARNING
              <br />
              PLATFORM
            </h1>

            {/* Spacer div to maintain layout */}
            <div className="h-[400px]" />

            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.6 }}
              className="relative"
            >
              <div className="w-20 h-20 bg-white rounded-full flex items-center justify-center shadow-lg mx-auto">
                <img
                  src="images/click.png"
                  alt="Interactive icon"
                  className="w-15 h-15"
                />
              </div>
            </motion.div>

            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.9 }}
              className="text-gray-300 text-lg max-w-3xl mx-auto leading-relaxed mt-16"
            >
              This platform delivers an enhanced learning experience for students through interactive 3D 
              elements, making complex concepts easier to understand. AI-powered features ensure 
              accessibility for students with disabilities, offering tools like an AI board, video summarization, 
              and AI-driven chatbots. It also includes a comprehensive learning platform where instructors 
              can easily post and share their courses.
            </motion.p>
          </motion.div>
          <br />
          <br />
          <AboutUs />
          <br></br>
          <br></br>
          <Features />
          <br></br>
          <br></br>
          <Hallmark />
          <br></br>
          <br></br>
          <Solid />
          <br></br>
          <br></br>
          <Contact />

        </div>
      </div>
    </>
    
  )
}

export default LandingPage