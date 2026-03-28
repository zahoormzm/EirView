import { useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { getProfile } from '../api';
import useStore from '../store';

export default function SpotifyCallback() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { setProfile, selectedUserId, showToast } = useStore();

  useEffect(() => {
    const code = searchParams.get('code');
    const state = searchParams.get('state') || selectedUserId;
    const error = searchParams.get('error');
    if (error) {
      showToast(`Spotify authorization failed: ${error}`, 'error');
      navigate('/settings', { replace: true });
      return;
    }
    if (!code) {
      showToast('Spotify callback is missing an authorization code', 'error');
      navigate('/settings', { replace: true });
      return;
    }

    const run = async () => {
      try {
        const response = await fetch(`/api/spotify/callback?code=${encodeURIComponent(code)}&state=${encodeURIComponent(state)}`);
        const payload = await response.json();
        if (!response.ok || !payload?.success) {
          throw new Error(payload?.detail || payload?.message || 'Spotify sync failed');
        }
        const profileResponse = await getProfile(state);
        setProfile(profileResponse.data);
        showToast('Spotify connected successfully');
      } catch (callbackError) {
        showToast(callbackError.message, 'error');
      } finally {
        navigate('/settings', { replace: true });
      }
    };

    run();
  }, [navigate, searchParams, selectedUserId, setProfile, showToast]);

  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-8 text-center">
      <div className="text-lg font-semibold text-slate-900">Connecting Spotify</div>
      <div className="text-sm text-slate-500 mt-2">Finishing authorization and syncing recent listening data.</div>
    </div>
  );
}
