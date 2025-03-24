import React, { useState, KeyboardEvent } from "react";

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  isLoading: boolean;
}

const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage, isLoading }) => {
  const [message, setMessage] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim() === "" || isLoading) return;

    onSendMessage(message);
    setMessage("");
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex space-x-2">
      <textarea
        className="flex-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-toyota-red resize-none"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Type your message..."
        rows={1}
        disabled={isLoading}
      />
      <button
        type="submit"
        className="bg-toyota-red hover:bg-toyota-darkred text-white px-4 py-2 rounded-md transition-colors disabled:opacity-50"
        disabled={isLoading || message.trim() === ""}
      >
        Send
      </button>
    </form>
  );
};

export default ChatInput;
