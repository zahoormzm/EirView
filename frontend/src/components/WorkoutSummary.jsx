import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';

export default function WorkoutSummary({ summary }) {
  if (!summary) {
    return <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 text-sm text-slate-500">Workout summary unavailable.</div>;
  }
  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
      <ResponsiveContainer width="100%" height={250}>
        <BarChart data={summary.chart || []}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="day" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="minutes" fill="#10b981" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
      <div className="text-sm text-slate-600 mt-3">{summary.total_sessions} sessions | {summary.total_minutes} total minutes | {summary.total_calories} calories burned this week</div>
    </div>
  );
}
