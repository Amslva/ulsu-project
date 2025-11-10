import { useState, useEffect } from 'react';

export const useData = (fetchFunction, dependencies = []) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        setError(null);
        const result = await fetchFunction();
        setData(result);
      } catch (err) {
        if (err.message.includes('Failed to fetch')) {
          setError('Проблемы с соединением. Проверьте интернет.');
        } else {
          setError(err.message);
        }
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, dependencies);

  return { data, loading, error };
};