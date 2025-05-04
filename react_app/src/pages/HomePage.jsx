import React, { useEffect, useState } from 'react';
import { Button, Typography, Row, Col, Card, Tag } from 'antd';
import { Layout } from 'antd';
import styled from 'styled-components';
import axios from 'axios';
import WebcamViewer from '../components/WebcamViewer';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const { Content } = Layout;
const { Text } = Typography;

const ContentBox = styled.div`
  padding: 24px;
  background: #fff;
  min-height: 360px;
`;

const GameButton = styled(Button)`
  width: 100px;
  height: 60px;
  font-size: 16px;
  font-weight: bold;
  color: #000;
  background-color: #ffffff;
  border: 1px solid #d9d9d9;
  &:hover {
    background-color: #f5f5f5;
  }
`;

const CenteredCard = styled(Card)`
  text-align: center;
  font-size: 16px;
  line-height: 2;
`;

const OperationHistoryPage = () => {
  const [table7Data, setTable7Data] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);
  const [mode, setMode] = useState('manual');

  const dummyActionCounts = {
    A: 3,
    B: 5,
    C: 2
  };

  const actionData = {
    labels: ['A', 'B', 'C'],
    datasets: [
      {
        label: '동작 횟수',
        data: Object.values(dummyActionCounts),
        backgroundColor: ['#ff4d4f', '#1890ff', '#52c41a'],
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: { display: false },
      title: { display: false },
    },
    scales: {
      x: {
        ticks: { font: { size: 14 } },
      },
      y: {
        beginAtZero: true,
        ticks: { stepSize: 1 },
      },
    },
  };

  useEffect(() => {
    const fetchData = () => {
      axios.get('http://localhost:8000/printdb/table7/')
        .then(res => {
          setTable7Data(res.data);
          setLastUpdated(new Date());
        })
        .catch(err => console.error('table7 불러오기 실패:', err));
    };

    fetchData();
    const interval = setInterval(fetchData, 10000);
    return () => clearInterval(interval);
  }, []);

  const renderStatusLight = () => (
    <Tag color={mode === 'auto' ? 'green' : 'red'}>
      {mode === 'auto' ? '자동 운용 중' : '수동 모드'}
    </Tag>
  );

  const handleCommand = (cmd) => {
    if (cmd === '자동') setMode('auto');
    else if (cmd === '수동') setMode('manual');
    else if (mode === 'manual') console.log(`명령 전송: ${cmd}`);
  };

  const sensorData = table7Data ? [
    { label: '🌡 온도 (℃)', value: table7Data.temperature },
    { label: '💧 습도 (%)', value: table7Data.humidity },
    { label: '💡 조도', value: table7Data.light },
    { label: '⏰ 시간', value: table7Data.timestamp },
    { label: '🌀 팬 상태', value: table7Data.fan_status },
    { label: '🔆 LED 상태', value: table7Data.led_status },
  ] : [];

  const buttonList = [
    '잡기', '놓기',
    '상승', '하강',
    '회전', '역회전',
    '수동', '자동', '정지'
  ];

  return (
    <Content>
      <ContentBox>
        <Row gutter={[16, 16]}>
          <Col span={12}>
            <WebcamViewer />
          </Col>
          <Col span={12}>
            <Typography.Title level={3}>🎮 로봇 제어</Typography.Title>
            <div style={{ marginBottom: 16 }}>{renderStatusLight()}</div>
            <Row gutter={[16, 16]}>
              {buttonList.map((label, index) => (
                <Col span={index < 6 ? 12 : 8} key={label} style={{ textAlign: 'center' }}>
                  <GameButton
                    onClick={() => handleCommand(label)}
                    disabled={mode === 'auto' && label !== '수동' && label !== '자동'}
                  >
                    {label}
                  </GameButton>
                </Col>
              ))}
            </Row>
          </Col>
        </Row>

        <div style={{ marginTop: 40 }}>
          <Row gutter={[16, 16]}>
            <Col span={12}>
              <Card title="동작 횟수">
                <Bar data={actionData} options={chartOptions} height={100} />
              </Card>
            </Col>
            <Col span={12}>
              <CenteredCard title="🌍 환경 현황">
                {sensorData.map(item => (
                  <div key={item.label}>
                    <strong>{item.label}</strong>: {item.value}
                  </div>
                ))}
              </CenteredCard>
            </Col>
          </Row>

          {lastUpdated && (
            <p style={{ fontStyle: 'italic', color: 'gray', marginTop: 12, textAlign: 'center' }}>
              🔄 마지막 갱신 시각: {lastUpdated.toLocaleTimeString()}
            </p>
          )}
        </div>
      </ContentBox>
    </Content>
  );
};

export default OperationHistoryPage;
