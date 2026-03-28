import { X } from 'lucide-react';
import { useEffect } from 'react';
import { getReminders } from '../api';
import useStore from '../store';

export default function ReminderCards() {
  const { reminders, setReminders, selectedUserId, showToast } = useStore();

  useEffect(() => {
    (async () => {
      try {
        const response = await getReminders(selectedUserId);
        setReminders(response.data);
      } catch (error) {
        showToast(error.message, 'error');
      }
    })();
  }, [selectedUserId, setReminders, showToast]);

  if (!reminders?.length) return null;

  return (
    <div className="flex gap-4 overflow-x-auto pb-2 mb-6">
      {reminders.map((reminder, index) => {
        const className = reminder.urgency === 'high' ? 'border-red-500 bg-red-50' : reminder.urgency === 'medium' ? 'border-amber-500 bg-amber-50' : 'border-blue-500 bg-blue-50';
        return (
          <div key={`${reminder.source}-${index}`} className={`flex-shrink-0 w-80 rounded-lg p-4 border-l-4 ${className}`}>
            <button className="ml-auto block text-slate-400 hover:text-slate-600 cursor-pointer" onClick={() => setReminders(reminders.filter((_, itemIndex) => itemIndex !== index))}>
              <X size={16} />
            </button>
            <div className="text-sm text-slate-700">{reminder.message}</div>
            <div className="text-xs text-slate-500 mt-1">{reminder.source}</div>
          </div>
        );
      })}
    </div>
  );
}
