export default function AchievementGrid({ achievements = [] }) {
  const defs = [
    { id: 'first_blood', name: 'First Blood', icon_emoji: '🩸' },
    { id: 'face_future', name: 'Face Future', icon_emoji: '📸' },
    { id: 'stand_tall', name: 'Stand Tall', icon_emoji: '🧍' },
    { id: 'week_warrior', name: 'Week Warrior', icon_emoji: '🔥' },
    { id: 'data_complete', name: 'Data Complete', icon_emoji: '📊' }
  ];
  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
      <div className="grid grid-cols-5 gap-4">
        {defs.map((item) => {
          const earned = achievements.some((achievement) => achievement.badge_id === item.id);
          return (
            <div key={item.id} className="text-center">
              <div className={`w-16 h-16 rounded-full flex items-center justify-center mx-auto text-2xl ${earned ? 'bg-emerald-100 border-2 border-emerald-500' : 'bg-slate-100 border-2 border-slate-200 opacity-40 grayscale'}`}>{item.icon_emoji}</div>
              <div className={`text-xs mt-1 font-medium ${earned ? 'text-slate-700' : 'text-slate-400'}`}>{item.name}</div>
            </div>
          );
        })}
      </div>
      <div className="text-sm text-slate-500 mt-4">Earned: {achievements.length}/{defs.length}</div>
    </div>
  );
}
