import { Link } from 'react-router-dom';
import { useCategories } from '../hooks/useCategories';
import { useData } from '../hooks/useData';
import { fetchAnalytics } from '../services/api';
import Layout from '../components/Layout';

export default function AnalyzePage() {
  const { data: categories, loading: categoriesLoading, error: categoriesError } = useCategories();
  const { data: analytics, loading: analyticsLoading, error: analyticsError } = useData(fetchAnalytics);

  const loading = categoriesLoading || analyticsLoading;
  const error = categoriesError || analyticsError;

  if (loading) return <Layout categories={[]}><div className="loading">Загрузка аналитики...</div></Layout>;
  if (error) return <Layout categories={[]}><div className="error">{error}</div></Layout>;

  return (
    <Layout categories={categories || []}>
      <h1>Аналитика</h1>

      <section>
        <h2>Топ языков программирования</h2>
        <div className="stats-list">
          {analytics?.top_languages?.map(item => (
            <div key={item.name} className="stat-item">
              <strong>{item.name}</strong>: {item.count} вакансий
            </div>
          ))}
        </div>
      </section>

      <section>
        <h2>Backend фреймворки</h2>
        <div className="stats-list">
          {analytics?.backend_frameworks?.map(item => (
            <div key={item.name} className="stat-item">
              <strong>{item.name}</strong>: {item.count} вакансий
            </div>
          ))}
        </div>
      </section>

      <p><Link to="/">← Назад к главной</Link></p>
    </Layout>
  );
}