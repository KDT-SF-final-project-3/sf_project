// src/pages/MainPage.jsx
import React from "react";
import WebcamViewer from "../components/WebcamViewer";  // ✅ 정확히 가져오기

const MainPage = () => {
  return (
    <div>
      <h1>메인 페이지</h1>
      <WebcamViewer /> {/* ✅ 웹캠 컴포넌트 사용 */}
    </div>
  );
};

export default MainPage;