import AchievementGrid from '../components/AchievementGrid';
import DailyChecklist from '../components/DailyChecklist';
import Leaderboard from '../components/Leaderboard';
import WeeklyChallenge from '../components/WeeklyChallenge';
import XPBar from '../components/XPBar';
import useStore from '../store';

export default function GamificationPage() {
  const { gamification } = useStore();
  const currentXP = gamification?.total_xp || 0;
  const nextLevelXP = currentXP + (gamification?.xp_to_next_level || 100);

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <XPBar level={gamification?.level} levelName={gamification?.level_name} currentXP={currentXP} nextLevelXP={nextLevelXP} />
        <div className="lg:col-span-2 bg-white rounded-xl shadow-sm border border-slate-200 p-6">
          <div className="text-2xl font-bold">🔥 {gamification?.current_streak || 0}-day streak</div>
          <div className="grid grid-cols-7 gap-2 mt-4">
            {Array.from({ length: 35 }).map((_, index) => <div key={index} className={`h-5 rounded ${index < (gamification?.current_streak || 0) ? 'bg-emerald-500' : 'bg-slate-200'}`} />)}
          </div>
        </div>
      </div>
      <DailyChecklist />
      <WeeklyChallenge name="Move 5 Days" description="Hit your movement target on 5 days this week." current={gamification?.active_challenge?.progress || 3} target={gamification?.active_challenge?.target || 5} />
      <AchievementGrid achievements={gamification?.achievements || []} />
      <Leaderboard />
    </div>
  );
}
