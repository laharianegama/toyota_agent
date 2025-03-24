// src/components/Home.tsx
import React from "react";

const Home: React.FC = () => {
  return (
    <div className="max-w-3xl mx-auto p-8 w-full">
      <h1 className="text-3xl font-bold mb-6">Welcome to Toyota</h1>
      <p className="mb-4">
        Toyota is dedicated to providing the best vehicles and services to our
        customers.
      </p>
      <p>
        Explore our website to learn more about our latest models, book a test
        drive, or schedule a service appointment.
      </p>
    </div>
  );
};

export default Home;
