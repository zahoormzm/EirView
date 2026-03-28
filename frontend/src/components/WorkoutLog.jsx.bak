import { Activity, Dumbbell, Heart, PersonStanding } from 'lucide-react';

const icons = {
  running: PersonStanding,
  walking: Activity,
  cycling: Activity,
  swimming: Activity,
  yoga: Heart,
  strength_training: Dumbbell,
  weight_training: Dumbbell
};

export default function WorkoutLog({ workouts = [] }) {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
      {workouts.length ? workouts.map((workout) => {
        const Icon = icons[workout.type] || Activity;
        const impact = [workout.cv_impact, workout.msk_impact, workout.met_impact, workout.neuro_impact].filter(Boolean)[0];
        return (
          <div key={workout.id} className="py-4 border-b border-slate-100">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Icon size={18} className="text-slate-500" />
                <span className="font-medium text-slate-700">{workout.type}</span>
                <span className="text-xs text-slate-400 ml-2">{workout.date}</span>
              </div>
              <div className="text-sm text-slate-500">{workout.duration_min} min · {workout.calories || 0} cal</div>
            </div>
            <div className="text-xs text-emerald-600 mt-1">Impact: {impact ? `${impact} years` : 'steady maintenance'}</div>
          </div>
        );
      }) : <div className="text-sm text-slate-500">No workouts logged yet.</div>}
    </div>
  );
}
