// src/pages/WebcamPage.jsx
import React from "react";
import WebcamViewer from "../components/WebcamViewer"; // ⭐ 컴포넌트 가져오기

const WebcamPage = () => {
  return (
    <div>
      <h2>웹캠 스트림 페이지</h2>
      <WebcamViewer /> {/* ⭐ 컴포넌트 사용 */}
    </div>
  );
};

export default WebcamPage;