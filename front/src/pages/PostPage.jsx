import { useParams, Link } from 'react-router-dom';
import { useCategories } from '../hooks/useCategories';
import { useData } from '../hooks/useData';
import { fetchProfessions } from '../services/api';
import Layout from '../components/Layout';

export default function PostPage() {
  const { slug } = useParams();
  const { data: categories } = useCategories();
  const { data: professions, loading, error } = useData(fetchProfessions);

  const post = professions?.find(p => p.slug === slug);

  if (loading) return <Layout><div className="loading">Загрузка...</div></Layout>;
  if (error) return <Layout><div className="error">{error}</div></Layout>;
  if (!post) return <Layout><div className="error">Профессия не найдена</div></Layout>;

  return (
    <Layout categories={categories}>
      <h1>{post.title}</h1>
      <p><strong>Категория:</strong> {post.cat_name}</p>
      <p><Link to="/">← Назад к главной</Link></p>
    </Layout>
  );
}