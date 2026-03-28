import { Activity, Droplets, Footprints, Heart, Moon, Timer, TrendingUp, Wind } from 'lucide-react';
import AgeComparison from '../components/AgeComparison';
import MetricCard from '../components/MetricCard';
import ReminderCards from '../components/ReminderCards';
import SpecialistCards from '../components/SpecialistCards';
import StepProgressRing from '../components/StepProgressRing';
import SubSystemAges from '../components/SubSystemAges';
import WorkoutSummary from '../components/WorkoutSummary';
import ActivityNudge from '../components/ActivityNudge';
import useStore from '../store';

export default function Dashboard() {
  const { dashboard } = useStore();
  if (!dashboard) {
    return <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">{Array.from({ length: 8 }).map((_, index) => <div key={index} className="bg-slate-200 animate-pulse rounded-xl h-32" />)}</div>;
  }
  if (!dashboard.profile) {
    return <div className="text-center text-slate-500 py-16">No health data yet. Go to Data Ingest to add your first data.</div>;
  }
  const metrics = dashboard.metrics || {};
  const metricCards = [
    ['Resting HR', metrics.resting_hr, 'bpm', Heart, metrics.resting_hr < 70 ? 'good' : 'warning'],
    ['HRV', metrics.hrv, 'ms', Activity, metrics.hrv > 40 ? 'good' : 'warning'],
    ['Steps', metrics.steps, 'steps', Footprints, metrics.steps > 7500 ? 'good' : 'warning'],
    ['Sleep', metrics.sleep, 'hours', Moon, metrics.sleep >= 7 ? 'good' : 'warning'],
    ['VO2max', metrics.vo2max, 'mL/kg/min', Wind, metrics.vo2max > 40 ? 'good' : 'warning'],
    ['SpO2', metrics.spo2, '%', Droplets, metrics.spo2 > 95 ? 'good' : 'warning'],
    ['Exercise Minutes', metrics.exercise_min, 'min', Timer, metrics.exercise_min > 30 ? 'good' : 'warning'],
    ['Flights Climbed', metrics.flights, 'flights', TrendingUp, 'neutral']
  ];

  return (
    <div>
      <ReminderCards />
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        <AgeComparison />
        <div className="lg:col-span-2"><SubSystemAges /></div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {metricCards.map(([label, value, unit, icon, status]) => <MetricCard key={label} label={label} value={value} unit={unit} icon={icon} status={status} />)}
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        <StepProgressRing current={dashboard.metrics.steps || 0} goal={dashboard.step_goal || 7500} size={200} />
        <div className="lg:col-span-2 space-y-6">
          <WorkoutSummary summary={dashboard.workout_summary} />
          <ActivityNudge currentSteps={dashboard.metrics.steps || 0} stepGoal={dashboard.step_goal || 7500} message={dashboard.activity_nudge?.message} />
        </div>
      </div>
      <SpecialistCards />
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 mt-6">
        <div className="text-sm text-slate-600 italic">{dashboard.cross_domain_insight}</div>
      </div>
    </div>
  );
}
