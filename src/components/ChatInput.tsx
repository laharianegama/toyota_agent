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
    <form onSubmit={handleSubmit} className="gap-2 flex items-center">
      <textarea
        className="bg-blue-100 flex-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-toyota-red resize-none"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Type your message..."
        rows={1}
        disabled={isLoading}
      />
      <button
        type="submit"
        className="bg-green-500 hover:bg-green-600 text-grey px-4 py-2 rounded-md transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed active:scale-95 focus:ring-2 focus:ring-green-400"
        disabled={isLoading || message.trim() === ""}
      >
        Send
      </button>
    </form>
  );
};

export default ChatInput;
