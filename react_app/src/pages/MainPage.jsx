// src/pages/MainPage.jsx
import React from "react";
import styled from "styled-components";
import { Layout as AntLayout, Menu } from 'antd';
import { BrowserRouter as Route, Routes, Link } from 'react-router-dom';
import { HomeOutlined, UserOutlined, HistoryOutlined, BarChartOutlined, LogoutOutlined } from '@ant-design/icons';
import { useNavigate } from "react-router-dom";
import { logout } from "../utils/auth";

import OperationHistoryPage from './OperationHistoryPage';
import EnvironmentHistoryPage from './EnvironmentHistoryPage';
import AdminPage from './AdminPage';
import HomePage from './HomePage';

const { Header: AntHeader, Sider: AntSider, Content: AntContent, Footer: AntFooter } = AntLayout;

export default function MainPage() {
    const navigate = useNavigate();
    const name = localStorage.getItem("name");

    const handleLogout = () => {
        logout();
        navigate("/login");
    };

    return (
        <Layout>
            <Sider width={200}>
                <div>
                    {name ? `${name}님` : "사용자"}
                </div>
                <Menu mode="inline" defaultSelectedKeys={['1']} style={{ borderRight: 0 }}>
                    <Menu.Item key="1" icon={<HomeOutlined />}>
                        <Link to="/">홈</Link>
                    </Menu.Item>
                    <Menu.Item key="2" icon={<HistoryOutlined />}>
                        <Link to="/operation">작동 이력</Link>
                    </Menu.Item>
                    <Menu.Item key="3" icon={<BarChartOutlined />}>
                        <Link to="/environment">환경 이력</Link>
                    </Menu.Item>
                    <Menu.Item key="4" icon={<UserOutlined />}>
                        <Link to="/admin">관리자 페이지</Link>
                    </Menu.Item>
                </Menu>

                <LogoutWrapper>
                    <Menu mode="inline">
                        <Menu.Item key="logout" icon={<LogoutOutlined />}
                            onClick={handleLogout} style={{ color: 'red' }}>
                            로그아웃
                        </Menu.Item>
                    </Menu>
                </LogoutWrapper>
            </Sider>

            <ContentLayout>
                <Header>
                    <Title>3 Factorial</Title>
                </Header>

                <Content style={{ margin: '24px 16px 0', padding: 24, background: '#fff' }}>
                    <Routes>
                        <Route path="/" element={<HomePage />} />
                        <Route path="/operation" element={<OperationHistoryPage />} />
                        <Route path="/environment" element={<EnvironmentHistoryPage />} />
                        <Route path="/admin" element={<AdminPage />} />
                    </Routes>
                </Content>


                <Footer>© Smart Factory</Footer>
                
            </ContentLayout>
        </Layout>
    );
}

// --- styled-components 정의 ---
const Layout = styled(AntLayout)`
  min-height: 100vh;
`;

const Header = styled(AntHeader)`
  background: #fff;
  height: 64px;
  line-height: 64px;
  padding: 0;
  position: fixed;
  width: 100%;
  top: 0;
  z-index: 10;
`;

const Title = styled.h1`
  text-align: center;
  font-weight: bold;
`;

const Sider = styled(AntSider)`
  background: #fff;
  position: fixed;
  height: 100vh;
  left: 0;
  overflow: auto;
`;

const ContentLayout = styled(AntLayout)`
  margin-left: 200px;
  margin-top: 64px;
`;

const Content = styled(AntContent)`
  margin: 16px;
`;

const Footer = styled(AntFooter)`
  text-align: center;
`;

const LogoutWrapper = styled.div`
  position: absolute;
  bottom: 0;
  width: 100%;
`;