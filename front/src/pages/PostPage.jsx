import { useParams, Link } from 'react-router-dom';
import { useCategories } from '../hooks/useCategories';
import { useData } from '../hooks/useData';
import { fetchProfessionBySlug } from '../services/api';  // ← Импортируем новый endpoint
import Layout from '../components/Layout';

export default function PostPage() {
  const { slug } = useParams();
  const { data: categories } = useCategories();
  
  // Используем новый endpoint для получения одной профессии
  const { data: post, loading, error } = useData(() => fetchProfessionBySlug(slug));

  if (loading) return <Layout><div className="loading">Загрузка...</div></Layout>;
  if (error) return <Layout><div className="error">{error}</div></Layout>;
  if (!post) return <Layout><div className="error">Профессия не найдена</div></Layout>;

  return (
    <Layout categories={categories}>
      <article className="profession-detail">
        <h1>{post.title}</h1>
        
        <div className="profession-meta">
          <p><strong>Категория:</strong> {post.cat_name}</p>
        </div>

        <div className="profession-content">
          <h2>Описание профессии</h2>
          <p>{post.content}</p>  {/* ← ВОТ КОНТЕНТ! */}
        </div>

        <div className="profession-footer">
          <Link to="/" className="back-link">← Назад к главной</Link>
        </div>
      </article>
    </Layout>
  );
}