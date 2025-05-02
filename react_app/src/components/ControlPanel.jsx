import React from "react";

const commands = ['a', 'm', '1,1', '1,2', '2,1', '2,2', '3,1', '3,2', 'q'];

const ControlPanel = () => {
  const sendCommand = async (cmd) => {
    try {
      const response = await fetch(`http://localhost:8000/api/control/?cmd=${encodeURIComponent(cmd)}`);
      const data = await response.json();
      console.log(`[${cmd}] 응답:`, data);
    } catch (error) {
      console.error(`[${cmd}] 오류:`, error);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', width: '200px' }}>
      {commands.map((cmd) => (
        <button
          key={cmd}
          onClick={() => sendCommand(cmd)}
          style={{ padding: '10px', fontSize: '16px' }}
        >
          {cmd}
        </button>
      ))}
    </div>
  );
};

export default ControlPanel;