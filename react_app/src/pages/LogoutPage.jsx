import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";

const LogoutPage = () => {
    const navigate = useNavigate();

    useEffect(() => {
        // 로컬 스토리지에서 토큰 제거
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");

        // 로그아웃 후 로그인 페이지로 리다이렉트
        navigate("/login");
    }, [navigate]);

    return (
        <div>
            <h2>로그아웃 중...</h2>
        </div>
    );
};

export default LogoutPage;