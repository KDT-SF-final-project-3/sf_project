import React from "react";
import { useNavigate } from "react-router-dom";

const MainPage = () => {
    const navigate = useNavigate();
    return (
        <div>
            <h1>메인 페이지</h1>
            <p>여기는 로그인한 사용자만 접근할 수 있어요.</p>
            <button onClick={() => navigate("/logout")}>로그아웃</button>
        </div>
    );
};

export default MainPage;