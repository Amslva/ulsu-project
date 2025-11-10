import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { register } from '../services/api';
import Layout from '../components/Layout';

export default function RegisterPage() {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    password_confirm: ''
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

    if (formData.password !== formData.password_confirm) {
      setError('Пароли не совпадают');
      setLoading(false);
      return;
    }

    try {
      await register(formData.username, formData.email, formData.password);
      navigate('/login', { 
        state: { message: 'Регистрация успешна! Теперь вы можете войти.' }
      });
    } catch (err) {
      setError(err.message || 'Ошибка регистрации');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      <h1>Регистрация</h1>
      
      {error && (
        <div className="form-error">
          <p>{error}</p>
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <p>
          <label className="form-label" htmlFor="username">Имя пользователя:</label>
          <input
            type="text"
            id="username"
            name="username"
            className="form-input"
            value={formData.username}
            onChange={handleChange}
            required
          />
        </p>

        <p>
          <label className="form-label" htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            name="email"
            className="form-input"
            value={formData.email}
            onChange={handleChange}
            required
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
          />
        </p>

        <p>
          <label className="form-label" htmlFor="password_confirm">Подтвердите пароль:</label>
          <input
            type="password"
            id="password_confirm"
            name="password_confirm"
            className="form-input"
            value={formData.password_confirm}
            onChange={handleChange}
            required
          />
        </p>

        <p>
          <button type="submit" className="form-button" disabled={loading}>
            {loading ? 'Регистрация...' : 'Зарегистрироваться'}
          </button>
        </p>
      </form>

      <p>
        <Link to="/login">Уже есть аккаунт? Войти</Link>
      </p>
      <p>
        <Link to="/">← Назад к главной</Link>
      </p>
    </Layout>
  );
}
