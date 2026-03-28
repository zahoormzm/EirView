import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { useEffect } from 'react';
import Sidebar from './components/Sidebar';
import TopBar from './components/TopBar';
import AlertBanner from './components/AlertBanner';
import Dashboard from './pages/Dashboard';
import DataIngest from './pages/DataIngest';
import Insights from './pages/Insights';
import Mental from './pages/Mental';
import Nutrition from './pages/Nutrition';
import FutureSelf from './pages/FutureSelf';
import Activity from './pages/Activity';
import Gamification from './pages/Gamification';
import Transparency from './pages/Transparency';
import Family from './pages/Family';
import Settings from './pages/Settings';
import SpotifyCallback from './pages/SpotifyCallback';
import useStore from './store';
import { getAlerts, getDashboard, getGamification, getProfile, getUsers } from './api';

export default function App() {
  const {
    selectedUserId,
    setUsers,
    setDashboard,
    setGamification,
    setAlerts,
    setProfile,
    toast,
    showToast
  } = useStore();

  useEffect(() => {
    (async () => {
      try {
        const response = await getUsers();
        setUsers(Array.isArray(response.data) ? response.data : response.data.users || []);
      } catch (error) {
        showToast(error.message, 'error');
      }
    })();
  }, [setUsers, showToast]);

  useEffect(() => {
    if (!selectedUserId) return;
    (async () => {
      try {
        const [dashboardResponse, gamificationResponse, alertsResponse, profileResponse] = await Promise.all([
          getDashboard(selectedUserId),
          getGamification(selectedUserId),
          getAlerts(selectedUserId),
          getProfile(selectedUserId)
        ]);
        setDashboard(dashboardResponse.data);
        setGamification(gamificationResponse.data);
        setAlerts(alertsResponse.data);
        setProfile(profileResponse.data);
      } catch (error) {
        showToast(error.message, 'error');
      }
    })();
  }, [selectedUserId, setAlerts, setDashboard, setGamification, setProfile, showToast]);

  return (
    <BrowserRouter>
      <div className="flex min-h-screen bg-slate-50">
        <Sidebar />
        <div className="flex-1 ml-64">
          <TopBar />
          <AlertBanner />
          <main className="max-w-7xl mx-auto px-6 py-6">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/ingest" element={<DataIngest />} />
              <Route path="/insights" element={<Insights />} />
              <Route path="/mental" element={<Mental />} />
              <Route path="/nutrition" element={<Nutrition />} />
              <Route path="/future" element={<FutureSelf />} />
              <Route path="/activity" element={<Activity />} />
              <Route path="/gamification" element={<Gamification />} />
              <Route path="/transparency" element={<Transparency />} />
              <Route path="/family" element={<Family />} />
              <Route path="/settings" element={<Settings />} />
              <Route path="/callback" element={<SpotifyCallback />} />
              <Route path="*" element={<Dashboard />} />
            </Routes>
          </main>
        </div>
        {toast && (
          <div className={`fixed top-4 right-4 z-50 px-4 py-3 rounded-lg shadow-lg text-white text-sm font-medium transition-all ${
            toast.type === 'success' ? 'bg-emerald-500' :
            toast.type === 'error' ? 'bg-red-500' :
            toast.type === 'warning' ? 'bg-amber-500' : 'bg-blue-500'
          }`}>
            {toast.message}
          </div>
        )}
      </div>
    </BrowserRouter>
  );
}
