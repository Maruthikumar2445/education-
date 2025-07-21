import React from 'react';
import { motion, useScroll, useTransform, useSpring, useInView } from 'framer-motion';

const FeatureCard = ({ id, title }) => {
  const ref = React.useRef(null);
  const isInView = useInView(ref, { once: true, margin: "-100px" });

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, x: -50 }}
      animate={isInView ? { opacity: 1, x: 0 } : { opacity: 0, x: -50 }}
      transition={{
        duration: 0.8,
        delay: parseInt(id) * 0.1,
        ease: [0.17, 0.55, 0.55, 1]
      }}
      className="relative group"
    >
      <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg blur opacity-25 group-hover:opacity-75 transition duration-500" />
      <motion.div
        whileHover={{ scale: 1.02 }}
        className="relative bg-[#2d2df7] rounded-lg p-6 flex items-center transform transition-all duration-300 hover:shadow-xl cursor-pointer"
      >
        {/* Feature Number with Gradient */}
        <div className="relative">
          <span className="absolute -inset-1 bg-gradient-to-r from-blue-400 to-purple-400 rounded-full blur opacity-25" />
          <span className="relative text-4xl md:text-5xl font-bold text-white mr-6 bg-clip-text text-transparent bg-gradient-to-r from-blue-200 to-purple-200">
            {id}
          </span>
        </div>

        {/* Feature Title with Line Animation */}
        <div className="flex-1">
          <h3 className="text-lg md:text-xl text-white font-sans tracking-wide">
            {title}
          </h3>
          <motion.div
            initial={{ scaleX: 0 }}
            animate={isInView ? { scaleX: 1 } : { scaleX: 0 }}
            transition={{ duration: 0.8, delay: parseInt(id) * 0.2 }}
            className="h-0.5 bg-gradient-to-r from-blue-400 to-purple-400 mt-2 origin-left"
          />
        </div>
      </motion.div>
    </motion.div>
  );
};

const Features = () => {
  const { scrollYProgress } = useScroll();
  const scaleProgress = useTransform(scrollYProgress, [0, 0.5], [0.8, 1]);
  const opacityProgress = useTransform(scrollYProgress, [0, 0.3], [0.3, 1]);
  const springProgress = useSpring(scrollYProgress, {
    stiffness: 100,
    damping: 30,
    restDelta: 0.001
  });

  const features = [
    { id: "01", title: "ONLINE LEARNING PLATFORM" },
    { id: "02", title: "HANDICAPPED EASE OF USE" },
    { id: "03", title: "AI ENHANCED" },
    { id: "04", title: "3D REAL TIME LEARNING" }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 py-16 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
      {/* Background Animation */}
      <motion.div
        style={{
          scale: scaleProgress,
          opacity: opacityProgress
        }}
        className="absolute inset-0 bg-gradient-to-r from-blue-500/10 to-purple-500/10 blur-3xl"
      />

      {/* Progress Bar */}
      <motion.div
        style={{ scaleX: springProgress }}
        className="fixed top-0 left-0 right-0 h-1 bg-gradient-to-r from-blue-500 to-purple-500 transform origin-left z-50"
      />

      <div className="max-w-3xl mx-auto relative">
        {/* Title with Gradient */}
        <motion.h1
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-4xl md:text-5xl font-serif text-center mb-16 bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-400"
        >
          FEATURES
        </motion.h1>

        {/* Features Container */}
        <div className="space-y-6">
          {features.map((feature) => (
            <FeatureCard
              key={feature.id}
              id={feature.id}
              title={feature.title}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default Features;