// import React from 'react'; React 17버전 이후로는 자동 JSX 변환!

function FetchButton({onFetch}){
    return(
        <button onClick={onFetch}>
            데이터 불러오기
        </button>
    );
}

export default FetchButton;
