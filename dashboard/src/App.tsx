import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import JobDetails from './pages/JobDetails';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<JobDetails />} />
          <Route path="/jobs/:jobId" element={<JobDetails />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;