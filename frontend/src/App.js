import logo from './logo.svg';
import './App.css';
import Home from './pages/Home';
import ConcertList from './pages/ConcertList';
import ConcertDetail from './pages/ConcertDetail';
import Reserved from './pages/Reserved';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />}/>
        <Route path="/concerts" element={<ConcertList />}/>
        <Route path="/concerts/:id" element={<ConcertDetail />}/>
        <Route path="/reserved" element={<Reserved />}/>
      </Routes>
    </Router>

  );
}

export default App;
