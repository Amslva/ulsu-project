import { API_BASE } from '../utils/constants';

export const changePassword = async (currentPassword, newPassword, confirmPassword) => {
  const response = await fetch(`${API_BASE}/auth/change-password/`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify({
      current_password: currentPassword,
      new_password: newPassword,
      confirm_password: confirmPassword
    }),
  });

  return handleResponse(response);
};

export const fetchProfessionBySlug = (slug) =>
  fetch(`${API_BASE}/professions/${slug}/`).then(handleResponse);

const handleResponse = async (response) => {
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.error || errorData.detail || `HTTP error! status: ${response.status}`);
  }
  return response.json();
};

export const getAuthHeaders = () => {
  const token = localStorage.getItem('access_token');
  return token ? {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  } : {};
};

export const storeTokens = (tokens) => {
  localStorage.setItem('access_token', tokens.access);
  localStorage.setItem('refresh_token', tokens.refresh);
};

export const clearTokens = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
};

export const fetchCategories = () =>
  fetch(`${API_BASE}/categories/`).then(handleResponse);

export const fetchProfessions = () =>
  fetch(`${API_BASE}/professions/`).then(handleResponse);

export const fetchProfessionsByCategory = (categoryId) =>
  fetch(`${API_BASE}/professions/category/${categoryId}/`).then(handleResponse);

export const fetchAnalytics = () =>
  fetch(`${API_BASE}/analytics/stats/`).then(handleResponse);

export const register = async (username, email, password) => {
  const response = await fetch(`${API_BASE}/auth/register/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username, email, password }),
  });

  const data = await handleResponse(response);

  if (data.tokens) {
    storeTokens(data.tokens);
  }

  return data;
};

export const login = async (username, password) => {
  const response = await fetch(`${API_BASE}/auth/login/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username, password }),
  });

  const data = await handleResponse(response);

  if (data.tokens) {
    storeTokens(data.tokens);
  }

  return data;
};

export const logout = async () => {
  const refreshToken = localStorage.getItem('refresh_token');

  if (refreshToken) {
    try {
      await fetch(`${API_BASE}/auth/logout/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh: refreshToken }),
      });
    } catch (error) {
      console.error('Logout error:', error);
    }
  }

  clearTokens();
};

export const getCurrentUser = () =>
  fetch(`${API_BASE}/auth/profile/`, {
    headers: getAuthHeaders()
  }).then(handleResponse);