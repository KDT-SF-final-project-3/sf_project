import React from 'react';
import { Navigate } from 'react-router-dom';

const ProtectedRoute = ({ children }) => {
  const isLoggedIn = localStorage.getItem("isLoggedIn");

  if (isLoggedIn !== "true") {
    // 로그인 상태가 아니면 로그인 페이지로 리다이렉트
    return <Navigate to="/login" />;
  }

  return children;  // 로그인 상태일 경우 자식 컴포넌트 렌더링
};

export default ProtectedRoute;