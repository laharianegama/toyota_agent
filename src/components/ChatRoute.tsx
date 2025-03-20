// A component that renders the chat route
import MessageList from "../components/MessageList";
import ChatInput from "../components/ChatInput";
import { Message } from "../components/MessageItem";

// Props type for the chat route component
interface ChatRouteProps {
  messages: Message[];
  isLoading: boolean;
  messagesEndRef: React.RefObject<HTMLDivElement | null>;
  onSendMessage: (message: string) => void;
}

const ChatRoute = ({
  messages,
  isLoading,
  messagesEndRef,
  onSendMessage,
}: ChatRouteProps) => {
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
          <ChatInput onSendMessage={onSendMessage} isLoading={isLoading} />
        </div>
      </div>
    </>
  );
};

export default ChatRoute;
