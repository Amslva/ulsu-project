import { useParams, Link } from 'react-router-dom';
import { useCategories } from '../hooks/useCategories';
import { useData } from '../hooks/useData';
import { fetchProfessionsByCategory } from '../services/api';
import Layout from '../components/Layout';

export default function CategoryPage() {
  const { catSlug } = useParams();
  const { data: categories } = useCategories();

  const category = categories?.find(c => c.slug === catSlug);
  const { data: professions, loading, error } = useData(
    () => fetchProfessionsByCategory(category?.id),
    [category?.id]
  );

  if (loading) return <Layout><div className="loading">Загрузка...</div></Layout>;
  if (error) return <Layout><div className="error">{error}</div></Layout>;
  if (!category) return <Layout><div className="error">Категория не найдена</div></Layout>;

  return (
    <Layout categories={categories}>
      <h1>Категория: {category.name}</h1>

      {!professions || professions.length === 0 ? (
        <p>В этой категории пока нет профессий</p>
      ) : (
        <div className="professions-list">
          {professions.map(prof => (
            <div key={prof.id} className="profession-card">
              <h3>{prof.title}</h3>
              <Link to={`/post/${prof.slug}`} className="btn">
                Изучить
              </Link>
            </div>
          ))}
        </div>
      )}

      <p><Link to="/">← Назад к главной</Link></p>
    </Layout>
  );
}