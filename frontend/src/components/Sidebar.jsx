import { Activity, Apple, Brain, LayoutDashboard, Lightbulb, PersonStanding, Search, Settings as SettingsIcon, Sparkles, Trophy, Upload, Users } from 'lucide-react';
import { NavLink } from 'react-router-dom';

const items = [
  { to: '/', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/ingest', label: 'Data Ingest', icon: Upload },
  { to: '/insights', label: 'Insights', icon: Lightbulb },
  { to: '/mental', label: 'Mental Health', icon: Brain },
  { to: '/nutrition', label: 'Nutrition', icon: Apple },
  { to: '/future', label: 'Future Self', icon: Sparkles },
  { to: '/activity', label: 'Activity', icon: Activity },
  { to: '/posture', label: 'Posture', icon: PersonStanding },
  { to: '/gamification', label: 'Gamification', icon: Trophy },
  { to: '/transparency', label: 'Transparency', icon: Search }
];

const bottomItems = [
  { to: '/family', label: 'Family', icon: Users },
  { to: '/settings', label: 'Settings', icon: SettingsIcon }
];

function LinkItem({ to, label, icon: Icon }) {
  return (
    <NavLink
      to={to}
      className={({ isActive }) => `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-slate-300 hover:bg-slate-800 hover:text-white transition ${isActive ? 'bg-slate-800 text-white' : ''}`}
    >
      <Icon size={20} />
      <span>{label}</span>
    </NavLink>
  );
}

export default function Sidebar() {
  return (
    <aside className="fixed inset-y-0 left-0 w-64 bg-slate-900 text-white border-r border-slate-800 flex flex-col overflow-hidden">
      <div className="px-6 pt-6 pb-5 border-b border-slate-800 shrink-0">
        <img
          src="/eirview-brand.png"
          alt="EirView logo"
          className="w-44 h-auto rounded-2xl bg-white p-2 shadow-lg shadow-slate-950/30"
        />
        <div className="mt-4">
          <div className="text-2xl font-semibold tracking-tight text-white">EirView</div>
          <div className="mt-1 text-sm leading-snug text-slate-300">Your progress, in full focus.</div>
        </div>
      </div>
      <div className="flex-1 overflow-y-auto px-3 py-6">
        <nav className="space-y-1">
          {items.map((item) => <LinkItem key={item.to} {...item} />)}
        </nav>
        <div className="border-t border-slate-700 my-4" />
        <nav className="space-y-1 pb-6">
          {bottomItems.map((item) => <LinkItem key={item.to} {...item} />)}
        </nav>
      </div>
    </aside>
  );
}
