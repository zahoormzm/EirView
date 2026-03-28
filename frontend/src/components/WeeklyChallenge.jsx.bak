import { Target } from 'lucide-react';

export default function WeeklyChallenge({ name, description, current, target }) {
  const pct = target ? (current / target) * 100 : 0;
  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
      <div className="flex items-center gap-2 font-medium text-slate-700"><Target className="text-amber-500" size={18} /> {name}</div>
      <div className="text-sm text-slate-500 mt-2">{description}</div>
      <div className="h-3 bg-slate-100 rounded-full mt-3">
        <div className="h-3 bg-amber-500 rounded-full" style={{ width: `${Math.min(pct, 100)}%` }} />
      </div>
      <div className="text-sm text-slate-600 mt-2">{current}/{target} days</div>
    </div>
  );
}
