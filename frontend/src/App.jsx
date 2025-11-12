// App.jsx
import React from "react";
import MobileForm from "./components/MobileForm";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

function App() {
  return (
    <div className="min-h-screen bg-black flex items-center justify-center">
      <MobileForm />
      <ToastContainer position="top-center" />
    </div>
  );
}

export default App;
