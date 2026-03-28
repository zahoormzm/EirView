import { X } from 'lucide-react';
import { useEffect } from 'react';
import { getReminders } from '../api';
import useStore from '../store';

const formatDateTime = (value) => {
  if (!value) return 'No upload recorded';
  const normalizedValue = /^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$/.test(value)
    ? value.replace(' ', 'T') + 'Z'
    : value;
  const parsed = new Date(normalizedValue);
  if (Number.isNaN(parsed.getTime())) return value;
  return parsed.toLocaleString([], { dateStyle: 'medium', timeStyle: 'short' });
};

export default function ReminderCards({ compact = false }) {
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
    <div className="mb-6 min-w-0">
      <div className="flex gap-4 overflow-x-auto pb-2 pr-1 snap-x snap-mandatory">
      {reminders.map((reminder, index) => {
        const className = reminder.urgency === 'high' ? 'border-red-500 bg-red-50' : reminder.urgency === 'medium' ? 'border-amber-500 bg-amber-50' : 'border-blue-500 bg-blue-50';
        const message = compact && reminder.message?.length > 120 ? `${reminder.message.slice(0, 117)}...` : reminder.message;
        return (
          <div key={`${reminder.source}-${index}`} className={`snap-start flex-shrink-0 ${compact ? 'w-[18rem] max-w-[70vw] p-3' : 'w-[22rem] max-w-[85vw] p-4'} rounded-lg border-l-4 ${className}`}>
            <button className="ml-auto block text-slate-400 hover:text-slate-600 cursor-pointer" onClick={() => setReminders(reminders.filter((_, itemIndex) => itemIndex !== index))}>
              <X size={16} />
            </button>
            <div className="text-xs font-semibold uppercase tracking-wide text-slate-500 mb-2">{reminder.label || reminder.source}</div>
            <div className={`${compact ? 'text-xs' : 'text-sm'} text-slate-700`}>{message}</div>
            <div className="text-xs text-slate-500 mt-2">
              Last recorded: {formatDateTime(reminder.last_synced)}
            </div>
          </div>
        );
      })}
      </div>
    </div>
  );
}
