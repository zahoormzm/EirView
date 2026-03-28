import { CartesianGrid, Legend, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';

export default function RiskChart({ data = [] }) {
  if (!data.length) {
    return <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 text-sm text-slate-500">No risk projection data yet.</div>;
  }
  const rows = data.map((item) => ({
    year: item.year,
    diabetes: (item.diabetes_risk || 0) * 100,
    cvd: (item.cvd_risk || 0) * 100,
    metabolic: (item.metabolic_risk || 0) * 100,
    mental: (item.mental_decline_risk || 0) * 100
  }));
  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
      <ResponsiveContainer width="100%" height={350}>
        <LineChart data={rows}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="year" label={{ value: 'Year', position: 'bottom' }} />
          <YAxis domain={[0, 50]} tickFormatter={(v) => `${v}%`} />
          <Tooltip formatter={(value) => `${Number(value).toFixed(1)}%`} />
          <Legend />
          <Line type="monotone" dataKey="diabetes" stroke="#3b82f6" strokeWidth={2} dot={{ r: 3 }} activeDot={{ r: 5 }} />
          <Line type="monotone" dataKey="cvd" stroke="#ef4444" strokeWidth={2} dot={{ r: 3 }} activeDot={{ r: 5 }} />
          <Line type="monotone" dataKey="metabolic" stroke="#f59e0b" strokeWidth={2} dot={{ r: 3 }} activeDot={{ r: 5 }} />
          <Line type="monotone" dataKey="mental" stroke="#8b5cf6" strokeWidth={2} dot={{ r: 3 }} activeDot={{ r: 5 }} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
