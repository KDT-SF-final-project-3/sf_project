import React, { useEffect, useState } from 'react';
import { Table } from 'antd';
import axios from 'axios';

const OperationHistoryPage = () => {
  const [table4Data, setTable4Data] = useState([]);
  const [lastUpdated, setLastUpdated] = useState(null);

  useEffect(() => {
    const fetchData = () => {
      axios.get('http://localhost:8000/printdb/table4/')
        .then(res => {
          setTable4Data(res.data);
          setLastUpdated(new Date());
        })
        .catch(err => console.error('table4 불러오기 실패:', err));
    };

    fetchData();
    const interval = setInterval(fetchData, 10000);
    return () => clearInterval(interval);
  }, []);

  const columns = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: '명령어', dataIndex: 'command', key: 'command' },
    { title: '시작 시간', dataIndex: 'start_time', key: 'start_time' },
    { title: '종료 시간', dataIndex: 'end_time', key: 'end_time' },
  ];

  return (
    <div style={{ padding: 24 }}>
      <h2>⚙️ 최근 제어 명령 (table4)</h2>
      {lastUpdated && (
        <p style={{ fontStyle: 'italic', color: 'gray' }}>
          📅 마지막 갱신 시각: {lastUpdated.toLocaleTimeString()}
        </p>
      )}
      <Table
        dataSource={table4Data}
        columns={columns}
        rowKey="id"
        pagination={{ pageSize: 10 }}
      />
    </div>
  );
};

export default OperationHistoryPage;