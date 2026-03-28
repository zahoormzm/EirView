import { useState } from 'react';
import { getDashboard, uploadMeal } from '../api';
import ChatInterface from '../components/ChatInterface';
import FileUpload from '../components/FileUpload';
import MealAnalysis from '../components/MealAnalysis';
import NutritionTargets from '../components/NutritionTargets';
import NutritionTracker from '../components/NutritionTracker';
import useStore from '../store';

export default function Nutrition() {
  const { dashboard, selectedUserId, showToast, setDashboard } = useStore();
  const [analysis, setAnalysis] = useState(null);
  const [description, setDescription] = useState('');
  const latestMealSummary = analysis
    ? {
        items: (analysis.items || []).map((item) => ({
          item: item.item,
          portion_g: item.portion_g,
          calories: item.calories,
          protein_g: item.protein_g,
          sat_fat_g: item.sat_fat_g
        })),
        total: analysis.total,
        flags: analysis.flags,
        score: analysis.health_score || analysis.score
      }
    : null;
  const nutritionContext = [
    `User: ${selectedUserId}`,
    `Nutrition targets: ${dashboard?.nutrition_targets ? JSON.stringify(dashboard.nutrition_targets) : 'unavailable'}`,
    `Recent meals: ${(dashboard?.recent_meals || []).slice(0, 3).map((meal) => `${meal.description || 'Meal entry'} (${meal.calories || meal.nutrition?.calories || 0} cal)`).join('; ') || 'none logged'}`,
    `Latest meal analysis: ${latestMealSummary ? JSON.stringify(latestMealSummary) : 'none yet on this page'}`
  ].join('\n');

  const refreshDashboard = async () => {
    const response = await getDashboard(selectedUserId);
    setDashboard(response.data);
  };

  const handleMealResult = async (payload) => {
    setAnalysis(payload);
    await refreshDashboard();
  };

  const uploadPhoto = async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('user_id', selectedUserId);
    return uploadMeal(formData);
  };

  const analyzeText = async () => {
    try {
      const response = await uploadMeal({ user_id: selectedUserId, description });
      await handleMealResult(response.data);
      setDescription('');
    } catch (error) {
      showToast(error.message, 'error');
    }
  };

  return (
    <div className="space-y-6">
      <NutritionTargets data={dashboard?.nutrition_targets} />
      <NutritionTracker />
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 space-y-4">
        <FileUpload accept=".jpg,.jpeg,.png" label="Meal Photo" endpoint={uploadPhoto} onUpload={handleMealResult} />
        <div className="text-center text-slate-400 text-sm">-- or --</div>
        <div className="flex gap-2">
          <input value={description} onChange={(event) => setDescription(event.target.value)} placeholder="Type what you ate" className="border border-slate-300 rounded-lg px-3 py-2 text-sm flex-1" />
          <button onClick={analyzeText} className="bg-emerald-500 hover:bg-emerald-600 text-white rounded-lg px-4 py-2 font-medium transition">Analyze</button>
        </div>
      </div>
      <MealAnalysis analysis={analysis} />
      <ChatInterface
        chatType="coach"
        userId={selectedUserId}
        title={analysis ? 'Ask AI About This Meal' : 'Nutrition Coach'}
        placeholder={analysis ? 'Ask what is good, bad, or what to change in this meal' : 'Ask about your meals, targets, or what to eat next'}
        helperText={
          analysis
            ? 'The uploaded meal above is included automatically in this chat context, along with your nutrition targets and recent meals.'
            : 'The coach uses your nutrition targets, recent meals, and the latest meal analysis on this page.'
        }
        suggestedPrompts={
          analysis
            ? [
                'What is wrong with this meal for my current targets?',
                'What should I change in this exact meal?',
                'If I eat this, what should my next meal look like?'
              ]
            : [
                'What should I eat next based on this analysis?',
                'Where is this meal off relative to my targets?',
                'How can I improve my protein and keep calories controlled?'
              ]
        }
        context={nutritionContext}
      />
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
        <div className="font-semibold text-slate-900 mb-4">Recent Meals</div>
        {(dashboard?.recent_meals || []).map((meal) => (
          <div key={meal.id} className="py-3 border-b border-slate-100">
            <div className="text-sm text-slate-700">{meal.description || 'Meal entry'}</div>
            <div className="text-xs text-slate-500">{meal.timestamp || meal.date} · {meal.calories || meal.nutrition?.calories || 0} cal</div>
          </div>
        ))}
      </div>
    </div>
  );
}
