import React from "react";

const TypingIndicator: React.FC = () => {
  return (
    <div className="flex items-center space-x-1 py-2 px-4 my-2 inline-block bg-gray-200 rounded-lg rounded-bl-none text-gray-800">
      <div className="w-2 h-2 bg-gray-500 rounded-full animate-pulse"></div>
      <div
        className="w-2 h-2 bg-gray-500 rounded-full animate-pulse"
        style={{ animationDelay: "0.2s" }}
      ></div>
      <div
        className="w-2 h-2 bg-gray-500 rounded-full animate-pulse"
        style={{ animationDelay: "0.4s" }}
      ></div>
    </div>
  );
};

export default TypingIndicator;
