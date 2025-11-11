import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import CategoryPage from './pages/CategoryPage';
import PostPage from './pages/PostPage';
import AnalyzePage from './pages/AnalyzePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import './styles/main.css';
import ChangePasswordPage from './pages/ChangePasswordPage';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/category/:catSlug" element={<CategoryPage />} />
          <Route path="/post/:slug" element={<PostPage />} />
          <Route path="/stats" element={<AnalyzePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/change-password" element={<ChangePasswordPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;