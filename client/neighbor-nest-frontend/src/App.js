import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Home from './components/Home';
import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './components/Dashboard';
import EventDetail from './components/EventDetail';
import Events from './components/Events';
import Navbar from './components/Navbar';
import NeighborhoodDetail from './components/NeighborhoodDetail';
import Neighborhoods from './components/Neighborhoods';
import News from './components/News';
import NewsDetail from './components/NewsDetail';
import UserDetail from './components/UserDetail';
import Users from './components/Users';
import './App.css'
import NotFound from './pages/NotFound';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/events" element={<Events />} />
          <Route path="/events/:event_id" element={<EventDetail />} />
          <Route path="/neighborhoods" element={<Neighborhoods />} />
          <Route path="/neighborhoods/:neighborhood_id" element={<NeighborhoodDetail />} />
          <Route path="/news" element={<News />} />
          <Route path="/news/:news_id" element={<NewsDetail />} />
          <Route path="/users" element={<Users />} />
          <Route path="/users/:user_id" element={<UserDetail />} />
          <Route path="/navbar" element={<Navbar />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
