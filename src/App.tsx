import { useState, useRef, useEffect } from "react";
import MessageList from "./components/MessageList";
import ChatInput from "./components/ChatInput";
import { Message } from "./components/MessageItem";
import * as api from "./services/api";

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [threadId] = useState(
    () => localStorage.getItem("threadId") || crypto.randomUUID()
  );
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Save thread ID
  useEffect(() => {
    localStorage.setItem("threadId", threadId);
  }, [threadId]);

  // Load saved messages
  useEffect(() => {
    const savedMessages = localStorage.getItem(`messages-${threadId}`);
    if (savedMessages) {
      try {
        // Parse dates when loading
        const parsedMessages = JSON.parse(savedMessages, (key, value) => {
          if (key === "timestamp") return new Date(value);
          return value;
        });
        setMessages(parsedMessages);
      } catch (e) {
        console.error("Error parsing saved messages:", e);
      }
    } else {
      // Add welcome message for new conversations
      setMessages([
        {
          id: "welcome",
          content:
            "Hello! I'm your Toyota Assistant. I can help with vehicle availability, service appointments, and test drives. How can I assist you today?",
          sender: "assistant",
          timestamp: new Date(),
        },
      ]);
    }
  }, [threadId]);

  // Save messages
  useEffect(() => {
    localStorage.setItem(`messages-${threadId}`, JSON.stringify(messages));
  }, [messages, threadId]);

  //   The useEffect hook detects the change in the messages dependency array
  // Inside useEffect, React finds the empty div using messagesEndRef.current
  // It calls scrollIntoView() on that div, telling the browser to scroll to it.

  // Auto-scroll
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSendMessage = async (messageText: string) => {
    // Add user message to history
    const userMessage: Message = {
      id: Date.now().toString(),
      content: messageText,
      sender: "user",
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      // Send to backend
      const response = await api.sendMessage(messageText, threadId);

      // Add assistant response to history
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: response.message,
        sender: "assistant",
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error("Error sending message:", error);

      // Add error message
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content:
          "Sorry, there was an error processing your request. Please try again.",
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
    <div className="flex flex-col h-screen bg-gray-100">
      <header className="bg-green-50 text-black p-6 shadow-md">
        <div className="max-w-3xl mx-auto flex items-center">
          <h1 className="text-xl font-bold">Toyota Assistant</h1>
        </div>
      </header>

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
    </div>
  );
}

export default App;
