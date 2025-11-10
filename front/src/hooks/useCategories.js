import { fetchCategories } from '../services/api';
import { useData } from './useData';

export const useCategories = () => {
  return useData(fetchCategories);
};