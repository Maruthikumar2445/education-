import React from 'react';
import { useState, useEffect } from 'react';

const HeartPage = () => {
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
        
        <h1 className="text-white font-bold text-4xl">HERT</h1>
        <span className="text-yellow-500 text-2xl font-semibold">ASPIRO</span>
        </div>
        <div className="flex justify-center mb-6">
          <model-viewer
            id="threedd"
            src="images/heart.glb"
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
        The human heart is a muscular organ about the size of a fist, responsible for pumping blood throughout the body. It has four chambers—two atria and two ventricles—that work together to circulate oxygen-rich blood to organs and tissues and return oxygen-poor blood to the lungs for oxygenation. The heart operates through a rhythmic cycle, contracting and relaxing to maintain a steady flow of blood, which is essential for delivering nutrients and removing waste products. Its function is regulated by electrical impulses, which coordinate the heartbeat and ensure efficient circulation.
        </p>
      </div>
    </div>
  );
};

export default HeartPage;