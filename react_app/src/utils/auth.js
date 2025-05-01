
// 로그아웃 시 토큰 삭제
export function logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
}