import React from "react";
import { useNavigate } from "react-router-dom";
import { logout } from "../utils/auth";

export default function LogoutButton() {
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();  // 토큰 제거
        navigate("/login");  // 로그인 페이지로 리다이렉트
    };

    return (
        <button onClick={handleLogout}>로그아웃</button>
    );
}

