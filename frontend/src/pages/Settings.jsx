import { useEffect, useState } from 'react';
import { createUser, getSpotifySync, getUsers, updateProfile } from '../api';
import useStore from '../store';

const demoUserNotes = {
  zahoor: 'Primary demo profile with broader health history, reminders, and multi-feature coverage for the main dashboard walkthrough.',
  riya: 'Secondary demo user suited for family-group and comparative views with a different baseline profile.',
  arjun: 'Third demo user for leaderboard, switching, and additional independent testing without affecting the main demo path.'
};

export default function Settings() {
  const { selectedUserId, profile, users, setProfile, setSelectedUser, setUsers, showToast } = useStore();
  const [server, setServer] = useState({ ip: 'localhost', port: '8000' });
  const [contacts, setContacts] = useState({
    doctor_name: profile?.doctor_name || '',
    doctor_email: profile?.doctor_email || '',
    doctor_phone: profile?.doctor_phone || '',
    emergency_contact_name: profile?.emergency_contact_name || '',
    emergency_contact_phone: profile?.emergency_contact_phone || '',
    privacy_level: 'summary'
  });
  const [newUser, setNewUser] = useState({ id: '', name: '', age: '', sex: 'female', height_cm: '' });

  useEffect(() => {
    setContacts((previous) => ({
      ...previous,
      doctor_name: profile?.doctor_name || '',
      doctor_email: profile?.doctor_email || '',
      doctor_phone: profile?.doctor_phone || '',
      emergency_contact_name: profile?.emergency_contact_name || '',
      emergency_contact_phone: profile?.emergency_contact_phone || ''
    }));
  }, [profile]);

  const save = async () => {
    try {
      const response = await updateProfile(selectedUserId, contacts);
      setProfile(response.data?.profile || { ...profile, ...contacts });
      showToast('Settings saved');
    } catch (error) {
      showToast(error.message, 'error');
    }
  };

  const connectSpotify = async () => {
    try {
      const response = await getSpotifySync(selectedUserId);
      if (response.data?.needs_auth && response.data?.auth_url) {
        window.location.href = response.data.auth_url;
        return;
      }
      showToast(response.data?.success ? 'Spotify synced' : 'Spotify is unavailable', response.data?.success ? 'success' : 'warning');
    } catch (error) {
      showToast(error.message, 'error');
    }
  };

  const addUser = async () => {
    if (!newUser.id.trim() || !newUser.name.trim()) {
      showToast('User id and name are required', 'error');
      return;
    }
    try {
      const payload = {
        id: newUser.id.trim().toLowerCase(),
        name: newUser.name.trim(),
        age: newUser.age === '' ? null : Number(newUser.age),
        sex: newUser.sex,
        height_cm: newUser.height_cm === '' ? null : Number(newUser.height_cm)
      };
      await createUser(payload);
      const usersResponse = await getUsers();
      const nextUsers = Array.isArray(usersResponse.data) ? usersResponse.data : usersResponse.data?.users || [];
      setUsers(nextUsers);
      setSelectedUser(payload.id);
      setNewUser({ id: '', name: '', age: '', sex: 'female', height_cm: '' });
      showToast('User created successfully');
    } catch (error) {
      showToast(error.message, 'error');
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
        <div className="font-semibold text-slate-900 mb-4">Users</div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div>
            <div className="text-sm font-medium text-slate-700 mb-3">Existing Users</div>
            <div className="space-y-3">
              {users.map((user) => (
                <div key={user.id} className={`rounded-lg border px-4 py-3 ${user.id === selectedUserId ? 'border-emerald-400 bg-emerald-50' : 'border-slate-200 bg-slate-50'}`}>
                  <div className="flex items-center justify-between gap-3">
                    <div>
                      <div className="font-medium text-slate-800">{user.name}</div>
                      <div className="text-xs text-slate-500">{user.id} • {user.age ?? 'Age n/a'} • {user.sex || 'Sex n/a'}</div>
                    </div>
                    <button onClick={() => setSelectedUser(user.id)} className="text-sm font-medium text-emerald-700 hover:text-emerald-800">
                      {user.id === selectedUserId ? 'Selected' : 'Switch'}
                    </button>
                  </div>
                  <div className="text-sm text-slate-600 mt-2">
                    {demoUserNotes[user.id] || 'Custom user profile created from the Settings page for additional testing and demos.'}
                  </div>
                </div>
              ))}
            </div>
          </div>
          <div>
            <div className="text-sm font-medium text-slate-700 mb-3">Add User</div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <input value={newUser.id} onChange={(event) => setNewUser({ ...newUser, id: event.target.value })} placeholder="User id" className="border border-slate-300 rounded-lg px-3 py-2 text-sm" />
              <input value={newUser.name} onChange={(event) => setNewUser({ ...newUser, name: event.target.value })} placeholder="Full name" className="border border-slate-300 rounded-lg px-3 py-2 text-sm" />
              <input type="number" value={newUser.age} onChange={(event) => setNewUser({ ...newUser, age: event.target.value })} placeholder="Age" className="border border-slate-300 rounded-lg px-3 py-2 text-sm" />
              <input type="number" value={newUser.height_cm} onChange={(event) => setNewUser({ ...newUser, height_cm: event.target.value })} placeholder="Height (cm)" className="border border-slate-300 rounded-lg px-3 py-2 text-sm" />
              <select value={newUser.sex} onChange={(event) => setNewUser({ ...newUser, sex: event.target.value })} className="border border-slate-300 rounded-lg px-3 py-2 text-sm md:col-span-2">
                <option value="female">female</option>
                <option value="male">male</option>
                <option value="other">other</option>
              </select>
            </div>
            <button onClick={addUser} className="bg-emerald-500 hover:bg-emerald-600 text-white rounded-lg px-4 py-2 font-medium transition mt-4">Create User</button>
          </div>
        </div>
      </div>
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
        <button onClick={connectSpotify} className="bg-emerald-500 hover:bg-emerald-600 text-white rounded-lg px-4 py-2 font-medium transition">Connect Spotify</button>
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
