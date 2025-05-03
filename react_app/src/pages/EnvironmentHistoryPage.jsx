import React, { useEffect, useState } from 'react';
import { Table } from 'antd';
import axios from 'axios';

const Table3Page = () => {
  const [table3Data, setTable3Data] = useState([]);
  const [lastUpdated, setLastUpdated] = useState(null);

  useEffect(() => {
    const fetchData = () => {
      axios.get('http://localhost:8000/printdb/table3/')
        .then(res => {
          setTable3Data(res.data);
          setLastUpdated(new Date());
        })
        .catch(err => console.error('table3 불러오기 실패:', err));
    };

    fetchData();
    const interval = setInterval(fetchData, 10000);
    return () => clearInterval(interval);
  }, []);

  const columns = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: '조도', dataIndex: 'light', key: 'light' },
    { title: '온도 (℃)', dataIndex: 'temperature', key: 'temperature' },
    { title: '습도 (%)', dataIndex: 'humidity', key: 'humidity' },
    { title: '팬 상태', dataIndex: 'fan_status', key: 'fan_status' },
    { title: 'LED 상태', dataIndex: 'led_status', key: 'led_status' },
    { title: '시간', dataIndex: 'timestamp', key: 'timestamp' },
  ];

  return (
    <div style={{ padding: 24 }}>
      <h2>📊 환경 이력 (table3)</h2>
      {lastUpdated && (
        <p style={{ fontStyle: 'italic', color: 'gray' }}>
          🔄 마지막 갱신 시각: {lastUpdated.toLocaleTimeString()}
        </p>
      )}
      <Table dataSource={table3Data} columns={columns} rowKey="id" />
    </div>
  );
};

export default Table3Page;