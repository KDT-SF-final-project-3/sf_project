// src/pages/LoginPage.jsx
import React, { useState, useEffect } from "react";
import { Input, Button, message } from "antd";
import { UserOutlined, LockOutlined, EyeTwoTone, EyeInvisibleOutlined } from '@ant-design/icons';
import { useNavigate } from "react-router-dom";
import styled from "styled-components";
import axios from "axios";

export default function LoginPage() {
  const [formData, setFormData] = useState({ userID: "", password: "" });
  const [messageApi, contextHolder] = message.useMessage();
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (token) {
      const decoded = JSON.parse(atob(token.split('.')[1]));
      if (decoded.exp > Math.floor(Date.now() / 1000)) {
        navigate("/");
      }
    }
  }, [navigate]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post("http://127.0.0.1:8000/api/accounts/login/", formData);
      const { message, name, userID, is_approved } = res.data; // 백엔드 응답에 맞춰 변경
      // const { access, refresh, is_approved, name, userID } = res.data; // 기존 JWT 관련 코드 주석 처리

      // JWT 토큰 관련 localStorage 저장 부분 제거
      // localStorage.setItem("access_token", access);
      // localStorage.setItem("refresh_token", refresh);
      
      if (!is_approved) {
        return messageApi.error("승인되지 않은 계정입니다.");
      }

      localStorage.setItem("isLoggedIn", "true");
      localStorage.setItem("name", name);
      localStorage.setItem("userID", userID);

      messageApi.success(message || "로그인 성공!"); // 백엔드 메시지 사용 또는 기본 메시지
      setTimeout(() => navigate("/"), 1000);
    } catch (err) {
      messageApi.error(err.response?.data?.error || "로그인 실패! 😢");
    }
  };

  return (
    <MainDiv>
      {contextHolder}
      <FormBox>
        <Title>Login</Title>
        <StyledForm onSubmit={handleSubmit}>
          <Input name="userID" placeholder="아이디" prefix={<UserOutlined />} value={formData.userID} onChange={handleChange} />
          <Input.Password name="password" placeholder="비밀번호" prefix={<LockOutlined />} iconRender={visible => visible ? <EyeTwoTone /> : <EyeInvisibleOutlined />} value={formData.password} onChange={handleChange} />
          <Button type="primary" htmlType="submit">로그인</Button>
        </StyledForm>
        <p>계정이 없으신가요?</p>
        <Button onClick={() => navigate("/register")}>회원가입</Button>
      </FormBox>
    </MainDiv>
  );
}

const MainDiv = styled.div`
  display: flex; justify-content: center; align-items: center;
  height: 100vh; background-color: #f0f0f0;
`;

const FormBox = styled.div`
  background: white; padding: 40px; border-radius: 10px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1); width: 400px;
  display: flex; flex-direction: column; align-items: center; gap: 10px;
`;

const Title = styled.h2` font-size: 32px; color: #333; `;

const StyledForm = styled.form`
  display: flex; flex-direction: column; width: 100%; gap: 10px;
  input, button { height: 48px; font-size: 16px; }
`;