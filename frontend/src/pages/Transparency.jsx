import AgentTrace from '../components/AgentTrace';
import useStore from '../store';
import { getTransparency } from '../api';
import { useEffect, useState } from 'react';

export default function Transparency() {
  const { selectedUserId, showToast } = useStore();
  const [data, setData] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);

  const statsFor = (providerKey) => {
    const providerStats = data?.model_stats?.[providerKey];
    if (providerStats?.calls) {
      return providerStats;
    }
    const exactStats = Object.entries(data?.exact_model_stats || {})
      .filter(([model]) => model.toLowerCase().includes(providerKey))
      .reduce((aggregate, [, stats]) => ({
        calls: aggregate.calls + (stats.calls || 0),
        success: aggregate.success + (stats.success || 0),
        total_latency_ms: aggregate.total_latency_ms + (stats.total_latency_ms || 0),
        estimated_cost: aggregate.estimated_cost + Number(stats.estimated_cost || 0),
      }), { calls: 0, success: 0, total_latency_ms: 0, estimated_cost: 0 });
    if (!exactStats.calls) {
      return providerStats || {};
    }
    return {
      ...exactStats,
      avg_latency_ms: Math.round(exactStats.total_latency_ms / Math.max(exactStats.calls, 1)),
      success_rate: Math.round((exactStats.success / Math.max(exactStats.calls, 1)) * 1000) / 10,
    };
  };

  const load = async ({ silent = false } = {}) => {
    try {
      const response = await getTransparency(selectedUserId);
      setData(response.data);
      setLastUpdated(new Date());
    } catch (error) {
      if (!silent) {
        showToast(error.message, 'error');
      }
    }
  };

  useEffect(() => {
    load();
    const intervalId = window.setInterval(() => load({ silent: true }), 5000);
    return () => window.clearInterval(intervalId);
  }, [selectedUserId, showToast]);

  const cards = [
    ['Claude Sonnet 4', statsFor('claude'), 'bg-blue-50 border-blue-200'],
    ['Gemini 2.5 Flash', statsFor('gemini'), 'bg-purple-50 border-purple-200'],
    ['Deterministic', statsFor('deterministic'), 'bg-slate-50 border-slate-200']
  ];
  const recentCalls = data?.recent_calls || [];

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
        <div>
          <div className="font-semibold text-slate-900">Live Transparency Feed</div>
          <div className="text-sm text-slate-600 mt-1">
            This tab auto-refreshes every 5 seconds. Stored agent logs appear after agent/tool runs, while recent model calls appear below even before they are summarized elsewhere.
          </div>
        </div>
        <div className="text-sm text-slate-500">
          Last updated: {lastUpdated ? lastUpdated.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit', second: '2-digit' }) : 'Loading...'}
        </div>
      </div>
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
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 overflow-x-auto">
        <div className="font-semibold text-slate-900">Recent Model Calls</div>
        <div className="text-sm text-slate-500 mt-1">These are the latest provider calls seen by the backend process.</div>
        {!recentCalls.length ? (
          <div className="text-sm text-slate-500 mt-4">No recent model calls in memory yet. Trigger Coach, Mental Health, Future Self, blood parsing, or meal/photo analysis to populate this.</div>
        ) : (
          <table className="w-full mt-4">
            <thead>
              <tr>
                {['Time', 'Task', 'Model', 'Latency', 'Success'].map((header) => (
                  <th key={header} className="text-left text-xs text-slate-500 uppercase tracking-wide font-medium py-3 border-b border-slate-200">
                    {header}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {recentCalls.slice().reverse().map((row, index) => (
                <tr key={`${row.timestamp}-${row.task}-${index}`} className="border-b border-slate-100">
                  <td className="py-3 text-sm text-slate-600">
                    {row.timestamp ? new Date(row.timestamp * 1000).toLocaleTimeString([], { hour: 'numeric', minute: '2-digit', second: '2-digit' }) : '—'}
                  </td>
                  <td className="py-3 text-sm text-slate-800">{row.task || '—'}</td>
                  <td className="py-3 text-sm text-slate-600 font-mono">{row.model || '—'}</td>
                  <td className="py-3 text-sm text-slate-600">{row.latency_ms || 0}ms</td>
                  <td className="py-3 text-sm">
                    <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${row.success ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-700'}`}>
                      {row.success ? 'yes' : 'no'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
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
