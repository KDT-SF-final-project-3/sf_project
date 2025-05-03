// src/pages/DataMonitor.jsx

import React, { useEffect, useState } from "react";
import axios from "axios";

function DataMonitor() {
  const [tables, setTables] = useState({
    table1: [],
    table2: [],
    table3: [],
    table4: [],
  });

  const fetchData = () => {
    axios.get("http://localhost:8000/print_db/get-tables/")
      .then((res) => {
        console.log("✅ API 응답:", res.data);  // 콘솔 확인용
        setTables(res.data);
      })
      .catch((err) => {
        console.error("❌ API 오류:", err);
      });
  };

  useEffect(() => {
    fetchData(); // 최초 실행
    const interval = setInterval(fetchData, 10000); // 10초마다 실행
    return () => clearInterval(interval); // 언마운트 시 정리
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h2>📊 Smart Factory 실시간 데이터 모니터링</h2>

      {Object.entries(tables).map(([tableName, rows]) => (
        <section key={tableName} style={{ marginBottom: "30px" }}>
          <h3>{tableName.toUpperCase()}</h3>
          {rows.length === 0 ? (
            <p>데이터 없음</p>
          ) : (
            <table border="1" cellPadding="5" style={{ borderCollapse: "collapse", width: "100%" }}>
              <thead>
                <tr>
                  {Object.keys(rows[0]).map((col) => (
                    <th key={col}>{col}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {rows.map((row, idx) => (
                  <tr key={idx}>
                    {Object.values(row).map((val, i) => (
                      <td key={i}>{String(val)}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </section>
      ))}
    </div>
  );
}

export default DataMonitor;