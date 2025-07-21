import React from 'react';
import { motion } from 'framer-motion';
import { AppWindow, Apple, Play } from 'lucide-react';

const RotatingText = () => {
  const text = "COMING SOON ";
  const characters = text.split('');
  const radius = 50;
  
  return (
    <div className="relative w-40 h-40 animate-spin-slow">
      {characters.map((char, i) => {
        const angle = (i / characters.length) * 360;
        const radian = (angle * Math.PI) / 180;
        const x = radius * Math.cos(radian);
        const y = radius * Math.sin(radian);
        
        return (
          <div
            key={i}
            className="absolute left-1/2 top-1/2 text-white font-bold transform -translate-x-1/2 -translate-y-1/2"
            style={{
              transform: `translate(${x}px, ${y}px) rotate(${angle + 90}deg)`
            }}
          >
            {char}
          </div>
        );
      })}
    </div>
  );
};

const Button = ({ icon: Icon, children, className = "" }) => (
  <motion.button
    whileHover={{ scale: 1.05 }}
    whileTap={{ scale: 0.95 }}
    className={`
      px-6 py-3 border border-white/20 rounded-lg
      flex items-center justify-center gap-2
      text-white font-medium
      transition-all duration-300
      hover:border-white/40 hover:bg-white/5
      focus:outline-none focus:ring-2 focus:ring-white/20
      shadow-[0_0_15px_rgba(255,255,255,0.1)]
      ${className}
    `}
  >
    {Icon && <Icon className="w-5 h-5" />}
    {children}
  </motion.button>
);

const Solid = () => {
  return (
    <div className="min-h-screen bg-black flex flex-col items-center justify-center relative overflow-hidden px-4 py-16">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-radial from-purple-900/20 via-transparent to-transparent" />
      
      <div className="max-w-6xl mx-auto flex flex-col lg:flex-row items-center gap-12">
        <div className="flex-1 text-center lg:text-left">
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-4xl md:text-5xl lg:text-6xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-white to-white/80 mb-8"
          >
            Take the next step toward your personal and professional goals with Coursera.
          </motion.h1>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start"
          >
            <Button icon={AppWindow} className="bg-blue-600 hover:bg-blue-700 border-0">
              Let's start learning
            </Button>
            
            <div className="flex flex-col sm:flex-row gap-4">
              <Button icon={Apple}>
                Download on App Store
              </Button>
              
              <Button icon={Play}>
                Get it on Google Play
              </Button>
            </div>
          </motion.div>
        </div>

        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          whileInView={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8 }}
          className="relative"
        >
          <div className="absolute inset-0 bg-gradient-to-r from-blue-500/20 to-purple-500/20 blur-3xl" />
          <RotatingText />
        </motion.div>
      </div>

      {/* Glowing orbs in background */}
      <div className="absolute -top-40 -right-40 w-80 h-80 bg-purple-500/30 rounded-full blur-3xl" />
      <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-blue-500/30 rounded-full blur-3xl" />
    </div>
  );
};

export default Solid;