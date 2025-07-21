import React from 'react';
import { Shield, Settings2, UserCircle2 } from 'lucide-react';
import { motion } from 'framer-motion';

const FeatureCard = ({ icon: Icon, title, description, delay }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    whileInView={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.5, delay }}
    viewport={{ once: true }}
    className="p-6 rounded-xl bg-white/5 backdrop-blur-lg hover:bg-white/10 transition-all duration-300 hover:scale-[1.02] cursor-pointer border border-white/10"
  >
    <div className="flex items-start space-x-4">
      <div className="p-2 rounded-lg bg-white/5">
        <Icon className="w-6 h-6 text-gray-300" />
      </div>
      <div className="flex-1">
        <h3 className="text-lg font-semibold text-gray-200 mb-2">{title}</h3>
        <p className="text-gray-400 text-sm">{description}</p>
      </div>
    </div>
  </motion.div>
);

const Hallmark = () => {
  const features = [
    {
      icon: UserCircle2,
      title: "User-friendly",
      description: "Write here a key feature of the app or software that is being advertised here.",
      delay: 0
    },
    {
      icon: Settings2,
      title: "Seamless integration",
      description: "Write here a key feature of the app or software that is being advertised here.",
      delay: 0.2
    },
    {
      icon: Shield,
      title: "Secure & safe",
      description: "Write here a key feature of the app or software that is being advertised here.",
      delay: 0.4
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-blue-950 relative overflow-hidden">
      {/* Radial gradient overlay */}
      <div className="absolute top-0 right-0 w-1/2 h-full bg-blue-900/20 blur-[10px] rounded-full" />
      
      <div className="relative container mx-auto px-4 py-16">
        {/* Header */}
        <motion.h1 
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6 }}
          className="text-5xl font-light text-white mb-16"
        >
          Hallmark
        </motion.h1>

        {/* Features Container */}
        <div className="max-w-2xl mx-auto space-y-6">
          {features.map((feature, index) => (
            <FeatureCard
              key={index}
              icon={feature.icon}
              title={feature.title}
              description={feature.description}
              delay={feature.delay}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default Hallmark;