import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import styled from "styled-components";

export default function RegisterForm () {
    const [formData, setFormData] = useState({
        emp_no: "",
        userID: "",
        password: "",
        name: "",
        email: "",
        position: "",
    });

    const [message, setMessage] = useState("");
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
    try {
        const res = await axios.post("http://127.0.0.1:8000/api/register/", formData);
        setMessage("✅ 회원가입 성공! 🎉");
        console.log("서버 응답:", res.data);

        // 회원가입 성공 후 로그인 페이지로 리다이렉트
        setTimeout(() => {
            navigate("/login");  // 로그인 페이지로 이동
        }, 2000);  // 2초 후 로그인 페이지로 이동 (2초 딜레이로 회원가입 성공 메시지를 볼 수 있도록)


    } catch (error) {
        console.error("회원가입 실패:", error.response.data);
        setMessage("❌ 회원가입 실패! 😢");
    }
    };

    return (
        <MainDiv>
            <FormBox>
                <Title>Sign Up</Title>
                <StyledForm onSubmit={handleSubmit}>
                    <input name="emp_no" placeholder="직번" onChange={handleChange} />
                    <input name="name" placeholder="이름" onChange={handleChange} />
                    <input name="userID" placeholder="아이디" onChange={handleChange} />
                    <input name="password" type="password" placeholder="비밀번호" onChange={handleChange} />
                    <input name="email" placeholder="이메일" onChange={handleChange} />
                    <input name="position" placeholder="직급" onChange={handleChange} />
                    <button type="submit">가입하기</button>
                </StyledForm>
            </FormBox>

            {message && <p>{message}</p>}
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
    padding: 10px;
    font-size: 16px;
  }

  button {
    background-color: #007bff;
    color: white;
    border: none;
    cursor: pointer;
  }
`;