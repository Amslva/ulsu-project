import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getCurrentUser, logout, changeAvatar } from '../services/api';
import Layout from '../components/Layout';

export default function ProfilePage() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [avatarLoading, setAvatarLoading] = useState(false);

  useEffect(() => {
    loadUserProfile();
  }, []);

  const loadUserProfile = async () => {
    try {
      const userData = await getCurrentUser();
      setUser(userData);
    } catch (err) {
      setError('Ошибка загрузки профиля');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    setUser(null);
    window.location.href = '/';
  };

  const handleAvatarChange = async (avatarType) => {
  setAvatarLoading(true);
  setError(''); // Очищаем предыдущие ошибки
  try {
    const result = await changeAvatar(avatarType);
    
    // Обновляем данные пользователя
    const userData = await getCurrentUser();
    setUser(userData);
    
    // Убираем alert - слишком навязчиво
    console.log('Аватарка изменена:', result.message);
    
  } catch (err) {
    setError(err.message || 'Ошибка при смене аватарки');
    console.error('Ошибка смены аватарки:', err);
  } finally {
    setAvatarLoading(false);
  }
};

  if (loading) return <Layout showSidebar={false}><div className="loading">Загрузка...</div></Layout>;
  if (error) return <Layout showSidebar={false}><div className="error">{error}</div></Layout>;
  if (!user) return <Layout showSidebar={false}><div className="error">Пользователь не найден</div></Layout>;

  return (
    <Layout showSidebar={false}>
      <div className="profile-container">
        <h1>Личный кабинет</h1>
        
        <div className="profile-header">
          <div className="avatar-section">
            <div className="avatar-preview">
              <img 
                src={user.avatar_url || '/avatars/men.png'} 
                alt="Аватар" 
                className="avatar-image"
              />
              {avatarLoading && <div className="avatar-loading">Загрузка...</div>}
            </div>
            <h2>Приветствую, {user.username}!</h2>
          </div>
          <p>Добро пожаловать в ваш личный кабинет</p>
        </div>

        <div className="avatar-selection">
          <h3>Выберите аватарку</h3>
          
          <div className="default-avatars">
            <div className="avatar-grid">
              {['men', 'girl'].map(type => (
                <div 
                  key={type}
                  className={`avatar-option ${user.avatar_url?.includes(type) ? 'selected' : ''}`}
                  onClick={() => handleAvatarChange(type)}
                >
                  <img 
                    src={`/avatars/${type}.png`} 
                    alt={`Аватар ${type}`}
                  />
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="profile-info">
          <h3>Основная информация</h3>
          <div className="info-item">
            <label>Ваше имя:</label>
            <input 
              type="text" 
              value={user.first_name || ''} 
              placeholder="Введите ваше имя"
              className="form-input"
            />
          </div>
          <div className="info-item">
            <label>Email:</label>
            <input 
              type="email" 
              value={user.email || ''} 
              disabled 
              className="form-input"
            />
            <span className="hint">(нельзя изменить)</span>
          </div>
          <div className="info-item">
            <label>Имя пользователя:</label>
            <input 
              type="text" 
              value={user.username || ''} 
              disabled 
              className="form-input"
            />
          </div>
        </div>

        <div className="profile-actions">
          <h3>Действия</h3>
          <div className="action-buttons">
            <Link to="/change-password" className="btn btn-primary">
              Сменить пароль
            </Link>
            <Link to="/select-direction" className="btn btn-secondary">
              Выбрать направление →
            </Link>
            <button onClick={handleLogout} className="btn btn-danger">
              Выйти из аккаунта
            </button>
          </div>
        </div>

        <div className="profile-footer">
          <Link to="/">← Назад к главной</Link>
        </div>
      </div>
    </Layout>
  );
}