import React from 'react';
import { useState, useEffect } from 'react';

const PlantPage = () => {
  const [modelLoaded, setModelLoaded] = useState(false);

  useEffect(() => {
    const modelViewer = document.getElementById('threedd');

    if (modelViewer) {
      modelViewer.addEventListener('load', () => {
        setModelLoaded(true);
      });
    }
  }, []);

  return (
    <div className="flex justify-center items-center min-h-screen bg-gradient-to-r from-[#000020] to-[#2323A6]">
      <div className="bg-gradient-to-r from-[#1A1A3B] to-[#3B3BA3] rounded-lg shadow-lg border border-[#E0E0E0] p-8 w-full max-w-3xl">
        <div className="flex justify-between items-center mb-6">
        <img src="images/aspiro-icon.png" alt="Aspiro Logo" className="h-8" />
        
          <h1 className="text-white font-bold text-4xl">PLANT</h1>
          <span className="text-yellow-500 text-2xl font-semibold">ASPIRO</span>
        </div>
        <div className="flex justify-center mb-6">
          <model-viewer
            id="threedd"
            src="images/plant1.glb"
            auto-rotate
            rotation-per-second="30deg"
            camera-controls
            shadow-intensity="1"
            class="w-full h-[400px] rounded-md shadow-md"
          >
            {!modelLoaded && (
              <div className="absolute inset-0 flex justify-center items-center">
                <div className="text-white text-xl font-bold">Loading 3D Model...</div>
              </div>
            )}
          </model-viewer>
        </div>
        <p className="text-[#D0D0D0] text-center leading-relaxed">
          Plants have several key parts: roots, which anchor the plant and absorb water and nutrients from the soil; stems, which support the plant and transport water, nutrients, and food; leaves, where photosynthesis occurs to produce energy; flowers, which are involved in reproduction; and fruits, which contain seeds for new plant growth.
        </p>
      </div>
    </div>
  );
};

export default PlantPage;