// src/routes/index.tsx
import { RouteObject } from "react-router-dom";
import Home from "../components/Home";
import ContactUs from "../components/ContactUs";

// Move your chat interface to a separate component
const Chat = () => {
  // This component will contain all your existing chat functionality
  // For now, just leave it as a placeholder and we'll update it later
  return <div>Chat Component</div>;
};

export const routes: RouteObject[] = [
  {
    path: "/",
    element: <Chat />,
  },
  {
    path: "/home",
    element: <Home />,
  },
  {
    path: "/contact",
    element: <ContactUs />,
  },
];
