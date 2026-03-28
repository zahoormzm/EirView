export default function FamilyDashboard({ data }) {
  if (!data) {
    return <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 text-sm text-slate-500">Family dashboard unavailable.</div>;
  }
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {data.members?.map((member) => (
          <div key={member.user_id} className="bg-white rounded-xl shadow-sm border border-slate-200 p-4">
            <div className="font-medium text-slate-700">{member.name}</div>
            <div className="text-sm text-slate-500">{member.relationship}</div>
            <div className="text-sm text-slate-600 mt-3">Bio age: {member.bio_age_overall ?? '—'}</div>
            <div className="text-sm text-slate-600">Streak: {member.current_streak}</div>
            <div className="text-xs text-slate-400 mt-2">Privacy: {member.privacy_level}</div>
          </div>
        ))}
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {(data.health_flags || []).map((flag, index) => (
          <div key={`${flag.condition}-${index}`} className="bg-amber-50 rounded-xl p-4 border border-amber-200">
            <div className="font-medium text-amber-800">{flag.condition}</div>
            <div className="text-sm text-amber-700 mt-1">{flag.evidence}</div>
          </div>
        ))}
      </div>
      <div className="bg-slate-100 rounded-lg px-4 py-3 text-center font-mono text-lg text-slate-700">
        {data.family?.join_code}
      </div>
      <button className="text-red-500 text-sm hover:text-red-700 cursor-pointer mt-4">Leave Family</button>
    </div>
  );
}
