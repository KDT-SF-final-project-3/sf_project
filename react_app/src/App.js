import "./App.css";
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import WebcamPage from "./pages/WebcamPage";
import ControlPanel from "./components/ControlPanel"; // ✅ 직접 import

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={
          <div>
            <h1>로봇 제어 패널</h1>
            <ControlPanel />
          </div>
        } />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/webcam" element={<WebcamPage />} />
      </Routes>
    </Router>
  );
}

export default App;