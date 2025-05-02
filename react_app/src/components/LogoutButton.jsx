import {useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { logout } from "../utils/auth";

export default function LogoutButton() {
    const navigate = useNavigate();

    useEffect(() => {
        logout();            // 토큰 제거
        navigate("/login");  // 로그인 페이지로 이동
    }, [navigate]);

    return null;
}

