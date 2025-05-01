import React from "react";
import { Layout, Menu } from 'antd';
import { HomeOutlined, UserOutlined } from '@ant-design/icons';
import LogoutButton from "../components/LogoutButton";

const { Header, Footer, Sider, Content } = Layout;

export default function MainPage() {
    return (
        <Layout style={{ minHeight: '100vh' }}>
            {/* 사이드바 */}
            <Sider width={200} className="site-layout-background">
                <Menu
                    mode="inline"
                    defaultSelectedKeys={['1']}
                    style={{ height: '100%', borderRight: 0 }}
                >
                    <Menu.Item key="1" icon={<HomeOutlined />}>
                        홈
                    </Menu.Item>
                    <Menu.Item key="2" icon={<UserOutlined />}>
                        사용자 관리
                    </Menu.Item>
                </Menu>
            </Sider>

            {/* 메인 컨텐츠 */}
            <Layout>
                <Header style={{ background: '#fff', padding: 0 }}>
                    <h1 style={{ textAlign: 'center', fontWeight: 'bold' }}>메인 페이지</h1>
                </Header>
                <Content style={{ margin: '16px' }}>
                    <div style={{ padding: 24, background: '#fff', minHeight: 360 }}>
                        <p>여기는 로그인한 사용자만 접근할 수 있어요.</p>
                        <LogoutButton />
                    </div>
                </Content>
                <Footer style={{ textAlign: 'center' }}>© 2025 회사 이름</Footer>
            </Layout>
        </Layout>
    );
}


