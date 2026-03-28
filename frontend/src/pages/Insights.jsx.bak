import HabitSliders from '../components/HabitSliders';
import RiskChart from '../components/RiskChart';
import WorkoutTargets from '../components/WorkoutTargets';
import useStore from '../store';

export default function Insights() {
  const { dashboard } = useStore();
  return (
    <div className="space-y-6">
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 border-l-4 border-l-emerald-500 text-sm text-slate-600 italic leading-relaxed">
        {dashboard?.narrative || 'Complete your profile to get a personalized health narrative.'}
      </div>
      <HabitSliders />
      <RiskChart data={dashboard?.risk_projections || []} />
      <WorkoutTargets data={dashboard?.workout_targets} />
    </div>
  );
}
