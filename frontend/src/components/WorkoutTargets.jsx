import { Dumbbell, Heart, PersonStanding } from 'lucide-react';

const icons = { running: PersonStanding, yoga: Heart, strength: Dumbbell, walking: PersonStanding, cycling: PersonStanding, weight_training: Dumbbell, hiit: Dumbbell };

export default function WorkoutTargets({ data }) {
  const sessions = data?.recommended_sessions || [];
  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
      {sessions.length ? sessions.map((session, index) => {
        const Icon = icons[session.type] || PersonStanding;
        return (
          <div key={`${session.type}-${index}`} className={`${index < sessions.length - 1 ? 'border-b border-slate-100' : ''} py-3`}>
            <div className="flex items-center gap-3">
              <Icon size={18} className="text-slate-500" />
              <div className="font-medium text-slate-700">{session.type}</div>
              <div className="text-sm text-slate-500">{session.frequency}</div>
            </div>
            <div className="text-xs text-slate-500 mt-2">{session.reason}</div>
          </div>
        );
      }) : <div className="text-sm text-slate-500">No workout targets available.</div>}
    </div>
  );
}
