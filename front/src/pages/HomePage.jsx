import { Link } from 'react-router-dom';
import { useCategories } from '../hooks/useCategories';
import { useData } from '../hooks/useData';
import { fetchProfessions } from '../services/api';
import Layout from '../components/Layout';

export default function HomePage() {
  const { data: professions, loading, error } = useData(fetchProfessions);
  const { data: categories } = useCategories();

  if (loading) return <Layout><div className="loading">Загрузка...</div></Layout>;
  if (error) return <Layout><div className="error">{error}</div></Layout>;

  return (
    <Layout categories={categories}>
      <h1>Карта IT-профессий</h1>

      {!professions || professions.length === 0 ? (
        <p>Пока нет профессий</p>
      ) : (
        <div className="professions-list">
          {professions.map(prof => (
            <div key={prof.id} className="profession-card">
              <h3>{prof.title}</h3>
              <p>Категория: {prof.cat_name}</p>
              <Link to={`/post/${prof.slug}`} className="btn">
                Изучить
              </Link>
            </div>
          ))}
        </div>
      )}
    </Layout>
  );
}