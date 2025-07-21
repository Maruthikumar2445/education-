import React, { useEffect, useRef } from 'react';
import { motion, useAnimation } from 'framer-motion';

const AboutUs = () => {
  const controls = useAnimation();
  const sectionRef = useRef(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            controls.start('visible');
          } else {
            controls.start('hidden');
          }
        });
      },
      { threshold: 0.3 }
    );

    if (sectionRef.current) {
      observer.observe(sectionRef.current);
    }

    return () => {
      if (sectionRef.current) {
        observer.unobserve(sectionRef.current);
      }
    };
  }, [controls]);

  const testimonials = [
   
    {
      name: 'VIJAYA',
      avatar: 'images/aspiro-icon.png',
      testimonial:
        'CSE 3RD YEAR AIML MERN STACK DEVELOPER'
    },
    {
      name: 'ASPIRO',
      avatar: 'images/aspiro-icon.png',
      testimonial:
        'EDU PLATFORM'
    },
    {
      name: 'AGRI',
      avatar: 'images/agri-logo.png',
      testimonial:
        'AGRICULTURE PLATFORM'
    },
    // {
    //   name: 'Jonah',
    //   avatar: 'https://via.placeholder.com/80',
    //   testimonial:
    //     'Testimonials are short quotes from people who love your brand. It\'s a great way to convince customers to try your services.'
    // }
  ];

  return (
    <div
      className="py-20 bg-[#0e0e0e] text-white"
      ref={sectionRef}
    >
      <motion.h2
        className="text-4xl font-bold text-center mb-12"
        initial={{ opacity: 0, y: 50 }}
        animate={controls}
        variants={{
          visible: { opacity: 1, y: 0, transition: { duration: 0.6 } },
          hidden: { opacity: 0, y: 50 }
        }}
      >
        About Us
      </motion.h2>
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-8 px-4 sm:px-5">
        {testimonials.map((testimonial, index) => (
          <motion.div
            key={index}
            className="bg-[rgba(255,255,255,0.1)] rounded-lg shadow-[0_8px_16px_rgba(0,0,0,0.3)] transform transition-transform duration-300 hover:scale-105"
            initial={{ opacity: 0, y: 50 }}
            animate={controls}
            variants={{
              visible: {
                opacity: 1,
                y: 0,
                transition: { duration: 0.6, delay: index * 0.2 }
              },
              hidden: { opacity: 0, y: 50 }
            }}
          >
            <div className="flex flex-col items-center p-8">
              <img
                src={testimonial.avatar}
                alt={testimonial.name}
                className="rounded-full w-20 h-20 shadow-md"
              />
              <h3 className="text-lg font-bold mt-4">{testimonial.name}</h3>
              <p className="text-sm mt-2">{testimonial.testimonial}</p>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default AboutUs;