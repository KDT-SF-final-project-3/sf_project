import './DataTable.css';

function DataTable({data}){
    return(
        <table className="table">
            <thead>
                <th>
                    <th>ID</th>
                    <th>이름</th>
                    <th>나이</th>
                    <th>날짜</th>
                </th>
            </thead>
            <tbody>
                {data.map((item) => (
                    <tr key={item.id}>
                        <td>{item.id}</td>
                        <td>{item.name}</td>
                        <td>{item.age}</td>
                        <td>{item.created_at}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
}

export default DataTable;