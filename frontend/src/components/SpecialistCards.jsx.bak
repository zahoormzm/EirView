import { useEffect, useState } from 'react';
import { getSpecialists } from '../api';
import useStore from '../store';

export default function SpecialistCards() {
  const { selectedUserId, showToast } = useStore();
  const [items, setItems] = useState([]);

  useEffect(() => {
    (async () => {
      try {
        const response = await getSpecialists(selectedUserId);
        setItems(response.data || []);
      } catch (error) {
        showToast(error.message, 'error');
      }
    })();
  }, [selectedUserId, showToast]);

  if (!items.length) return null;
  return (
    <section className="mt-6">
      <h3 className="font-semibold text-slate-900 mb-4">Specialist Recommendations</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {items.map((item) => (
          <div key={item.specialist} className={`rounded-xl border p-4 ${item.urgency === 'urgent' ? 'border-red-500' : 'border-amber-500'}`}>
            <div className="flex items-start justify-between gap-3">
              <div className="font-medium text-slate-700 capitalize">{item.specialist}</div>
              <span className={`text-xs font-semibold uppercase tracking-wide px-2 py-1 rounded-full ${item.urgency === 'urgent' ? 'bg-red-100 text-red-700' : item.urgency === 'soon' ? 'bg-amber-100 text-amber-700' : 'bg-slate-100 text-slate-600'}`}>
                {item.urgency}
              </span>
            </div>
            <div className="text-sm text-slate-600 mt-2">{item.doctor_report?.summary?.headline || item.reasons.join(', ')}</div>
            {!!item.metrics?.length && (
              <div className="mt-4 space-y-2">
                {item.metrics.map((metric) => (
                  <div key={`${item.specialist}-${metric.metric}-${metric.reason}`} className="rounded-lg bg-slate-50 border border-slate-200 px-3 py-2">
                    <div className="text-sm font-medium text-slate-700">{metric.reason}</div>
                    <div className="text-xs text-slate-500 mt-1">{metric.display_value} vs threshold {metric.display_threshold}</div>
                  </div>
                ))}
              </div>
            )}
            <div className="text-xs text-slate-500 mt-3">{item.hospitals.join(' • ')}</div>
            <details className="mt-4 rounded-lg border border-slate-200 bg-white">
              <summary className="cursor-pointer list-none px-4 py-3 text-sm font-medium text-slate-700">View Doctor Report</summary>
              <div className="px-4 pb-4">
                {(item.doctor_report?.summary?.why_now || []).map((reason) => (
                  <div key={reason} className="text-sm text-slate-600 mt-2">{reason}</div>
                ))}
                {!!item.doctor_report?.next_steps?.length && (
                  <div className="mt-4">
                    <div className="text-xs font-semibold uppercase tracking-wide text-slate-500">Next Steps</div>
                    {item.doctor_report.next_steps.map((step) => (
                      <div key={step} className="text-sm text-slate-600 mt-2">{step}</div>
                    ))}
                  </div>
                )}
                {!!item.doctor_report?.missing_relevant_data?.length && (
                  <div className="mt-4">
                    <div className="text-xs font-semibold uppercase tracking-wide text-slate-500">Missing Relevant Data</div>
                    <div className="text-sm text-slate-600 mt-2">{item.doctor_report.missing_relevant_data.join(', ')}</div>
                  </div>
                )}
              </div>
            </details>
          </div>
        ))}
      </div>
    </section>
  );
}
