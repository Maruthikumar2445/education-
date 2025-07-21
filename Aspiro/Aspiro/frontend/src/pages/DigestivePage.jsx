import React from 'react';
import { useState, useEffect } from 'react';

const DigestivePage = () => {
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
        
        <h1 className="text-white font-bold text-4xl">DIGESTIVE SYSTEM</h1>
        <span className="text-yellow-500 text-2xl font-semibold">ASPIRO</span>
        </div>
        <div className="flex justify-center mb-6">
          <model-viewer
            id="threedd"
            src="images/digestive1.glb"
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
        The human digestive system is a complex series of organs that work together to break down food, absorb nutrients, and eliminate waste. It begins in the mouth, where food is chewed and mixed with saliva, then moves down the esophagus to the stomach for further breakdown by stomach acids. The partially digested food then travels to the small intestine, where most nutrients are absorbed into the bloodstream. Finally, waste moves into the large intestine, where water is absorbed before elimination from the body.
        </p>
      </div>
    </div>
  );
};

export default DigestivePage;