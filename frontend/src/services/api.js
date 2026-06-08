import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
});

export const playMove = async (board, player, difficulty, size) => {
  const response = await api.post('/play', { board, player, difficulty, size });
  return response.data;
};

export const saveMatchHistory = async (matchData) => {
  const response = await api.post('/history', matchData);
  return response.data;
};

export const getMatchHistory = async () => {
  const response = await api.get('/history');
  return response.data;
};
