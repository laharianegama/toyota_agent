import React from "react";

export interface Message {
  id: string;
  content: string;
  sender: "user" | "assistant";
  timestamp: Date;
  isError?: boolean;
}

interface MessageItemProps {
  message: Message;
}

const MessageItem: React.FC<MessageItemProps> = ({ message }) => {
  const isUser = message.sender === "user";

  return (
    <div className={`my-3 ${isUser ? "text-right" : "text-left"}`}>
      <div
        className={`inline-block max-w-[80%] px-4 py-2 rounded-lg ${
          isUser
            ? "bg-blue-100 text-black rounded-bl-none"
            : message.isError
            ? "bg-red-100 text-red-800 rounded-bl-none"
            : "bg-gray-200 text-gray-800 rounded-bl-none"
        }`}
      >
        {message.content}
      </div>
      <div className="text-xs text-gray-500 mt-1 px-1">
        {new Date(message.timestamp).toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        })}
      </div>
    </div>
  );
};

export default MessageItem;
