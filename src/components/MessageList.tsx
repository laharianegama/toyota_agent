import React, { RefObject } from "react";
import MessageItem, { Message } from "./MessageItem";
import TypingIndicator from "./TypingIndicator";

export interface MessageListProps {
  messages: Message[];
  isLoading: boolean;
  messagesEndRef: RefObject<HTMLDivElement | null>;
}

const MessageList: React.FC<MessageListProps> = ({
  messages,
  isLoading,
  messagesEndRef,
}) => {
  return (
    <div className="flex flex-col space-y-2">
      {messages.length === 0 ? (
        <div className="text-center text-gray-500 my-8">
          <p>Start a conversation with Toyota Assistant</p>
        </div>
      ) : (
        <>
          {messages.map((message) => (
            <MessageItem key={message.id} message={message} />
          ))}
        </>
      )}

      {isLoading && (
        <div className="text-left">
          <TypingIndicator />
        </div>
      )}

      <div ref={messagesEndRef} />
    </div>
  );
};

export default MessageList;
