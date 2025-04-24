import React from "react";
import { Navigate } from "react-router-dom";

// ProtectedRoute 컴포넌트는 인증된 사용자만 접근할 수 있는 페이지에 사용
const ProtectedRoute = ({ element }) => {
    const token = localStorage.getItem("access_token");

    // 인증된 사용자만 element를 렌더링하고, 그렇지 않으면 로그인 페이지로 리다이렉트
    return token ? element : <Navigate to="/login" replace />;
};

export default ProtectedRoute;