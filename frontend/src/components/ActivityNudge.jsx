import { Footprints } from 'lucide-react';

export default function ActivityNudge({ currentSteps, stepGoal, message, compact = false }) {
  if (currentSteps >= stepGoal) return null;
  return (
    <div className={`border-l-4 border-amber-500 bg-amber-50 rounded-r-lg ${compact ? 'p-3' : 'p-4'}`}>
      <div className={`flex items-center gap-2 ${compact ? 'text-xs' : 'text-sm'} text-amber-800`}>
        <Footprints className="text-amber-500" size={compact ? 16 : 18} />
        {message || `You're ${(stepGoal - currentSteps).toLocaleString()} steps behind your goal. A 20-minute walk would get you there!`}
      </div>
    </div>
  );
}
