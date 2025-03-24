import React from "react";
import { motion } from "framer-motion";

const TypingIndicator: React.FC = () => {
  return (
    <div className="inline-flex items-center space-x-2 py-2 px-4 bg-gray-200 rounded-lg">
      {[0, 0.2, 0.4].map((delay, index) => (
        <motion.div
          key={index}
          className="w-3 h-3 bg-gray-500 rounded-full"
          animate={{ y: [0, -5, 0] }}
          transition={{
            repeat: Infinity,
            duration: 0.6,
            ease: "easeInOut",
            delay,
          }}
        />
      ))}
    </div>
  );
};

export default TypingIndicator;
