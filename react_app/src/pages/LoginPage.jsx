import React, { useState } from "react";
import axios from "axios";
import {Input, Button, message} from 'antd';
import { UserOutlined, LockOutlined, EyeTwoTone, EyeInvisibleOutlined } from '@ant-design/icons';
import { useNavigate } from "react-router-dom";
import styled from "styled-components";

export default function LoginPage () {
    const [formData, setFormData] = useState({
        userID: "",
        password: "",
    });
    const [messageApi, contextHolder] = message.useMessage();
    const navigate = useNavigate();  // 로그인 성공 시 페이지 이동을 위한 navigate

    // 로그인 상태 체크 (페이지 로드 시 추가)
    React.useEffect(() => {
        const token = localStorage.getItem("access_token");
        if (token) {
            // 토큰이 있으면 만료 여부 체크
            const isTokenExpired = checkTokenExpiration(token);
            if (!isTokenExpired) {
                navigate("/"); // 이미 로그인 된 경우, 메인 페이지로 리다이렉트
            }
        }
    }, [navigate]); // navigate는 의존성 배열에 포함

    // 토큰 만료 여부를 확인하는 함수 추가
    const checkTokenExpiration = (token) => {
        const decodedToken = JSON.parse(atob(token.split('.')[1])); // JWT의 payload를 디코드
        const currentTime = Math.floor(Date.now() / 1000); // 현재 시간 (초 단위)
        return decodedToken.exp < currentTime; // 만약 토큰의 만료시간이 현재 시간보다 작으면 만료된 것
    };


    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            // 로그인 API 요청 보내기
            const res = await axios.post("http://127.0.0.1:8000/api/login/", formData);
            const { access_token, refresh_token, is_approved, name } = res.data;

            if (is_approved) {
                // 서버로부터 받은 JWT 토큰을 로컬 스토리지에 저장
                localStorage.setItem("access_token", access_token);
                localStorage.setItem("refresh_token", refresh_token);
                localStorage.setItem("name", name);

                messageApi.success("로그인 성공! 🎉");
                setTimeout(() => {
                    navigate("/");  // 메인 페이지로 리다이렉트
                }, 1500);
            } else {
                messageApi.error("승인되지 않은 계정입니다. 관리자에게 문의하세요.");
            }
    
        } catch (error) {
            console.error("로그인 실패:", error.response.data);
            messageApi.error("로그인 실패! 😢 아이디 또는 비밀번호를 확인해주세요.");
        }
    };

    const goToRegister = () => {
        navigate("/register");  // 회원가입 페이지로 리다이렉트
    };


    return (
        <MainDiv>
            {contextHolder}
            <FormBox>
                <Title>Hello, world!</Title>
                <StyledForm onSubmit={handleSubmit}>
                    <Input name="userID" type="text" placeholder="아이디"
                        prefix={<UserOutlined />} onChange={handleChange}
                        value={formData.userID}
                    />
                    <Input.Password name="password" placeholder="비밀번호" 
                        prefix={<LockOutlined />} iconRender={visible => (visible ? <EyeTwoTone /> : <EyeInvisibleOutlined />)} 
                        onChange={handleChange} value={formData.password}
                    />
                    <Button htmlType="submit" type="primary" size="large">로그인</Button>
                </StyledForm>
                <br></br>
                <h4>계정이 없으신가요?</h4>
                <Button onClick={goToRegister}>회원가입</Button>
            </FormBox>
        </MainDiv>
    );
};

// 전체 배경 (배경 바깥쪽)
export const MainDiv = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f0f0f0;  /* 배경색: 연한 회색 (예시) */
`;

// 회원가입 박스 (안쪽 박스)
const FormBox = styled.div`
  background-color: white;   /* 폼 내부 색: 흰색 */
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);  /* 그림자 */
  width: 400px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
`;

// 제목 스타일
const Title = styled.h2`
  font-size: 32px;
  color: #333;
  margin-bottom: 20px;
`;

// 폼 스타일
const StyledForm = styled.form`
  display: flex;
  flex-direction: column;
  width: 100%;
  gap: 10px;

  input, button {
    border-radius: 8px;
    padding: 10px;

    height: 48px;
    line-height: 48px;

    font-size: 17px;
  }

  input {
    border: 1px solid #ccc;     /* 기본 테두리 색 */
    outline: none; 
  }
`;