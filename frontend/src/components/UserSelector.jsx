import useStore from '../store';

export default function UserSelector() {
  const { users, selectedUserId, setSelectedUser } = useStore();

  return (
    <select
      className="border border-slate-300 rounded-lg px-3 py-1.5 text-sm bg-white"
      value={selectedUserId}
      onChange={(event) => setSelectedUser(event.target.value)}
    >
      {users.map((user) => (
        <option key={user.id} value={user.id}>{user.name}</option>
      ))}
    </select>
  );
}
