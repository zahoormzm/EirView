import { Bell } from 'lucide-react';
import { useLocation } from 'react-router-dom';
import useStore from '../store';
import StreakBadge from './StreakBadge';
import UserSelector from './UserSelector';

const titles = {
  '/': 'Dashboard',
  '/ingest': 'Data Ingest',
  '/insights': 'Insights',
  '/mental': 'Mental Health',
  '/nutrition': 'Nutrition',
  '/future': 'Future Self',
  '/activity': 'Activity',
  '/gamification': 'Gamification',
  '/transparency': 'Transparency',
  '/family': 'Family',
  '/settings': 'Settings'
};

export default function TopBar() {
  const location = useLocation();
  const { alerts } = useStore();

  return (
    <header className="bg-white border-b border-slate-200 px-6 py-3 flex justify-between items-center sticky top-0 z-20">
      <div>
        <h1 className="text-lg font-semibold text-slate-900">{titles[location.pathname] || 'EirView'}</h1>
        <p className="text-sm text-slate-500">EirView. Your progress, in full focus.</p>
      </div>
      <div className="flex items-center gap-4">
        <UserSelector />
        <StreakBadge />
        <button className="relative text-slate-400 hover:text-slate-600">
          <Bell size={18} />
          {alerts?.length > 0 && <span className="absolute -top-1 -right-1 h-2.5 w-2.5 rounded-full bg-red-500" />}
        </button>
      </div>
    </header>
  );
}
