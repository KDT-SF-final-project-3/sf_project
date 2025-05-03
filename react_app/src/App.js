// src/App.js

import "./App.css";
import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate, Link } from "react-router-dom";

import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import WebcamPage from "./pages/WebcamPage";
import ControlPanel from "./components/ControlPanel";
import DataMonitor from "./pages/DataMonitor";

function App() {
  return (
    <Router>
      <div>
        {/* ✅ 상단 네비게이션 */}
        <nav style={{ padding: "10px", borderBottom: "1px solid #ccc", marginBottom: "20px" }}>
          <Link to="/monitor" style={{ marginRight: "10px" }}>📊 데이터</Link>
          <Link to="/dddd" style={{ marginRight: "10px" }}>🏠 제어</Link>
          <Link to="/webcam" style={{ marginRight: "10px" }}>📷 웹캠</Link>
          <Link to="/login" style={{ marginRight: "10px" }}>🔑 로그인</Link>
        </nav>

        {/* ✅ 라우터 경로 */}
        <Routes>
          {/* ✅ 앱 실행 시 /monitor로 자동 이동 */}
          <Route path="/" element={<Navigate to="/monitor" />} />

          <Route path="/monitor" element={<DataMonitor />} />
          <Route path="/control" element={
            <div>
              <h1>로봇 제어 패널</h1>
              <ControlPanel />
            </div>
          } />
          <Route path="/webcam" element={<WebcamPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />

          {/* ✅ 존재하지 않는 경로 대응 */}
          <Route path="*" element={<div><h2>404 - 페이지를 찾을 수 없습니다</h2></div>} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;