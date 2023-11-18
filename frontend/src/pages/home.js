import React from 'react';
import { Link } from "react-router-dom";

export default function Home() {
  return (
    <div className="container">
      <div className="card">
        <div className="card-header">
          <h2 className="text-center mt-5 mb-3">Home</h2>
        </div>
        <div className="card-body">
          <p><Link to={`/list`} className="btn btn-outline-success">Concert 목록 보기</Link></p>
          <p><Link to={`/add`} className="btn btn-outline-success">Concert 등록하기</Link></p>
        </div>
      </div>         
    </div>
  );
}