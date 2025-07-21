import React from 'react';
import { Link } from 'react-router-dom';

const ResourceCard = ({ title, description, icon, to }) => (
  <Link to={to} className="block">
    <div className="bg-[#2d2a5a] rounded-xl border border-white/30 p-6 flex flex-col items-center transition-all hover:shadow-xl hover:border-white hover:scale-105">
      <div className="w-32 h-32 mb-4 flex items-center justify-center rounded-full bg-[#3c38a6]">
        {icon}
      </div>
      <h3 className="text-xl font-semibold text-white mb-2">{title}</h3>
      <p className="text-[#c2c2c2] text-sm text-center">{description}</p>
    </div>
  </Link>
);

const LearningResources = () => {
  const resources = [
    {
      title: "Plant",
      description: "A 3D plant explore plant anatomy interactively",
      icon: (
        <model-viewer id="threedd" src="images/plant1.glb" autoplay camera-controls shadow-intensity="1"></model-viewer>
      ),
      to: "/plant"
    },
    {
      title: "Heart",
      description: "A 3D heart model allows users to explore heart anatomy interactively",
      icon: (
        <model-viewer id="threedd" src="images/heart.glb" autoplay camera-controls shadow-intensity="1"></model-viewer>
      ),
      to: "/heart"
    },
    {
      title: "Digestive System",
      description: "A 3D digestive system model allows users to explore digestive anatomy interactively",
      icon: (
        <model-viewer id="threedd" src="images/digestive1.glb" autoplay camera-controls shadow-intensity="1"></model-viewer>
      ),
      to: "/digestive"
    },
    {
      title: "Micro Scope",
      description: "A 3D microscope model allows users to explore microscope anatomy interactively",
      icon: (
        <model-viewer id="threedd" src="images/micro.glb" autoplay camera-controls shadow-intensity="1"></model-viewer>
      ),
      to: "/micro"
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-[#1a1f71] to-[#2d3b9d]">
      <div className="container mx-auto px-4 py-8">
        {/* Navbar */}
        <nav className="flex items-center mb-12">
          <img src="images/aspiro-icon.png" alt="Aspiro Logo" className="h-8" />
          <span className="text-white text-2xl font-semibold">ASPIRO</span>
        </nav>

        {/* Header */}
        <h1 className="text-3xl font-bold text-white mb-12 tracking-wider">
          LEARNING RESOURCES
        </h1>

        {/* Grid of cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          {resources.map((resource, index) => (
            <ResourceCard
              key={index}
              title={resource.title}
              description={resource.description}
              icon={resource.icon}
              to={resource.to}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default LearningResources;