// src/components/WebcamViewer.jsx
import React from 'react';

const WebcamViewer = () => {
    return (
        <div>
            <h2>웹캠 스트림</h2>
            <img 
                src="http://localhost:8000/video_feed/" 
                alt="Webcam Stream" 
                style={{ width: "100%", maxWidth: "600px" }}
            />
        </div>
    );
};

export default WebcamViewer;