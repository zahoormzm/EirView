import { GraduationCap } from 'lucide-react';
import ChatInterface from '../components/ChatInterface';
import WellnessGauge from '../components/WellnessGauge';
import useStore from '../store';

export default function Mental() {
  const { dashboard, selectedUserId, profile } = useStore();
  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div>
        <WellnessGauge score={dashboard?.wellness_score || 0} breakdown={dashboard?.wellness_breakdown || []} />
        {profile?.academic_year && (
          <div className="bg-amber-50 border border-amber-200 rounded-xl p-4 mt-4">
            <div className="flex items-center gap-2 text-sm font-semibold text-amber-800"><GraduationCap size={16} /> Academic Pressure</div>
            <div className="mt-3 flex flex-wrap gap-2">
              <span className="bg-white rounded-full px-3 py-1 text-sm font-medium">GPA {profile.academic_gpa ?? '—'}</span>
              <span className="bg-white rounded-full px-3 py-1 text-sm font-medium">{profile.study_hours_daily ?? '—'}h/day</span>
            </div>
            <div className="mt-3 text-sm text-amber-700">Academic year: {profile.academic_year}</div>
            {profile.exam_stress > 7 && <div className="text-amber-700 text-xs mt-2">High academic stress detected — this may be affecting your overall wellness score.</div>}
            {profile.exam_stress > 7 && profile.sleep_hours < 6 && <div className="text-red-600 text-xs mt-1 font-medium">Burnout risk: High study load + insufficient sleep. Consider talking to the coach about balance strategies.</div>}
          </div>
        )}
      </div>
      <div className="lg:col-span-2">
        <ChatInterface
          chatType="mental"
          userId={selectedUserId}
          title="Mental Health Chat"
          placeholder="How are you feeling today?"
          helperText="Use this chat for stress, burnout, mood, routines, sleep-linked wellbeing, and emotional reflection. Unrelated questions are intentionally blocked."
          suggestedPrompts={[
            'I feel overwhelmed and burnt out. What should I do tonight?',
            'How is my sleep affecting my mental wellness?',
            'What routine would help with exam stress?'
          ]}
        />
      </div>
    </div>
  );
}
