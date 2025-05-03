import React from 'react';
import { Table } from 'antd';

const OperationHistoryPage = () => {
  // 임시 데이터
  const dataSource = [
    {
      key: '3',
      date: '2025-05-12 12:30:00',
      action: 'Fan ON',
      user: 'admin',
    },
    {
      key: '2',
      date: '2025-05-02 16:45:00',
      action: 'LED OFF',
      user: 'user1',
    },
  ];

  // 테이블 컬럼 정의
  const columns = [
    {
      title: '날짜',
      dataIndex: 'date',
      key: 'date',
    },
    {
      title: '작동 내용',
      dataIndex: 'action',
      key: 'action',
    },
    {
      title: '작업자',
      dataIndex: 'user',
      key: 'user',
    },
  ];

  return (
    <div>
      <h2 style={{ marginBottom: '16px' }}>작동 이력</h2>
      <Table dataSource={dataSource} columns={columns} />
    </div>
  );
};

export default OperationHistoryPage;