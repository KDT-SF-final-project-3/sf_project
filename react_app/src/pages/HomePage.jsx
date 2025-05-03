import React, { useEffect, useState } from 'react';
import { Row, Col, Card } from 'antd';
import { Layout, Table } from 'antd';
import styled from 'styled-components';
import axios from 'axios';
import WebcamViewer from "../components/WebcamViewer"; 
import ControlPanel from "../components/ControlPanel";

const { Content } = Layout;

const ContentBox = styled.div`
  padding: 24px;
  background: #fff;
  min-height: 360px;
`;

const OperationHistoryPage = () => {
  const [table7Data, setTable7Data] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null); // ✅ 마지막 갱신 시각

  // ✅ table7 데이터 10초마다 자동 갱신
  useEffect(() => {
    const fetchData = () => {
      axios.get('http://localhost:8000/printdb/table7/')
        .then(res => {
          setTable7Data(res.data);
          setLastUpdated(new Date()); // ✅ 갱신 시각 저장
        })
        .catch(err => console.error('table7 불러오기 실패:', err));
    };

    fetchData(); // 최초 1회 실행
    const interval = setInterval(fetchData, 10000); // 10초마다 갱신

    return () => clearInterval(interval); // 언마운트 시 인터벌 해제
  }, []);

  // 작동 이력 예시 데이터
  const columns = [
    { title: '날짜', dataIndex: 'date', key: 'date' },
    { title: '작동 내용', dataIndex: 'action', key: 'action' },
    { title: '작업자', dataIndex: 'user', key: 'user' },
  ];


  return (
    <Content>
      <ContentBox>
        <WebcamViewer />
        <h1>로봇 제어 패널</h1>
        <ControlPanel />
        <p>여기는 로그인한 사용자만 접근할 수 있어요.</p>

        {/* ✅ 센서 데이터 출력 */}
        {table7Data ? (
          <div style={{ marginTop: 32 }}>
            <h3>📡 센서 최신 데이터 (10초마다 자동 갱신)</h3>

            {/* ✅ 마지막 갱신 시각 표시 */}
            {lastUpdated && (
              <p style={{ fontStyle: 'italic', color: 'gray' }}>
                🔄 마지막 갱신 시각: {lastUpdated.toLocaleTimeString()}
              </p>
            )}

            <Row gutter={[16, 16]}>
              <Col xs={24} sm={12} md={8}>
                <Card title="조도" bordered>{table7Data.light}</Card>
              </Col>
              <Col xs={24} sm={12} md={8}>
                <Card title="온도 (℃)" bordered>{table7Data.temperature}</Card>
              </Col>
              <Col xs={24} sm={12} md={8}>
                <Card title="습도 (%)" bordered>{table7Data.humidity}</Card>
              </Col>
              <Col xs={24} sm={12} md={8}>
                <Card title="팬 상태" bordered>{table7Data.fan_status}</Card>
              </Col>
              <Col xs={24} sm={12} md={8}>
                <Card title="LED 상태" bordered>{table7Data.led_status}</Card>
              </Col>
              <Col xs={24} sm={12} md={8}>
                <Card title="측정 시각" bordered>{table7Data.timestamp}</Card>
              </Col>
            </Row>
          </div>
        ) : (
          <p>센서 데이터를 불러오는 중...</p>
        )}


      </ContentBox>
    </Content>
  );
};

export default OperationHistoryPage;