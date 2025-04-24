// src/components/RegisterForm.jsx
import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const RegisterForm = () => {
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
        <div>
            <h2>회원가입</h2>
            <form onSubmit={handleSubmit}>
                <input name="emp_no" placeholder="직번" onChange={handleChange} />
                <input name="name" placeholder="이름" onChange={handleChange} />
                <input name="userID" placeholder="아이디" onChange={handleChange} />
                <input name="password" type="password" placeholder="비밀번호" onChange={handleChange} />
                <input name="email" placeholder="이메일" onChange={handleChange} />
                <input name="position" placeholder="직급" onChange={handleChange} />
                <button type="submit">가입하기</button>
            </form>

            {message && <p>{message}</p>}
    </div>
    );
};

export default RegisterForm;