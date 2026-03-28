import { Bone, Brain, Flame, Heart } from 'lucide-react';
import useStore from '../store';

const config = [
  { key: 'cardiovascular', icon: Heart, label: 'Cardiovascular', deltaKey: 'cv' },
  { key: 'metabolic', icon: Flame, label: 'Metabolic', deltaKey: 'met' },
  { key: 'musculoskeletal', icon: Bone, label: 'Musculoskeletal', deltaKey: 'msk' },
  { key: 'neurological', icon: Brain, label: 'Neurological', deltaKey: 'neuro' }
];

export default function SubSystemAges({ data, compact = false }) {
  const { dashboard } = useStore();
  const source = data || dashboard;
  if (!source) {
    return <div className={`bg-white rounded-xl shadow-sm border border-slate-200 ${compact ? 'p-4 h-[250px]' : 'p-6 h-[360px]'} animate-pulse bg-slate-200`} />;
  }
  const chrono = source.profile?.age || 0;
  const bio = source.bio_age || {};
  const deltas = bio.deltas || source.bio_age_deltas || {};
  const maxScale = Math.max(...config.map((item) => bio[item.key] || chrono), chrono + 5);

  return (
    <div className={`bg-white rounded-xl shadow-sm border border-slate-200 ${compact ? 'p-4 space-y-3' : 'p-6 space-y-4'}`}>
      {config.map(({ key, icon: Icon, label, deltaKey }) => {
        const value = bio[key] || chrono;
        const delta = deltas[deltaKey] || 0;
        const color = delta < 0 ? 'bg-emerald-500' : delta > 2 ? 'bg-red-500' : 'bg-amber-500';
        return (
          <div key={key}>
            <div className="flex items-center gap-3">
              <Icon size={compact ? 18 : 20} className="text-slate-500" />
              <span className={`${compact ? 'text-xs w-28' : 'text-sm w-36'} font-medium text-slate-700`}>{label}</span>
              <div className="flex-1">
                <div className={`${compact ? 'h-2' : 'h-3'} bg-slate-100 rounded-full`}>
                  <div className={`${compact ? 'h-2' : 'h-3'} rounded-full ${color}`} style={{ width: `${(value / maxScale) * 100}%` }} />
                </div>
              </div>
              <span className={`font-mono ${compact ? 'text-xs w-12' : 'text-sm w-16'} text-right`}>{value.toFixed(1)}</span>
            </div>
            <div className={`text-xs mt-1 ${compact ? 'ml-9' : 'ml-29'} ${delta < 0 ? 'text-emerald-600' : delta > 0 ? 'text-red-600' : 'text-slate-500'}`}>
              {delta === 0 ? 'Aligned with chronological age' : `${Math.abs(delta).toFixed(1)} years ${delta < 0 ? 'younger' : 'older'}`}
            </div>
          </div>
        );
      })}
    </div>
  );
}
