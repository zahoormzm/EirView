import { Sparkles } from 'lucide-react';
import ChatInterface from '../components/ChatInterface';
import useStore from '../store';

export default function FutureSelf() {
  const { selectedUserId, profile, insightSimulation } = useStore();
  const simulationContext = insightSimulation?.simulation ? [
    'Latest Insights scenario (hypothetical, not saved profile):',
    `Sleep: ${insightSimulation?.changes?.sleep ?? 'unchanged'} hours`,
    `Exercise: ${insightSimulation?.changes?.exercise ?? 'unchanged'} hours/week`,
    `Diet score: ${insightSimulation?.changes?.diet ?? 'unchanged'} / 4`,
    `Stress level: ${insightSimulation?.changes?.stress ?? 'unchanged'} / 10`,
    `Screen time: ${insightSimulation?.changes?.screen_time ?? 'unchanged'} hours/day`,
    `Projected bio age: ${insightSimulation.simulation.projected.overall} (current ${insightSimulation.simulation.current.overall})`,
    `Improvement: ${insightSimulation.simulation.improvement} years`
  ].join('\n') : '';
  return (
    <div>
      <div className="bg-blue-50 border border-blue-200 rounded-xl p-6 mb-6">
        <div className="flex items-center gap-2 font-semibold text-blue-800"><Sparkles size={18} className="text-blue-500" /> Talk to Your Future Self</div>
        <div className="text-sm text-blue-700 mt-2">You're chatting with {(profile?.age || 19) + 15}-year-old you — the version that lived through the next 15 years with your current data.</div>
        {insightSimulation?.simulation && (
          <div className="text-sm text-blue-800 mt-3 font-medium">
            This chat is currently grounded in your latest Insights simulation as well.
          </div>
        )}
      </div>
      <ChatInterface
        chatType="future"
        userId={selectedUserId}
        title="Future Self"
        placeholder="Ask your future self about your health path..."
        helperText="This chat is for long-term health trajectory, risk, habit consequences, and where your current patterns may lead. Unrelated questions are blocked."
        suggestedPrompts={[
          'If I keep these habits for five years, what happens?',
          'What changes would my future self thank me for most?',
          'How does my current bio age trend affect my long-term outlook?'
        ]}
        context={simulationContext}
        tall
      />
    </div>
  );
}
