import { Footprints } from 'lucide-react';

export default function ActivityNudge({ currentSteps, stepGoal, message }) {
  if (currentSteps >= stepGoal) return null;
  return (
    <div className="border-l-4 border-amber-500 bg-amber-50 p-4 rounded-r-lg">
      <div className="flex items-center gap-2 text-sm text-amber-800">
        <Footprints className="text-amber-500" size={18} />
        {message || `You're ${(stepGoal - currentSteps).toLocaleString()} steps behind your goal. A 20-minute walk would get you there!`}
      </div>
    </div>
  );
}
