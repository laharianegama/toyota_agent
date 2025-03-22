import { useLoaderData } from 'react-router-dom';
import MessageList from "./MessageList";
import ChatInput from "./ChatInput";
import { ChatProvider, useChat } from '../features/chat/ChatContext';

interface LoaderData {
  threadId: string;
}

function ChatContent() {
  const { messages, isLoading, messagesEndRef, handleSendMessage } = useChat();

  return (
    <>
      <div className="flex-1 overflow-y-auto p-4">
        <div className="max-w-3xl mx-auto">
          <MessageList
            messages={messages}
            isLoading={isLoading}
            messagesEndRef={messagesEndRef}
          />
        </div>
      </div>

      <div className="p-4 border-t bg-white shadow-md">
        <div className="max-w-3xl mx-auto">
          <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
        </div>
      </div>
    </>
  );
}

function ChatRoute() {
  const { threadId } = useLoaderData() as LoaderData;

  return (
    <ChatProvider threadId={threadId}>
      <ChatContent />
    </ChatProvider>
  );
}

export default ChatRoute;
