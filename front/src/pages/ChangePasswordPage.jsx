import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { changePassword } from '../services/api';
import Layout from '../components/Layout';

export default function ChangePasswordPage() {
  const [formData, setFormData] = useState({
    current_password: '',
    new_password: '',
    confirm_password: ''
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
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
    setSuccess('');

    if (formData.new_password !== formData.confirm_password) {
      setError('Новые пароли не совпадают');
      setLoading(false);
      return;
    }

    try {
      await changePassword(
        formData.current_password, 
        formData.new_password, 
        formData.confirm_password
      );
      setSuccess('Пароль успешно изменен!');
      setFormData({
        current_password: '',
        new_password: '',
        confirm_password: ''
      });
      
      // Перенаправляем через 2 секунды
      setTimeout(() => {
        navigate('/');
      }, 2000);
      
    } catch (err) {
      setError(err.message || 'Ошибка при смене пароля');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      <div className="change-password-container">
        <h1>Смена пароля</h1>
        
        {error && (
          <div className="form-error">
            <p>{error}</p>
          </div>
        )}

        {success && (
          <div className="form-success">
            <p>{success}</p>
            <p>Перенаправление на главную страницу...</p>
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <p>
            <label className="form-label" htmlFor="current_password">Текущий пароль:</label>
            <input
              type="password"
              id="current_password"
              name="current_password"
              className="form-input"
              value={formData.current_password}
              onChange={handleChange}
              required
              disabled={loading || success}
            />
          </p>

          <p>
            <label className="form-label" htmlFor="new_password">Новый пароль:</label>
            <input
              type="password"
              id="new_password"
              name="new_password"
              className="form-input"
              value={formData.new_password}
              onChange={handleChange}
              required
              disabled={loading || success}
            />
          </p>

          <p>
            <label className="form-label" htmlFor="confirm_password">Подтвердите новый пароль:</label>
            <input
              type="password"
              id="confirm_password"
              name="confirm_password"
              className="form-input"
              value={formData.confirm_password}
              onChange={handleChange}
              required
              disabled={loading || success}
            />
          </p>

          <p>
            <button 
              type="submit" 
              className="form-button" 
              disabled={loading || success}
            >
              {loading ? 'Смена пароля...' : 'Сменить пароль'}
            </button>
          </p>
        </form>

        <p>
          <Link to="/">← Назад к главной</Link>
        </p>
      </div>
    </Layout>
  );
}