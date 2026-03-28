import { useState } from 'react';
import { updateProfile } from '../api';
import useStore from '../store';

export default function Settings() {
  const { selectedUserId, profile, showToast } = useStore();
  const [server, setServer] = useState({ ip: 'localhost', port: '8000' });
  const [contacts, setContacts] = useState({
    doctor_name: profile?.doctor_name || '',
    doctor_email: profile?.doctor_email || '',
    doctor_phone: profile?.doctor_phone || '',
    emergency_contact_name: profile?.emergency_contact_name || '',
    emergency_contact_phone: profile?.emergency_contact_phone || '',
    privacy_level: 'summary'
  });

  const save = async () => {
    try {
      await updateProfile(selectedUserId, contacts);
      showToast('Settings saved');
    } catch (error) {
      showToast(error.message, 'error');
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
        <div className="font-semibold text-slate-900 mb-4">Server Configuration</div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <input value={server.ip} onChange={(event) => setServer({ ...server, ip: event.target.value })} placeholder="IP" className="border border-slate-300 rounded-lg px-3 py-2 text-sm" />
          <input value={server.port} onChange={(event) => setServer({ ...server, port: event.target.value })} placeholder="Port" className="border border-slate-300 rounded-lg px-3 py-2 text-sm" />
        </div>
      </div>
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
        <div className="font-semibold text-slate-900 mb-4">Medical Contacts</div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {Object.keys(contacts).filter((key) => key !== 'privacy_level').map((key) => (
            <input key={key} value={contacts[key]} onChange={(event) => setContacts({ ...contacts, [key]: event.target.value })} placeholder={key.replace(/_/g, ' ')} className="border border-slate-300 rounded-lg px-3 py-2 text-sm" />
          ))}
        </div>
        <button onClick={save} className="bg-emerald-500 hover:bg-emerald-600 text-white rounded-lg px-4 py-2 font-medium transition mt-4">Save</button>
      </div>
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
        <div className="font-semibold text-slate-900 mb-4">Spotify Integration</div>
        <button className="bg-emerald-500 hover:bg-emerald-600 text-white rounded-lg px-4 py-2 font-medium transition">Connect Spotify</button>
      </div>
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
        <div className="font-semibold text-slate-900 mb-4">Privacy Settings</div>
        <select value={contacts.privacy_level} onChange={(event) => setContacts({ ...contacts, privacy_level: event.target.value })} className="border border-slate-300 rounded-lg px-3 py-2 text-sm">
          <option value="full">Full</option>
          <option value="summary">Summary</option>
          <option value="minimal">Minimal</option>
        </select>
      </div>
      <div className="bg-white rounded-xl shadow-sm border border-red-200 p-6">
        <div className="font-semibold text-slate-900 mb-4">Danger Zone</div>
        <button onClick={() => window.confirm('Delete all data?') && showToast('Delete flow not implemented on backend', 'warning')} className="bg-red-500 hover:bg-red-600 text-white rounded-lg px-4 py-2 font-medium transition">Delete My Data</button>
      </div>
    </div>
  );
}
