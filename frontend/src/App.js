import './App.css';
import React from 'react';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import ConcertList from "./pages/ConcertList";
import ConcertAdd from "./pages/ConcertAdd";
import ConcertView from "./pages/ConcertView";
import ConcertEdit from "./pages/ConcertEdit";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/admin/"  element={<ConcertList/>} />
        <Route path="/admin/concertsignup"  element={<ConcertAdd/>} />
        <Route path="/admin/concertlist/edit/:id"  element={<ConcertEdit/>} />
        <Route path="/admin/concertlist/:id"  element={<ConcertView/>} />
      </Routes>
    </BrowserRouter>
  );
}
