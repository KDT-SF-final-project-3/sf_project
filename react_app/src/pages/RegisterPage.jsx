import React, { useState, useEffect } from "react";
import axios from "axios";
import { EyeInvisibleOutlined, EyeTwoTone } from '@ant-design/icons';
import {Input, Button, message} from 'antd';
import { useNavigate } from "react-router-dom";
import styled from 'styled-components';

export default function RegisterForm() {
  const [formData, setFormData] = useState({
      emp_no: "",
      userID: "",
      password: "",
      password2: "", 
      email: "",
      name: "",      
      position: "",
  });

  const [empNoError, setEmpNoError] = useState("");
  const [userIDError, setUserIDError] = useState("");
  const [passwordError, setPasswordError] = useState("");
  const [password2Error, setPassword2Error] = useState("");
  const [emailError, setEmailError] = useState("");

  const [messageApi, contextHolder] = message.useMessage();
  const navigate = useNavigate();

  const [empNoToCheck, setEmpNoToCheck] = useState("");

  useEffect(() => {
    const fetchInfo = async () => {
      if (empNoToCheck) {
        try {
          const getRes = await axios.get(`http://127.0.0.1:8000/api/accounts/check-emp-no/?emp_no=${empNoToCheck}`);
          setFormData(prevFormData => ({
            ...prevFormData,
            name: getRes.data.name,
            position: getRes.data.position,
          }));
        } catch (error) {
          console.error("직원 정보 GET 요청 오류:", error.response?.data);
          messageApi.error("직원 정보 로딩 실패");
          setFormData(prevFormData => ({ ...prevFormData, name: "", position: "" }));
        }
      } else {
        setFormData(prevFormData => ({ ...prevFormData, name: "", position: "" }));
      }
    };

    fetchInfo();
  }, [empNoToCheck, messageApi]);

  const validateEmpNo = (value) => {
    setFormData(prevFormData => ({ ...prevFormData, emp_no: value }));
    setEmpNoError("");

    if (!value) {
      setEmpNoError("필수 입력 정보입니다.");
      setEmpNoToCheck(""); // 직번이 없으면 GET 요청 안 함
      return;
    }

    console.log("Sending emp_no:", value); // 추가

    // 간단한 형식 검사만 수행하거나, POST 요청을 통해 서버에서 1차 확인
    // 여기서는 POST 요청을 유지하고, 성공 시 empNoToCheck 상태를 업데이트
    axios.post("http://127.0.0.1:8000/api/accounts/check-emp-no/", { emp_no: value })
      .then(res => {
        setEmpNoError(res.data.message || "");
        if (res.data.message === "직원입니다.") {
          setEmpNoToCheck(value); // 직원 확인되면 GET 요청 트리거
        } else {
          setEmpNoToCheck(""); // 직원이 아니면 GET 요청 안 함
          setFormData(prevFormData => ({ ...prevFormData, name: "", position: "" }));
        }
      })
      .catch(error => {
        console.error("직번 확인 오류:", error.response?.data);
        setEmpNoError(error.response?.data?.message || "직번 확인에 실패했습니다.");
        setEmpNoToCheck("");
        setFormData(prevFormData => ({ ...prevFormData, name: "", position: "" }));
      });
  };

  const validateUserID = async (value) => {
      setFormData({ ...formData, userID: value });
      if (!value) {
          setUserIDError("필수 입력 정보입니다.");
          return;
      }
      try {
          const res = await axios.post("http://127.0.0.1:8000/api/accounts/check-user-id/", { userID: value });
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

    console.log("Form Data before validation:", formData); // 추가
    console.log("Before Validation"); // 추가

    // 1. 에러 상태 초기화
    setEmpNoError(null);
    setUserIDError(null);
    setPasswordError(null);
    setPassword2Error(null);
    setEmailError(null);

    // 2. 수동 유효성 검사 실행 (최신 값 기반으로)
    await validateEmpNo(formData.emp_no);
    await validateUserID(formData.userID);
    validatePassword(formData.password);
    validatePassword2(formData.password2);
    validateEmail(formData.email);

    console.log("After Validation"); // 추가
    console.log("empNoError:", empNoError); // 추가
    console.log("userIDError:", userIDError); // 추가
    console.log("passwordError:", passwordError); // 추가
    console.log("password2Error:", password2Error); // 추가
    console.log("emailError:", emailError); // 추가

    // 3. 에러 메시지가 존재하는지 확인
    const hasError = (empNoError !== null && empNoError !== "" && empNoError !== "직원입니다.") ||
                  (userIDError !== null && userIDError !== "" && userIDError !== "가입할 수 있는 ID입니다.") ||
                  (passwordError !== null && passwordError !== "") ||
                  (password2Error !== null && password2Error !== "") ||
                  (emailError !== null && emailError !== "");

    const hasEmpty = !formData.emp_no || !formData.userID || !formData.password || !formData.password2 || !formData.email;

    // 4. 제출 조건 확인
    console.log("hasError:", hasError, "hasEmpty:", hasEmpty);
    if (hasError || hasEmpty) {
      console.log("Validation Failed. Not submitting.");
      console.log("Form Data (on failure):", formData);
      messageApi.error("입력하신 정보를 다시 확인해주세요.");
      return;
    }

    // 5. 제출
    console.log("Validation Passed. Submitting...");
    console.log("Form Data (on success):", formData);
    try {
      const res = await axios.post("http://127.0.0.1:8000/api/accounts/register/", formData, {
        headers: {
          'Content-Type': 'application/json',
        }
      });
      console.log('회원가입 요청 완료');
      messageApi.success("회원가입 성공! 🎉");
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
                  $isSuccess={empNoError === "직원입니다."}
                  $isError={empNoError !== "" && empNoError !== "직원입니다."}
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
                  $isSuccess={userIDError === "가입할 수 있는 ID입니다."}
                  $isError={userIDError !== "" && userIDError !== "가입할 수 있는 ID입니다."}
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


// 스타일 컴포넌트
const MainDiv = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f0f0f0;
`;

const FormBox = styled.div`
  background-color: white;
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  width: 400px;
  display: flex;
  flex-direction: column;
  align-items: center;
`;

const Title = styled.h2`
  font-size: 32px;
  color: #333;
  margin-bottom: 20px;
`;

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
  shouldForwardProp: (prop) => !['$isSuccess', '$isError'].includes(prop),
})`
  color: red;
  font-size: 0.8rem;
  ${(props) => props.$isSuccess && `color: blue;`}
`;
