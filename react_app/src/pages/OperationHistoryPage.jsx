import React, { useEffect, useState } from 'react';
import { Table, Card, Row, Col } from 'antd';
import axios from 'axios';

const OperationHistoryPage = () => {
  const [table4Data, setTable4Data] = useState([]); // ✅ 배열로 선언
  const [lastUpdated, setLastUpdated] = useState(null);

  useEffect(() => {
    const fetchData = () => {
      axios.get('http://localhost:8000/printdb/table4/')
        .then(res => {
          setTable4Data(res.data); // ✅ 배열로 저장
          setLastUpdated(new Date());
        })
        .catch(err => console.error('table4 불러오기 실패:', err));
    };

    fetchData();
    const interval = setInterval(fetchData, 10000);
    return () => clearInterval(interval);
  }, []);


  return (
    <div style={{ padding: 24 }}>
      <h2>⚙️ 최근 제어 명령 (table4)</h2>
      {lastUpdated && (
        <p style={{ fontStyle: 'italic', color: 'gray' }}>
          🔄 마지막 갱신 시각: {lastUpdated.toLocaleTimeString()}
        </p>
      )}
      {table4Data.length > 0 ? (
        table4Data.map((item, index) => (
          <Row gutter={[16, 16]} key={index} style={{ marginBottom: 16 }}>
            <Col xs={24} sm={12} md={8}>
              <Card title="명령어" bordered>{item.command}</Card>
            </Col>
            <Col xs={24} sm={12} md={8}>
              <Card title="시작 시간" bordered>{item.start_time}</Card>
            </Col>
            <Col xs={24} sm={12} md={8}>
              <Card title="종료 시간" bordered>{item.end_time}</Card>
            </Col>
          </Row>
        ))
      ) : (
        <p>table4 데이터를 불러오는 중...</p>
      )}


    </div>
  );
};

export default OperationHistoryPage;