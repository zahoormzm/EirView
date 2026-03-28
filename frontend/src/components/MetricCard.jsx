import { ArrowDown, ArrowUp } from 'lucide-react';

export default function MetricCard({ label, value, unit, delta, icon: Icon, status = 'neutral', compact = false }) {
  const statusClass = {
    good: 'bg-green-500',
    warning: 'bg-amber-500',
    critical: 'bg-red-500',
    neutral: 'bg-slate-400'
  }[status];
  const display = value == null ? '—' : Number.isInteger(value) ? value.toLocaleString() : Number(value).toFixed(1);

  return (
    <div className={`bg-white rounded-xl shadow-sm border border-slate-200 ${compact ? 'p-3' : 'p-4'}`}>
      <div className="flex items-center justify-between">
        <Icon size={compact ? 18 : 20} className="text-slate-400" />
        <span className={`w-2.5 h-2.5 rounded-full ${statusClass}`} />
      </div>
      <div className={`${compact ? 'text-xs mt-2' : 'text-sm mt-3'} text-slate-500`}>{label}</div>
      <div className={`${compact ? 'text-xl' : 'text-2xl'} font-mono font-medium tabular-nums text-slate-900 mt-1`}>{display}</div>
      <div className="flex items-center justify-between mt-2">
        <span className="text-xs text-slate-400">{unit}</span>
        {delta != null && (
          <span className={`text-xs font-medium flex items-center gap-1 ${delta >= 0 ? 'text-green-600' : 'text-red-600'}`}>
            {delta >= 0 ? <ArrowUp size={12} /> : <ArrowDown size={12} />}
            {Math.abs(delta).toFixed(1)}
          </span>
        )}
      </div>
    </div>
  );
}
