import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const LoginPage = () => {
    const [formData, setFormData] = useState({
        userID: "",
        password: "",
    });
    const [message, setMessage] = useState("");
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
            
            // 서버로부터 받은 JWT 토큰을 로컬 스토리지에 저장
            localStorage.setItem("access_token", res.data.access);
            localStorage.setItem("refresh_token", res.data.refresh);
    
             // ✅ 서버 응답에서 is_approved 가져오기
            const { access, refresh, is_approved } = res.data;

            if (is_approved) {
                localStorage.setItem("access_token", access);
                localStorage.setItem("refresh_token", refresh);

                setMessage("✅ 로그인 성공! 🎉");
                navigate("/");  // 👉 메인페이지로 이동
            } else {
                setMessage("❌ 승인되지 않은 계정입니다. 관리자에게 문의하세요.");
            }
    
        } catch (error) {
            console.error("로그인 실패:", error.response.data);
            setMessage("❌ 로그인 실패! 😢 아이디 또는 비밀번호를 확인해주세요.");
        }
    };

    const goToRegister = () => {
        navigate("/register");  // 회원가입 페이지로 리다이렉트
    };


    return (
        <div>
            <h2>로그인</h2>
            <form onSubmit={handleSubmit}>
                <input
                name="userID"
                type="text"
                placeholder="아이디"
                onChange={handleChange}
                value={formData.userID}
                />
                <input
                name="password"
                type="password"
                placeholder="비밀번호"
                onChange={handleChange}
                value={formData.password}
                />
                <button type="submit">로그인</button>
            </form>
            <p>{message}</p>

            <button onClick={goToRegister}>회원가입</button>
        </div>
    );
};

export default LoginPage;