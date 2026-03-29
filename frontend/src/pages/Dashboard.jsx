import { Activity, CloudSun, Droplets, Footprints, Heart, Moon, ShieldAlert, Timer, TrendingUp, Wind } from 'lucide-react';
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
    <div className="space-y-4">
      <ReminderCards compact />
      <div className="grid grid-cols-1 xl:grid-cols-12 gap-4">
        <div className="xl:col-span-3">
          <AgeComparison compact />
        </div>
        <div className="xl:col-span-5">
          <SubSystemAges compact />
        </div>
        <div className="xl:col-span-4 space-y-4">
          <StepProgressRing current={dashboard.metrics.steps || 0} goal={dashboard.step_goal || 7500} size={150} compact />
          <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-4">
            <div className="flex items-center justify-between gap-3">
              <div className="flex items-center gap-2 text-sm font-semibold text-slate-900">
                <CloudSun size={16} className="text-sky-600" />
                Outdoor Conditions
              </div>
              <div className={`text-[11px] font-semibold uppercase tracking-wide ${dashboard.weather?.outdoor_ok ? 'text-emerald-700' : 'text-amber-700'}`}>
                {dashboard.weather?.label || 'Conditions unavailable'}
              </div>
            </div>
            <div className="grid grid-cols-3 gap-3 mt-4 text-center">
              <div className="rounded-lg bg-slate-50 border border-slate-200 py-2">
                <div className="text-[11px] uppercase tracking-wide text-slate-500">Temp</div>
                <div className="text-sm font-semibold text-slate-900 mt-1">{dashboard.weather?.temp_c != null ? `${Math.round(dashboard.weather.temp_c)}°C` : '—'}</div>
              </div>
              <div className="rounded-lg bg-slate-50 border border-slate-200 py-2">
                <div className="text-[11px] uppercase tracking-wide text-slate-500">AQI</div>
                <div className="text-sm font-semibold text-slate-900 mt-1">{dashboard.weather?.aqi ?? '—'}</div>
              </div>
              <div className="rounded-lg bg-slate-50 border border-slate-200 py-2">
                <div className="text-[11px] uppercase tracking-wide text-slate-500">UV</div>
                <div className="text-sm font-semibold text-slate-900 mt-1">{dashboard.weather?.uv_index != null ? Math.round(dashboard.weather.uv_index) : '—'}</div>
              </div>
            </div>
            <div className="mt-3 text-sm text-slate-700">{dashboard.weather?.summary || dashboard.weather?.description || 'Weather context unavailable.'}</div>
            {dashboard.weather?.note && (
              <div className="mt-2 inline-flex items-start gap-2 text-xs text-slate-500">
                <ShieldAlert size={13} className="mt-0.5 text-slate-400" />
                <span>{dashboard.weather.note}</span>
              </div>
            )}
          </div>
          <ActivityNudge currentSteps={dashboard.metrics.steps || 0} stepGoal={dashboard.step_goal || 7500} nudge={dashboard.activity_nudge} compact />
        </div>
      </div>
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
        {metricCards.map(([label, value, unit, icon, status]) => <MetricCard key={label} label={label} value={value} unit={unit} icon={icon} status={status} compact />)}
      </div>
      <div className="grid grid-cols-1 xl:grid-cols-12 gap-4">
        <div className="xl:col-span-7">
          <WorkoutSummary summary={dashboard.workout_summary} compact />
        </div>
        <div className="xl:col-span-5">
          <SpecialistCards compact />
        </div>
      </div>
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-4">
        <div className="text-xs font-semibold uppercase tracking-wide text-slate-500 mb-2">Cross-domain insight</div>
        <div className="text-sm text-slate-600 italic">{dashboard.cross_domain_insight}</div>
      </div>
    </div>
  );
}
