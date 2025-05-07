import React, { useState } from "react";
import axios from "axios";
import { EyeInvisibleOutlined, EyeTwoTone } from '@ant-design/icons';
import {Input, Button, message} from 'antd';
import { useNavigate } from "react-router-dom";
import styled from "styled-components";

export default function RegisterForm() {
  const [formData, setFormData] = useState({
      emp_no: "",
      userID: "",
      password: "",
      password2: "", // 비밀번호 재입력 필드 추가
      email: "",
  });

  const [empNoError, setEmpNoError] = useState("");
  const [userIDError, setUserIDError] = useState("");
  const [passwordError, setPasswordError] = useState("");
  const [password2Error, setPassword2Error] = useState("");
  const [emailError, setEmailError] = useState("");

  const [messageApi, contextHolder] = message.useMessage();
  const navigate = useNavigate();

  const validateEmpNo = async (value) => {
      setFormData({ ...formData, emp_no: value });
      if (!value) {
          setEmpNoError("필수 입력 정보입니다.");
          return;
      }
      try {
          const res = await axios.post("http://127.0.0.1:8000/api/users/check-emp-no/", { emp_no: value });
          setEmpNoError(res.data.message || "");
      } catch (error) {
          console.error("직번 확인 오류:", error.response?.data);
          setEmpNoError(error.response?.data?.message || "직번 확인에 실패했습니다.");
      }
  };

  const validateUserID = async (value) => {
      setFormData({ ...formData, userID: value });
      if (!value) {
          setUserIDError("필수 입력 정보입니다.");
          return;
      }
      try {
          const res = await axios.post("http://127.0.0.1:8000/api/users/check-user-id/", { userID: value });
          setUserIDError(res.data.message || "");
      } catch (error) {
          console.error("아이디 확인 오류:", error.response?.data);
          setUserIDError(error.response?.data?.message || "아이디 확인에 실패했습니다.");
      }
  };

  const validatePassword = (value) => {
      setFormData({ ...formData, password: value });
      if (!value) {
          setPasswordError("필수 입력 정보입니다.");
      } else if (formData.password2 && value !== formData.password2) {
          setPassword2Error("비밀번호가 다릅니다.");
      } else if (formData.password2 && value === formData.password2) {
          setPassword2Error("");
      } else {
          setPasswordError("");
      }
  };

  const validatePassword2 = (value) => {
      setFormData({ ...formData, password2: value });
      if (!value) {
          setPassword2Error("필수 입력 정보입니다.");
      } else if (formData.password !== value) {
          setPassword2Error("비밀번호가 다릅니다.");
      } else {
          setPassword2Error("");
      }
  };

  const validateEmail = (value) => {
      setFormData({ ...formData, email: value });
      if (!value) {
          setEmailError("필수 입력 정보입니다.");
      } else if (!/\S+@\S+\.\S+/.test(value)) {
          setEmailError("올바른 이메일 형식이 아닙니다.");
      } else {
          setEmailError("");
      }
  };

  const handleSubmit = async (e) => {
      e.preventDefault();

      // 폼 제출 시 최종 유효성 검사 (빈 값 여부)
      if (!formData.emp_no) setEmpNoError("필수 입력 정보입니다.");
      if (!formData.userID) setUserIDError("필수 입력 정보입니다.");
      if (!formData.password) setPasswordError("필수 입력 정보입니다.");
      if (!formData.password2) setPassword2Error("필수 입력 정보입니다.");
      if (!formData.email) setEmailError("필수 입력 정보입니다.");

      // 오류가 있으면 제출 막기
      if (empNoError || userIDError || passwordError || password2Error || emailError ||
          !formData.emp_no || !formData.userID || !formData.password || !formData.password2 || !formData.email) {
          messageApi.error("입력하신 정보를 다시 확인해주세요.");
          return;
      }

      try {
          const res = await axios.post("http://127.0.0.1:8000/api/users/register/", formData);
          messageApi.success("회원가입 성공! 🎉");
          console.log("서버 응답:", res.data);
          setTimeout(() => {
              navigate("/login");
          }, 1500);
      } catch (error) {
          console.error("회원가입 실패:", error.response?.data);
          messageApi.error("회원가입 실패! 😢");
      }
  };

  return (
    <MainDiv>
      {contextHolder}
      <FormBox>
          <Title>Sign Up</Title>
          <StyledForm onSubmit={handleSubmit}>
              <Input
                  name="emp_no"
                  placeholder="직번"
                  onChange={(e) => validateEmpNo(e.target.value)}
                  value={formData.emp_no}
              />
              {empNoError && (
                <ErrorMessage
                  isSuccess={empNoError === "직원입니다."}
                  isError={empNoError !== "" && empNoError !== "직원입니다."}
                >
                  {empNoError}
                </ErrorMessage>
              )}
              <Input
                  name="userID"
                  placeholder="아이디"
                  onChange={(e) => validateUserID(e.target.value)}
                  value={formData.userID}
              />
              {userIDError && (
                <ErrorMessage
                  isSuccess={userIDError === "가입할 수 있는 ID입니다."}
                  isError={userIDError !== "" && userIDError !== "가입할 수 있는 ID입니다."}
                >
                  {userIDError}
                </ErrorMessage>
              )}
              <Input.Password
                  name="password"
                  placeholder="비밀번호"
                  iconRender={visible => (visible ? <EyeTwoTone /> : <EyeInvisibleOutlined />)}
                  onChange={(e) => validatePassword(e.target.value)}
                  value={formData.password}
              />
              {passwordError && <ErrorMessage>{passwordError}</ErrorMessage>}
              <Input.Password
                  name="password2"
                  placeholder="비밀번호 재입력"
                  iconRender={visible => (visible ? <EyeTwoTone /> : <EyeInvisibleOutlined />)}
                  onChange={(e) => validatePassword2(e.target.value)}
                  value={formData.password2}
              />
              {password2Error && <ErrorMessage>{password2Error}</ErrorMessage>}
              <Input
                  name="email"
                  placeholder="이메일"
                  onChange={(e) => validateEmail(e.target.value)}
                  value={formData.email}
              />
              {emailError && <ErrorMessage>{emailError}</ErrorMessage>}
              <Button htmlType="submit" type="primary">회원가입</Button>
          </StyledForm>
      </FormBox>
    </MainDiv>
  );
}

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

  input, button, .ant-input-password {
    padding: 10px;
    height: 48px;
    font-size: 16px;
    line-height: 48px; 
  }

  .ant-input-password input {
    height: 100%;
    line-height: 48px;
    margin-bottom: 10px;
  }
`;

const ErrorMessage = styled('div', {
  shouldForwardProp: (prop) => !['isSuccess', 'isError'].includes(prop),
})`
  color: red;
  font-size: 0.8rem;
  ${props => props.isSuccess && `
    color: blue;
  `}
`;