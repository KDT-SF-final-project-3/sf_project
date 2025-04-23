import "./App.css";
import React, { useState } from "react";
import axios from "axios";
import FetchButton from "./Components/Table/FetchButton";
import DataTable from "./Components/Table/DataTable";

function App() {
  const [data, setData] = useState([]);

  const fetchData = async () => {
    axios.get('http://127.0.0.1:8000/temp/api/data/')
      .then((res) => {
          console.log("받은 데이터:", res.data);
          setData(res.data);
      })
      .catch((err) => console.error("에러 발생:", err));
  };

  return (
    <div>
      <h1>테스트 테이블 데이터 확인</h1>
      <FetchButton onFetch={fetchData} />
      <DataTable data={data}/>
    </div>
  );
}

export default App;
