import { createContext, useContext, useState, useRef, useEffect } from 'react';
import { Message } from "../../components/MessageItem";
import * as api from "../../services/api";

interface ChatContextType {
  messages: Message[];
  isLoading: boolean;
  messagesEndRef: React.RefObject<HTMLDivElement | null>;
  handleSendMessage: (message: string) => Promise<void>;
}

const ChatContext = createContext<ChatContextType | null>(null);

export function ChatProvider({ children, threadId }: { children: React.ReactNode, threadId: string }) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isInitialized, setIsInitialized] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Load messages with storage event listener
  useEffect(() => {
    const loadMessages = () => {
      const savedMessages = localStorage.getItem(`messages-${threadId}`);
      if (savedMessages) {
        try {
          const parsedMessages = JSON.parse(savedMessages, (key, value) => {
            if (key === "timestamp") return new Date(value);
            return value;
          });
          setMessages(parsedMessages);
        } catch (e) {
          console.error("Error parsing saved messages:", e);
        }
      } else {
        setMessages([
          {
            id: "welcome",
            content: "Hello! I'm your Toyota Assistant. How can I help you today?",
            sender: "assistant",
            timestamp: new Date(),
          },
        ]);
      }
      setIsInitialized(true);
    };

    loadMessages();

    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === `messages-${threadId}`) {
        loadMessages();
      }
    };

    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, [threadId]);

  // Save messages
  useEffect(() => {
    if (!isInitialized) return;
    localStorage.setItem(`messages-${threadId}`, JSON.stringify(messages));
  }, [messages, threadId, isInitialized]);

  // Auto-scroll
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSendMessage = async (messageText: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      content: messageText,
      sender: "user",
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await api.sendMessage(messageText, threadId);
      
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: response.message,
        sender: "assistant",
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error("Error sending message:", error);
      
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: "Sorry, there was an error processing your request. Please try again.",
        sender: "assistant",
        isError: true,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <ChatContext.Provider value={{ messages, isLoading, messagesEndRef, handleSendMessage }}>
      {children}
    </ChatContext.Provider>
  );
}

export const useChat = () => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
};