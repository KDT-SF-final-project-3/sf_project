import React, { useEffect, useState } from 'react';
import { Table, Button, DatePicker, Typography } from 'antd';
import axios from 'axios';

const { RangePicker } = DatePicker;
const { Text } = Typography;

const OperationHistoryPage = () => {
  const [table4Data, setTable4Data] = useState([]);
  const [table5Data, setTable5Data] = useState([]);
  const [lastUpdated, setLastUpdated] = useState(null);
  const [range4, setRange4] = useState([]);
  const [range5, setRange5] = useState([]);

  useEffect(() => {
    const fetchTable4 = () => {
      axios.get('http://localhost:8000/printdb/table4/')
        .then(res => {
          setTable4Data(res.data);
          setLastUpdated(new Date());
        })
        .catch(err => console.error('table4 불러오기 실패:', err));
    };

    const fetchTable5 = () => {
      axios.get('http://localhost:8000/printdb/table5/')
        .then(res => {
          setTable5Data(res.data.items);
        })
        .catch(err => console.error('table5 불러오기 실패:', err));
    };

    fetchTable4();
    fetchTable5();

    const interval = setInterval(() => {
      fetchTable4();
      fetchTable5();
    }, 10000);

    return () => clearInterval(interval);
  }, []);

  const table4Columns = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: '명령어', dataIndex: 'command', key: 'command' },
    { title: '시작 시간', dataIndex: 'start_time', key: 'start_time' },
    { title: '종료 시간', dataIndex: 'end_time', key: 'end_time' },
  ];

  const table5Columns = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: '명령어', dataIndex: 'command', key: 'command' },
    { title: '시작 시간', dataIndex: 'start_time', key: 'start_time' },
    { title: '종료 시간', dataIndex: 'end_time', key: 'end_time' },
  ];

  return (
    <div style={{ padding: 24 }}>
      {/* ⚙️ 수동 이력 */}
      <div style={{ fontSize: '28px', fontWeight: 'bold', marginBottom: '8px' }}>
        ⚙️ 작동 이력 (수동)
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px' }}>
        <RangePicker
          showTime
          format="YYYY-MM-DD HH:mm:ss"
          value={range4}
          onChange={(val) => setRange4(val)}
          style={{ width: 300 }}
        />
        <Button type="primary" onClick={() => window.location.href = 'http://localhost:8000/printdb/table4/export/'}>
          📁 CSV 내보내기
        </Button>
      </div>
      <Text type="secondary" style={{ display: 'block', marginBottom: 8 }}>
        📅 마지막 갱신 시각: {lastUpdated ? lastUpdated.toLocaleTimeString() : '-'}
      </Text>
      <Table
        dataSource={table4Data}
        columns={table4Columns}
        rowKey="id"
        pagination={{ pageSize: 10 }}
      />

      <hr style={{ margin: '40px 0' }} />

      {/* 📋 자동 이력 */}
      <div style={{ fontSize: '28px', fontWeight: 'bold', marginBottom: '8px' }}>
        📋 작동 이력 (자동)
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px' }}>
        <RangePicker
          showTime
          format="YYYY-MM-DD HH:mm:ss"
          value={range5}
          onChange={(val) => setRange5(val)}
          style={{ width: 300 }}
        />
        <Button type="primary" onClick={() => window.location.href = 'http://localhost:8000/printdb/table5/export/'}>
          📁 CSV 내보내기
        </Button>
      </div>
      <Text type="secondary" style={{ display: 'block', marginBottom: 8 }}>
        📅 마지막 갱신 시각: {lastUpdated ? lastUpdated.toLocaleTimeString() : '-'}
      </Text>
      <Table
        dataSource={table5Data}
        columns={table5Columns}
        rowKey="id"
        pagination={{ pageSize: 10 }}
      />
    </div>
  );
};

export default OperationHistoryPage;
