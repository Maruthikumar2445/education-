import React from 'react';
import { motion } from 'framer-motion';
import { Phone, Mail, Linkedin, Facebook, Instagram } from 'lucide-react';

const ContactItem = ({ icon: Icon, title, content, delay }) => (
  <motion.div
    initial={{ opacity: 0, x: 50 }}
    whileInView={{ opacity: 1, x: 0 }}
    transition={{ 
      duration: 0.6, 
      delay,
      ease: [0.25, 0.25, 0, 0.75]
    }}
    viewport={{ once: true }}
    className="flex flex-col space-y-1"
  >
    <span className="text-lg font-light text-white/90">
      {title}
    </span>
    <div className="flex items-center space-x-2 text-gray-300 hover:text-white transition-colors">
      {Icon && <Icon className="w-4 h-4" />}
      <span>{content}</span>
    </div>
  </motion.div>
);

const SocialIcon = ({ icon: Icon }) => (
  <motion.a
    href="#"
    whileHover={{ scale: 1.1 }}
    whileTap={{ scale: 0.95 }}
    className="p-2 rounded-full hover:bg-white/10 transition-colors"
  >
    <Icon className="w-6 h-6 text-white" />
  </motion.a>
);

const Contact = () => {
  return (
    <div className="min-h-screen bg-black relative overflow-hidden flex items-center px-4 py-16 md:px-8">
      {/* Enhanced Gradients */}
      <div 
        className="absolute top-0 right-0 w-1/2 h-1/2 blur-[100px] rounded-full"
        style={{
          background: 'radial-gradient(circle, rgba(74, 91, 137, 0.8) 0%, rgba(0, 0, 0, 0) 70%)'
        }}
      />
      <div 
        className="absolute bottom-0 left-0 w-1/2 h-1/2 blur-[100px] rounded-full"
        style={{
          background: 'radial-gradient(circle, rgba(179, 106, 0, 0.6) 0%, rgba(0, 0, 0, 0) 70%)'
        }}
      />
      
      {/* Additional ambient gradients for more depth */}
      <div 
        className="absolute top-1/4 right-1/4 w-1/3 h-1/3 blur-[50px] rounded-full opacity-100"
        style={{
          background: 'radial-gradient(circle, rgba(74, 91, 137, 1) 0%, rgba(0, 0, 0, 0) 60%)'
        }}
      />
      <div 
        className="absolute bottom-1/4 left-1/4 w-1/3 h-1/3 blur-[50px] rounded-full opacity-100"
        style={{
          background: 'radial-gradient(circle, rgba(179, 106, 0, 1) 0%, rgba(0, 0, 0, 0) 60%)'
        }}
      />
      
      <div className="max-w-7xl mx-auto w-full relative">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-12 md:gap-24">
          {/* Left side - Title */}
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="flex items-center"
          >
            <h1 className="text-5xl md:text-6xl lg:text-7xl font-light text-white">
              Contact
            </h1>
          </motion.div>

          {/* Right side - Contact Info */}
          <div className="space-y-8">
            <ContactItem
              icon={Phone}
              title="Phone"
              content="9182427236"
              delay={0.2}
            />

            <ContactItem
              icon={Mail}
              title="Email"
              content="99220040539@klu.ac.in"
              delay={0.3}
            />

            <ContactItem
              icon={Linkedin}
              title="linked-in"
              content="PAVITHRA"
              delay={0.4}
            />

            {/* Social Icons */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.5 }}
              viewport={{ once: true }}
            >
              <h3 className="text-lg font-light text-white/90 mb-4">
                Social
              </h3>
              <div className="flex items-center space-x-4">
                <SocialIcon icon={Facebook} />
                <SocialIcon icon={Instagram} />
                <SocialIcon icon={Linkedin} />
              </div>
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Contact;