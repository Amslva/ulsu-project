import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { login } from '../services/api';
import Layout from '../components/Layout';

export default function LoginPage() {
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const data = await login(formData.username, formData.password);
      console.log('Login successful:', data);

      // Принудительно обновляем страницу чтобы Layout перезагрузился
      window.location.href = '/';

    } catch (err) {
      setError(err.message || 'Ошибка входа');
      setLoading(false);
    }
  };

  return (
    <Layout>
      <h1>Авторизация</h1>

      {error && (
        <div className="form-error">
          <p>{error}</p>
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <p>
          <label className="form-label" htmlFor="username">Username или Email:</label>
          <input
            type="text"
            id="username"
            name="username"
            className="form-input"
            value={formData.username}
            onChange={handleChange}
            required
            disabled={loading}
          />
        </p>

        <p>
          <label className="form-label" htmlFor="password">Пароль:</label>
          <input
            type="password"
            id="password"
            name="password"
            className="form-input"
            value={formData.password}
            onChange={handleChange}
            required
            disabled={loading}
          />
        </p>

        <p>
          <button
            type="submit"
            className="form-button"
            disabled={loading}
          >
            {loading ? 'Вход...' : 'Войти'}
          </button>
        </p>
      </form>

      <p>
        <Link to="/register">Нет аккаунта? Зарегистрироваться</Link>
      </p>
      <p>
        <Link to="/">← Назад к главной</Link>
      </p>
    </Layout>
  );
}