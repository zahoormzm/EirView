import HabitSliders from '../components/HabitSliders';
import RiskChart from '../components/RiskChart';
import WorkoutTargets from '../components/WorkoutTargets';
import useStore from '../store';

function findYear(rows = [], year = 10) {
  return rows.find((row) => Number(row?.year) === year) || rows[rows.length - 1] || null;
}

function deltaClass(delta) {
  if (delta < 0) return 'text-emerald-700';
  if (delta > 0) return 'text-red-700';
  return 'text-slate-600';
}

function formatDelta(delta) {
  if (delta === null || delta === undefined || Number.isNaN(delta)) return 'No change';
  if (delta > 0) return `+${delta.toFixed(1)} pts higher`;
  if (delta < 0) return `${delta.toFixed(1)} pts lower`;
  return 'No change';
}

export default function Insights() {
  const { dashboard, profile, insightSimulation } = useStore();
  const topChange = dashboard?.bio_age?.contributing_factors?.[0];
  const simulation = insightSimulation?.simulation;
  const simulatedTenYear = findYear(simulation?.new_risk_projections, 10);
  const currentTenYear = findYear(dashboard?.risk_projections, 10);
  const scenarioSleep = insightSimulation?.changes?.sleep;
  const currentSleep = profile?.sleep_hours;
  const riskComparisons = currentTenYear && simulatedTenYear ? [
    {
      label: '10-year diabetes risk',
      current: (currentTenYear.diabetes_risk || 0) * 100,
      projected: (simulatedTenYear.diabetes_risk || 0) * 100
    },
    {
      label: '10-year heart risk',
      current: (currentTenYear.cvd_risk || 0) * 100,
      projected: (simulatedTenYear.cvd_risk || 0) * 100
    },
    {
      label: '10-year metabolic risk',
      current: (currentTenYear.metabolic_risk || 0) * 100,
      projected: (simulatedTenYear.metabolic_risk || 0) * 100
    },
    {
      label: '10-year mental decline risk',
      current: (currentTenYear.mental_decline_risk || 0) * 100,
      projected: (simulatedTenYear.mental_decline_risk || 0) * 100
    }
  ] : [];
  const topRiskShift = riskComparisons.length
    ? [...riskComparisons].sort((a, b) => Math.abs(b.projected - b.current) - Math.abs(a.projected - a.current))[0]
    : null;
  const changedInputs = [
    scenarioSleep !== undefined && currentSleep !== undefined
      ? `sleep from ${currentSleep}h to ${scenarioSleep}h`
      : null,
    insightSimulation?.changes?.exercise !== undefined && profile?.exercise_hours_week !== undefined
      ? `exercise from ${profile.exercise_hours_week} to ${insightSimulation.changes.exercise} h/week`
      : null,
    insightSimulation?.changes?.stress !== undefined && profile?.stress_level !== undefined
      ? `stress from ${profile.stress_level}/10 to ${insightSimulation.changes.stress}/10`
      : null,
    insightSimulation?.changes?.screen_time !== undefined && profile?.screen_time_hours !== undefined
      ? `screen time from ${profile.screen_time_hours}h to ${insightSimulation.changes.screen_time}h`
      : null,
  ].filter(Boolean);
  const nextStepText = simulation
    ? simulation.improvement >= 0
      ? `This scenario is worth taking seriously because it improves biological age. The next check is whether ${topRiskShift?.label || 'your highest risk'} drops enough to make this a habit you keep.`
      : `This scenario is not buying you enough. It mainly hurts ${topRiskShift?.label || 'your projected risk'}, so the smarter next test is to undo the most damaging change first${scenarioSleep !== undefined ? `, especially the drop to ${scenarioSleep}h sleep` : ''}.`
    : topChange
      ? `Your highest-leverage move from the current profile is ${topChange.change.toLowerCase()}. Test that single habit first before stacking multiple changes.`
      : 'Use one slider at a time and watch which risk curve drops most clearly.';
  const checkpointText = topRiskShift
    ? `For your current profile, Year 10 matters most because ${topRiskShift.label} is where the baseline and scenario separate most clearly.`
    : 'Year 10 is usually the clearest summary because it shows the trend without exaggerating distant tail risk.';
  const readHint = simulation
    ? `You tested ${changedInputs.join(', ') || 'a hypothetical change'}. If the dashed scenario line sits above the filled baseline, that change is making the outlook worse.`
    : 'Higher curves mean higher cumulative risk over time. Focus on the metric that looks most elevated for your current profile.';

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 border-l-4 border-l-emerald-500 text-sm text-slate-600 italic leading-relaxed">
        {dashboard?.narrative || 'Complete your profile to get a personalized health narrative.'}
      </div>
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
        <div className="text-xs font-semibold uppercase tracking-wide text-slate-500">One Change You Should Do Today</div>
        {topChange ? (
          <>
            <div className="text-2xl font-semibold text-slate-900 mt-2">{topChange.change}</div>
            <div className="text-sm text-slate-600 mt-2">
              Estimated biological age reduction if you make this your next consistent habit:
              {' '}
              <span className="font-semibold text-emerald-700">
                {topChange.estimated_bio_age_reduction?.toFixed?.(1) ?? topChange.estimated_bio_age_reduction} years
              </span>
            </div>
          </>
        ) : (
          <div className="text-sm text-slate-500 mt-2">Add more profile data to rank your highest-impact next step.</div>
        )}
      </div>
      <HabitSliders />
      {simulation && (
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 space-y-5">
          <div>
            <div className="text-lg font-semibold text-slate-900">How To Read Your Last Simulation</div>
            <div className="text-sm text-slate-600 mt-1">
              This is a hypothetical outcome, not a saved profile change.
              {scenarioSleep !== undefined && currentSleep !== undefined && (
                <> You tested sleep moving from <span className="font-medium text-slate-900">{currentSleep}h</span> to <span className="font-medium text-slate-900">{scenarioSleep}h</span>.</>
              )}
            </div>
          </div>
          <div className="grid gap-4 md:grid-cols-3">
            <div className="rounded-xl border border-slate-200 bg-slate-50 p-4">
              <div className="text-xs uppercase tracking-wide font-semibold text-slate-500">Overall Bio Age</div>
              <div className="mt-2 text-sm text-slate-600">Current</div>
              <div className="text-2xl font-semibold text-slate-900">{simulation.current.overall}</div>
              <div className="mt-3 text-sm text-slate-600">Scenario</div>
              <div className="text-2xl font-semibold text-slate-900">{simulation.projected.overall}</div>
            </div>
            <div className={`rounded-xl border p-4 ${simulation.improvement >= 0 ? 'border-emerald-200 bg-emerald-50' : 'border-red-200 bg-red-50'}`}>
              <div className="text-xs uppercase tracking-wide font-semibold text-slate-500">Interpretation</div>
              <div className={`mt-2 text-lg font-semibold ${simulation.improvement >= 0 ? 'text-emerald-700' : 'text-red-700'}`}>
                {simulation.improvement >= 0 ? `${simulation.improvement.toFixed(1)} years younger` : `${Math.abs(simulation.improvement).toFixed(1)} years older`}
              </div>
              <div className="mt-2 text-sm text-slate-600">
                {simulation.improvement >= 0
                  ? 'In this scenario, your habits improve enough to lower projected biological age.'
                  : 'In this scenario, your habits make your projected biological age worse than your current baseline.'}
              </div>
            </div>
            <div className="rounded-xl border border-slate-200 bg-slate-50 p-4">
              <div className="text-xs uppercase tracking-wide font-semibold text-slate-500">What Changed Most</div>
              <div className="mt-2 text-sm text-slate-600">Cardio: <span className={deltaClass(simulation.projected.cardiovascular - simulation.current.cardiovascular)}>{(simulation.projected.cardiovascular - simulation.current.cardiovascular).toFixed(1)}</span></div>
              <div className="text-sm text-slate-600">Metabolic: <span className={deltaClass(simulation.projected.metabolic - simulation.current.metabolic)}>{(simulation.projected.metabolic - simulation.current.metabolic).toFixed(1)}</span></div>
              <div className="text-sm text-slate-600">Musculoskeletal: <span className={deltaClass(simulation.projected.musculoskeletal - simulation.current.musculoskeletal)}>{(simulation.projected.musculoskeletal - simulation.current.musculoskeletal).toFixed(1)}</span></div>
              <div className="text-sm text-slate-600">Neurological: <span className={deltaClass(simulation.projected.neurological - simulation.current.neurological)}>{(simulation.projected.neurological - simulation.current.neurological).toFixed(1)}</span></div>
            </div>
          </div>
          {insightSimulation?.narrative && (
            <div className="rounded-xl border border-blue-200 bg-blue-50 p-4 text-sm text-blue-900 leading-relaxed">
              {insightSimulation.narrative}
            </div>
          )}
          {riskComparisons.length > 0 && (
            <div>
              <div className="text-sm font-semibold text-slate-900 mb-3">What the scenario does to your 10-year outlook</div>
              <div className="grid gap-3 md:grid-cols-2">
                {riskComparisons.map((item) => {
                  const delta = item.projected - item.current;
                  return (
                    <div key={item.label} className="rounded-xl border border-slate-200 p-4 bg-white">
                      <div className="text-sm font-medium text-slate-900">{item.label}</div>
                      <div className="text-xs text-slate-500 mt-1">Current {item.current.toFixed(1)}% -&gt; Scenario {item.projected.toFixed(1)}%</div>
                      <div className={`text-sm font-semibold mt-2 ${deltaClass(delta)}`}>{formatDelta(delta)}</div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}
          <div className="text-xs text-slate-500">
            Future Self chat will use this latest simulation as extra context until you switch users or run a different scenario.
          </div>
        </div>
      )}
      <RiskChart
        data={dashboard?.risk_projections || []}
        comparisonData={simulation?.new_risk_projections || []}
        title={simulation ? 'Risk Forecast: Current vs Your Last Scenario' : 'Risk Forecast From Your Current Profile'}
        subtitle={
          simulation
            ? 'The filled curve is your saved baseline. The dashed curve shows your latest slider simulation so you can see if the scenario genuinely improves your outlook.'
            : 'Pick a metric and read the 5, 10, and 15-year snapshots to understand where risk is heading from your current saved profile.'
        }
        nextStepText={nextStepText}
        checkpointText={checkpointText}
        readHint={readHint}
      />
      <WorkoutTargets data={dashboard?.workout_targets} />
    </div>
  );
}
