import { useState, useEffect } from "react";
import { Outlet, useNavigation } from "react-router-dom";
import { NavLink } from "react-router-dom";

function App() {
  const navigation = useNavigation();

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      <header className="bg-blue-50 text-black p-4 shadow-md">
        <div className="max-w-3xl mx-auto flex items-center justify-between">
          <h1 className="text-xl font-bold">Toyota Assistant</h1>
          <nav className="flex space-x-4">
            <NavLink
              to="/"
              className={({ isActive }) => `hover:underline
                ${isActive ? "text-blue-500 font-bold" : "text-gray-500"}`}
            >
              Chat
            </NavLink>
            <NavLink
              to="/home"
              className={({ isActive }) => `hover:underline
                ${isActive ? "text-blue-500 font-bold" : "text-gray-500"}`}
            >
              Home
            </NavLink>
            <NavLink
              to="/contact"
              className={({ isActive }) => `hover:underline
                ${isActive ? "text-blue-500 font-bold" : "text-gray-500"}`}
            >
              Contact Us
            </NavLink>
          </nav>
        </div>
      </header>

      {/* Show loading state when navigating */}
      {navigation.state === "loading" && (
        <div className="loading-indicator">Loading...</div>
      )}

      {/* Render child routes */}
      <Outlet />
    </div>
  );
}

export default App;