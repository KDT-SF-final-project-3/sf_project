import React from "react";
import styled from "styled-components";
import { Layout as AntLayout, Menu } from 'antd';
import { HomeOutlined, UserOutlined, LogoutOutlined } from '@ant-design/icons';
import { useNavigate } from "react-router-dom";
import { logout } from "../utils/auth";

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
                        홈
                    </Menu.Item>
                    <Menu.Item key="2" icon={<UserOutlined />}>
                        사용자 관리
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

                <Content>
                    <ContentBox>
                        <p>여기는 로그인한 사용자만 접근할 수 있어요.</p>
                    </ContentBox>
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

const ContentBox = styled.div`
  padding: 24px;
  background: #fff;
  min-height: 360px;
`;

const Footer = styled(AntFooter)`
  text-align: center;
`;

const LogoutWrapper = styled.div`
  position: absolute;
  bottom: 0;
  width: 100%;
`;