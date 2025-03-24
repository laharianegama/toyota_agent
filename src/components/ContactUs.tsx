// src/components/Contact-us.tsx
import React from "react";

const ContactUs: React.FC = () => {
  return (
    <div className="max-w-3xl mx-auto p-8 w-full">
      <h1 className="text-3xl font-bold mb-6">Contact Us</h1>
      <p className="mb-4">
        We're here to help with any questions about Toyota vehicles or services.
      </p>
      <div className="mt-6">
        <h2 className="text-xl font-semibold mb-3">Toyota Support</h2>
        <p>Email: support@toyota.com</p>
        <p>Phone: (555) 123-4567</p>
        <p>Hours: Monday-Friday, 8am-6pm</p>
      </div>
    </div>
  );
};

export default ContactUs;
