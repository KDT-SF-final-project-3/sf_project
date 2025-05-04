// Table3Page.jsx

import React, { useEffect, useState } from 'react';
import { Table, Button, Form, DatePicker, message } from 'antd';
import axios from 'axios';
import dayjs from 'dayjs';

const Table3Page = () => {
  const [table3Data, setTable3Data] = useState([]);
  const [lastUpdated, setLastUpdated] = useState(null);
  const [form] = Form.useForm();

  // 전체 이력 데이터 로딩
  const fetchData = () => {
    axios.get('http://localhost:8000/printdb/table3/')
      .then(res => {
        setTable3Data(res.data);
        setLastUpdated(new Date());
      })
      .catch(err => {
        console.error('이력 불러오기 실패:', err);
        message.error('이력 데이터를 불러오는 데 실패했습니다.');
      });
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 10000); // 10초마다 새로고침
    return () => clearInterval(interval);
  }, []);

  // 내보내기 처리
  const handleExport = ({ start_time, end_time }) => {
    const start = dayjs(start_time).format("YYYY-MM-DD HH:mm:ss");
    const end = dayjs(end_time).format("YYYY-MM-DD HH:mm:ss");

    const url = `http://localhost:8000/printdb/table3/export/?start=${start}&end=${end}`;
    window.open(url, '_blank');
  };

  // 테이블 컬럼 정의
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
      <h2>📊 환경 이력 </h2>
      <br />

      {/* 시간 범위 선택 + 내보내기 버튼 */}
      <Form
        form={form}
        layout="inline"
        onFinish={handleExport}
        style={{ marginBottom: 24 }}
      >
        <Form.Item name="start_time" rules={[{ required: true }]}>
          <DatePicker showTime format="YYYY-MM-DD HH:mm:ss" placeholder="시작 시간" />
        </Form.Item>
        <Form.Item name="end_time" rules={[{ required: true }]}>
          <DatePicker showTime format="YYYY-MM-DD HH:mm:ss" placeholder="종료 시간" />
        </Form.Item>
        <Form.Item>
          <Button type="primary" htmlType="submit">📁 CSV 내보내기</Button>
        </Form.Item>
      </Form>

      {/* 갱신 시간 */}
      {lastUpdated && (
        <p style={{ fontStyle: 'italic', color: 'gray' }}>
          🔄 마지막 갱신: {lastUpdated.toLocaleTimeString()}
        </p>
      )}

      {/* 전체 이력 테이블 */}
      <Table
        dataSource={table3Data}
        columns={columns}
        rowKey="id"
        pagination={{ pageSize: 10 }}
      />
    </div>
  );
};

export default Table3Page;