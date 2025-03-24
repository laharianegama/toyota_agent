import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import "./index.css";
import App from "./App.tsx";
import ErrorPage from './routes/ErrorPage.tsx'
import ChatRoute from "./components/ChatRoute.tsx";
import Home from './components/Home.tsx'
import ContactUs from "./components/ContactUs.tsx";

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    errorElement: <ErrorPage />,
    children: [
      {
        path: "",
        element: <ChatRoute />,
        loader: async () => {
          const savedThreadId = localStorage.getItem("threadId") || crypto.randomUUID();
          localStorage.setItem("threadId", savedThreadId);
          return { threadId: savedThreadId };
        },
      },
      {
        path: "home",
        element: <Home />,
      },
      {
        path: "contact",
        element: <ContactUs />,
      },
    ],
  },
]);

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>
);