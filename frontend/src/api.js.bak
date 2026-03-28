import axios from 'axios';

const API = axios.create({ baseURL: 'http://localhost:8000' });

export const getUsers = () => API.get('/api/users');
export const createUser = (data) => API.post('/api/users', data);
export const getProfile = (userId) => API.get(`/api/profile/${userId}`);
export const updateProfile = (userId, data) => API.put(`/api/profile/${userId}`, data);
export const getDashboard = (userId) => API.get(`/api/dashboard/${userId}`);
export const uploadFile = (formData) => API.post('/api/ingest', formData, { headers: { 'Content-Type': 'multipart/form-data' } });
export const uploadFaceAge = (formData) => API.post('/api/face-age', formData, { headers: { 'Content-Type': 'multipart/form-data' } });
export const uploadAppleHealth = (formData) => API.post('/api/apple-health', formData, { headers: { 'Content-Type': 'multipart/form-data' } });
export const uploadMeal = (payload) => {
  if (payload instanceof FormData) {
    return API.post('/api/meal', payload, { headers: { 'Content-Type': 'multipart/form-data' } });
  }
  return API.post('/api/meal', payload);
};
export const logWater = (userId, amount_ml) => API.post('/api/water', { user_id: userId, amount_ml });
export const simulate = (userId, changes) => API.post('/api/simulate', { user_id: userId, changes });
export const getGamification = (userId) => API.get(`/api/gamification/${userId}`);
export const logAction = (userId, action) => API.post(`/api/gamification/${userId}/action`, { action });
export const getLeaderboard = () => API.get('/api/gamification/leaderboard');
export const createFamily = (name, userId) => API.post('/api/family', { name, created_by: userId });
export const joinFamily = (joinCode, userId, relationship, privacy) => API.post('/api/family/join', { join_code: joinCode, user_id: userId, relationship, privacy_level: privacy });
export const getFamily = (familyId) => API.get(`/api/family/${familyId}`);
export const getReminders = (userId) => API.get(`/api/reminders/${userId}`);
export const getAlerts = (userId) => API.get(`/api/alerts/${userId}`);
export const notifyDoctor = (userId, alertId) => API.post(`/api/alerts/${userId}/notify-doctor`, { alert_id: alertId });
export const getSpecialists = (userId) => API.get(`/api/specialists/${userId}`);
export const getWorkouts = (userId) => API.get(`/api/workouts/${userId}`);
export const logWorkout = (userId, data) => API.post(`/api/workouts/${userId}`, data);
export const getWorkoutSummary = (userId) => API.get(`/api/workouts/${userId}/summary`);
export const getWorkoutTargets = (userId) => API.get(`/api/workouts/${userId}/targets`);
export const getTransparency = (userId) => API.get(`/api/transparency/${userId}`);

export const streamChat = async (endpoint, userId, message, history, onText, onTool, onDone) => {
  const response = await fetch(`http://localhost:8000/api/chat/${endpoint}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id: userId, message, history })
  });

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    const lines = decoder.decode(value).split('\n');
    for (const line of lines) {
      if (!line.startsWith('data: ')) continue;
      try {
        const data = JSON.parse(line.slice(6));
        if (data.type === 'text') onText(data.content);
        else if (data.type === 'tool') onTool(data);
        else if (data.type === 'done') onDone();
      } catch {
        // ignore malformed chunks
      }
    }
  }
};
