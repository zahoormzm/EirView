import AgentTrace from '../components/AgentTrace';
import useStore from '../store';
import { getTransparency } from '../api';
import { useEffect, useState } from 'react';

export default function Transparency() {
  const { selectedUserId, showToast } = useStore();
  const [data, setData] = useState(null);

  useEffect(() => {
    (async () => {
      try {
        const response = await getTransparency(selectedUserId);
        setData(response.data);
      } catch (error) {
        showToast(error.message, 'error');
      }
    })();
  }, [selectedUserId, showToast]);

  const cards = [
    ['Claude 4.6', data?.model_stats?.claude || {}, 'bg-blue-50 border-blue-200'],
    ['Gemini 2.5 Flash', data?.model_stats?.gemini || {}, 'bg-purple-50 border-purple-200'],
    ['Deterministic', data?.model_stats?.deterministic || {}, 'bg-slate-50 border-slate-200']
  ];

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {cards.map(([name, stats, classes]) => (
          <div key={name} className={`rounded-xl border p-6 ${classes}`}>
            <div className="font-semibold text-slate-900">{name}</div>
            <div className="text-sm text-slate-600 mt-2">Calls: {stats.calls || 0}</div>
            <div className="text-sm text-slate-600">Avg latency: {stats.avg_latency_ms || 0}ms</div>
            <div className="text-sm text-slate-600">Estimated cost: ${stats.estimated_cost || 0}</div>
          </div>
        ))}
      </div>
      <AgentTrace data={data?.agent_logs || []} />
      <div className="bg-slate-50 rounded-xl p-6">
        Frontend (React) -&gt; FastAPI Backend -&gt; Agent System (Collector, Mirror, Coach, Mental Health) -&gt; SQLite
      </div>
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr>
              {['Date', 'Metric', 'Value', 'Threshold', 'Doctor Notified'].map((header) => <th key={header} className="text-left text-xs text-slate-500 uppercase tracking-wide font-medium py-3 border-b border-slate-200">{header}</th>)}
            </tr>
          </thead>
          <tbody>
            {(data?.agent_logs || []).filter((row) => row.action === 'alert').map((row, index) => (
              <tr key={index} className="border-b border-slate-100">
                <td className="py-3">{row.timestamp}</td>
                <td className="py-3">{row.tool_name}</td>
                <td className="py-3">{row.tool_output}</td>
                <td className="py-3">—</td>
                <td className="py-3"><span className="px-2 py-0.5 rounded-full text-xs font-medium bg-slate-100 text-slate-700">no</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
