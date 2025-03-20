import { Route, Routes } from "react-router-dom";
import Home from "../components/Home";
import ContactUs from "../components/ContactUs";
import ChatRoute from "../components/ChatRoute";
import { Message } from "../components/MessageItem";
import { MessageListProps } from "../components/MessageList";

// The main AppRoutes component that contains all routes
interface AppRoutesProps {
  messages: Message[];
  isLoading: boolean;
  messagesEndRef: React.RefObject<HTMLDivElement | null>;
  onSendMessage: (message: string) => void; // Adjust the function signature as needed
}

const AppRoutes: React.FC<AppRoutesProps> = ({
  messages,
  isLoading,
  messagesEndRef,
  onSendMessage,
}) => {
  return (
    <Routes>
      <Route
        path="/"
        element={
          <ChatRoute
            messages={messages}
            isLoading={isLoading}
            messagesEndRef={messagesEndRef}
            onSendMessage={onSendMessage}
          />
        }
      />
      <Route path="/home" element={<Home />} />
      <Route path="/contact" element={<ContactUs />} />
    </Routes>
  );
};

export default AppRoutes;
