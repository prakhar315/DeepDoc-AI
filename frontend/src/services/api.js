import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
});

export const searchDocuments = (payload) => api.post('/search', payload);

export const uploadText = (payload) => api.post('/upload', payload);

export const uploadFile = (file, department, title) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('department', department);
  formData.append('title', title);
  return api.post('/upload-file', formData);
};

export const getFullDocument = (docId) =>
  api.get(`/document/full/doc_id/${encodeURIComponent(docId)}`);

export const deleteDocument = (docId) =>
  api.delete(`/delete/doc_id/${encodeURIComponent(docId)}`);

export const getHealth = () => api.get('/health');
