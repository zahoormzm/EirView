import { useEffect, useState } from 'react';
import { getWorkouts, getWorkoutSummary, getWorkoutTargets, logWorkout } from '../api';
import ActivityNudge from '../components/ActivityNudge';
import StepProgressRing from '../components/StepProgressRing';
import WorkoutLog from '../components/WorkoutLog';
import WorkoutSummary from '../components/WorkoutSummary';
import WorkoutTargets from '../components/WorkoutTargets';
import useStore from '../store';

export default function ActivityPage() {
  const { selectedUserId, dashboard, showToast } = useStore();
  const [workouts, setWorkouts] = useState([]);
  const [summary, setSummary] = useState(dashboard?.workout_summary);
  const [targets, setTargets] = useState(dashboard?.workout_targets);
  const [form, setForm] = useState({ type: 'Running', duration_min: 30, calories: '' });

  const load = async () => {
    try {
      const [workoutsResponse, summaryResponse, targetsResponse] = await Promise.all([
        getWorkouts(selectedUserId),
        getWorkoutSummary(selectedUserId),
        getWorkoutTargets(selectedUserId)
      ]);
      setWorkouts(workoutsResponse.data);
      setSummary(summaryResponse.data);
      setTargets(targetsResponse.data);
    } catch (error) {
      showToast(error.message, 'error');
    }
  };

  useEffect(() => { load(); }, [selectedUserId]);

  const submit = async () => {
    try {
      await logWorkout(selectedUserId, { ...form, type: form.type.toLowerCase().replace(' ', '_') });
      await load();
      showToast('Workout logged');
    } catch (error) {
      showToast(error.message, 'error');
    }
  };

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <StepProgressRing current={dashboard?.metrics?.steps || 0} goal={dashboard?.step_goal || 7500} size={200} />
        <div className="lg:col-span-2"><WorkoutSummary summary={summary} /></div>
      </div>
      <WorkoutTargets data={targets} />
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <select value={form.type} onChange={(event) => setForm({ ...form, type: event.target.value })} className="border border-slate-300 rounded-lg px-3 py-2 text-sm">
            {['Running', 'Walking', 'Cycling', 'Swimming', 'Yoga', 'Strength Training', 'HIIT', 'Other'].map((option) => <option key={option}>{option}</option>)}
          </select>
          <input type="number" value={form.duration_min} onChange={(event) => setForm({ ...form, duration_min: Number(event.target.value) })} placeholder="Duration" className="border border-slate-300 rounded-lg px-3 py-2 text-sm" />
          <input type="number" value={form.calories} onChange={(event) => setForm({ ...form, calories: Number(event.target.value) })} placeholder="Calories" className="border border-slate-300 rounded-lg px-3 py-2 text-sm" />
          <button onClick={submit} className="bg-emerald-500 hover:bg-emerald-600 text-white rounded-lg px-4 py-2 font-medium transition">Log Workout</button>
        </div>
      </div>
      <WorkoutLog workouts={workouts} />
      <ActivityNudge currentSteps={dashboard?.metrics?.steps || 0} stepGoal={dashboard?.step_goal || 7500} />
    </div>
  );
}
