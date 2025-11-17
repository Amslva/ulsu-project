import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { logout, getCurrentUser } from '../services/api';
import '../styles/Layout.css';

export default function Layout({ children, categories = [] }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    const token = localStorage.getItem('access_token');
    if (token) {
      try {
        const userData = await getCurrentUser();
        setUser(userData);
      } catch (error) {
        console.error('Auth error:', error);
        localStorage.removeItem('access_token');
      }
    }
    setLoading(false);
  };

  const handleLogout = () => {
    logout();
    setUser(null);
    window.location.href = '/';
  };

  const getUserName = () => {
    if (!user) return 'Пользователь';
    return user.first_name || user.last_name
      ? `${user.first_name || ''} ${user.last_name || ''}`.trim()
      : user.username || 'Пользователь';
  };

  if (loading) {
    return (
      <div className="layout">
        <header className="header">
          <div className="nav">
            <Link to="/">Главная</Link>
            <Link to="/stats">Аналитика</Link>
            <span>Загрузка...</span>
          </div>
        </header>
        <div className="loading">Загрузка...</div>
      </div>
    );
  }

  return (
    <div className="layout">
      <header className="header">
        <div className="nav">
          <Link to="/">Главная</Link>
          <Link to="/stats">Аналитика</Link>

          <div className="user-info">
            {user ? (
              <>
                <span>Привет, {getUserName()}!</span>
                <button onClick={handleLogout} className="logout-btn">
                  Выйти
                </button>
              </>
            ) : (
              <>
                <Link to="/login">Войти</Link>
                <Link to="/register">Регистрация</Link>
              </>
            )}
          </div>
        </div>
      </header>

      <div className="main-content">
            <aside className="sidebar">
              <h3>Категории</h3>
              <nav>
                {categories && categories.map(cat => (
                  <Link
                    key={cat.id}
                    to={`/category/${cat.slug}`}
                    className="category-link"
                  >
                    {cat.name}
                  </Link>
                ))}
              </nav>
            </aside>

        <main className="content">
          {children}
        </main>
      </div>

      <footer className="footer">
        <p>&copy; 2025 JunItCompass</p>
      </footer>
    </div>
  );
}