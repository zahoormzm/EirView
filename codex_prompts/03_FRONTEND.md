# Codex Task: EirView Frontend — Complete React Application

Generate the COMPLETE frontend for EirView, a health intelligence platform. Every single file listed in the file structure below must be created with full, working code. Do not leave any file as a stub or placeholder.

**Tech stack**: React 19 + Vite + Tailwind CSS v4 (CSS-first config via `@tailwindcss/vite`) + Recharts + Zustand + axios + lucide-react + react-router-dom.

---

## Design System

### Color Palette (Tailwind classes)
- **Primary**: emerald — `emerald-500` (buttons, active states), `emerald-600` (hover), `emerald-50` (light bg)
- **Secondary**: blue — `blue-500` (info), `blue-50` (light bg)
- **Warning**: amber — `amber-500` (caution flags), `amber-50` (light bg)
- **Danger**: red — `red-500` (critical alerts), `red-50` (light bg)
- **Success**: green — `green-500` (good values)
- **Background**: `slate-50` (page bg), `white` (cards)
- **Sidebar**: `slate-900` (dark sidebar), `slate-800` (hover), `white` text
- **Text**: `slate-900` (headings), `slate-600` (body), `slate-400` (muted)
- **Border**: `slate-200`

### Typography
- Font: system default (Inter if available)
- Headings: `font-semibold`
- Metrics/numbers: `font-mono font-medium tabular-nums`
- Body: `text-sm` or `text-base`

### Component Patterns
- Cards: `bg-white rounded-xl shadow-sm border border-slate-200 p-6`
- Buttons primary: `bg-emerald-500 hover:bg-emerald-600 text-white rounded-lg px-4 py-2 font-medium transition`
- Buttons secondary: `border border-slate-300 text-slate-700 rounded-lg px-4 py-2 hover:bg-slate-50`
- Input fields: `border border-slate-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500`
- Badge: `px-2 py-0.5 rounded-full text-xs font-medium`
- Toast/alert: fixed top-right, auto-dismiss after 5s

### Layout Structure
```
+-------------------------------------------------------------+
| Sidebar (w-64, fixed)  |  Main Content (flex-1, ml-64)      |
|                        |                                     |
| +--------------------+ |  +-----------------------------+   |
| | EirView Logo       | |  | Top Bar                     |   |
| | (32px height)      | |  | Page title | UserSelector    |   |
| +--------------------+ |  | | StreakBadge | Notifications|   |
|                        |  +-----------------------------+   |
| Nav Items:             |                                     |
|  Dashboard             |  +-----------------------------+   |
|  Data Ingest           |  |                             |   |
|  Insights              |  |  Page Content               |   |
|  Mental Health         |  |  (max-w-7xl mx-auto px-6)   |   |
|  Nutrition             |  |                             |   |
|  Future Self           |  |                             |   |
|  Activity              |  |                             |   |
|  Gamification          |  |                             |   |
|  Transparency          |  |                             |   |
|                        |  +-----------------------------+   |
| --------------------   |                                     |
|  Family (if joined)    |                                     |
|  Settings              |                                     |
+-------------------------------------------------------------+
```

---

## File Structure

Create ALL of these files with complete, working code:

```
frontend/
  package.json
  vite.config.js
  index.html
  src/
    main.jsx
    index.css
    App.jsx
    api.js
    store.js
    pages/
      Dashboard.jsx
      DataIngest.jsx
      Insights.jsx
      Mental.jsx
      Nutrition.jsx
      FutureSelf.jsx
      Activity.jsx
      Gamification.jsx
      Transparency.jsx
      Family.jsx
      Settings.jsx
    components/
      Sidebar.jsx
      TopBar.jsx
      UserSelector.jsx
      StreakBadge.jsx
      AgeComparison.jsx
      SubSystemAges.jsx
      MetricCard.jsx
      HabitSliders.jsx
      RiskChart.jsx
      WellnessGauge.jsx
      ChatInterface.jsx
      FileUpload.jsx
      ManualEntryForm.jsx
      NutritionTracker.jsx
      NutritionTargets.jsx
      MealAnalysis.jsx
      XPBar.jsx
      DailyChecklist.jsx
      AchievementGrid.jsx
      Leaderboard.jsx
      WeeklyChallenge.jsx
      WorkoutLog.jsx
      WorkoutSummary.jsx
      StepProgressRing.jsx
      WorkoutTargets.jsx
      ActivityNudge.jsx
      ReminderCards.jsx
      AlertBanner.jsx
      SpecialistCards.jsx
      FamilyDashboard.jsx
      AgentTrace.jsx
```

---

## package.json

```json
{
  "name": "eirview-frontend",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "react-router-dom": "^7.0.0",
    "recharts": "^2.15.0",
    "axios": "^1.7.0",
    "zustand": "^5.0.0",
    "lucide-react": "^0.500.0",
    "react-webcam": "^7.2.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.5.0",
    "vite": "^6.0.0",
    "tailwindcss": "^4.0.0",
    "@tailwindcss/vite": "^4.0.0"
  }
}
```

---

## vite.config.js

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: { proxy: { '/api': 'http://localhost:8000' } }
})
```

---

## index.html

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>EirView — Health Intelligence</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
```

---

## src/index.css

```css
@import "tailwindcss";

body {
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
}

/* Scrollbar styling */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

/* Typing animation for chat */
@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}
.typing-dot {
  animation: blink 1.4s infinite both;
}
.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }
```

---

## src/main.jsx

```jsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

---

## src/api.js — All Backend Calls

Create this file with ALL of these exports. Every function must be present.

```javascript
import axios from 'axios';

const API = axios.create({ baseURL: 'http://localhost:8000' });

// Users
export const getUsers = () => API.get('/api/users');
export const createUser = (data) => API.post('/api/users', data);

// Profile
export const getProfile = (userId) => API.get(`/api/profile/${userId}`);
export const updateProfile = (userId, data) => API.put(`/api/profile/${userId}`, data);

// Dashboard
export const getDashboard = (userId) => API.get(`/api/dashboard/${userId}`);

// Data ingestion
export const uploadFile = (formData) => API.post('/api/ingest', formData, { headers: { 'Content-Type': 'multipart/form-data' } });
export const uploadFaceAge = (formData) => API.post('/api/face-age', formData, { headers: { 'Content-Type': 'multipart/form-data' } });
export const uploadAppleHealth = (formData) => API.post('/api/apple-health', formData, { headers: { 'Content-Type': 'multipart/form-data' } });

// Meal & Water
export const uploadMeal = (formData) => API.post('/api/meal', formData, { headers: { 'Content-Type': 'multipart/form-data' } });
export const logWater = (userId, amount_ml) => API.post('/api/water', { user_id: userId, amount_ml });

// Simulation
export const simulate = (userId, changes) => API.post('/api/simulate', { user_id: userId, changes });

// Gamification
export const getGamification = (userId) => API.get(`/api/gamification/${userId}`);
export const logAction = (userId, action) => API.post(`/api/gamification/${userId}/action`, { action });
export const getLeaderboard = () => API.get('/api/gamification/leaderboard');

// Family
export const createFamily = (name, userId) => API.post('/api/family', { name, created_by: userId });
export const joinFamily = (joinCode, userId, relationship, privacy) => API.post('/api/family/join', { join_code: joinCode, user_id: userId, relationship, privacy_level: privacy });
export const getFamily = (familyId) => API.get(`/api/family/${familyId}`);

// Reminders & Alerts
export const getReminders = (userId) => API.get(`/api/reminders/${userId}`);
export const getAlerts = (userId) => API.get(`/api/alerts/${userId}`);
export const notifyDoctor = (userId, alertId) => API.post(`/api/alerts/${userId}/notify-doctor`, { alert_id: alertId });
export const getSpecialists = (userId) => API.get(`/api/specialists/${userId}`);

// Workouts
export const getWorkouts = (userId) => API.get(`/api/workouts/${userId}`);
export const logWorkout = (userId, data) => API.post(`/api/workouts/${userId}`, data);
export const getWorkoutSummary = (userId) => API.get(`/api/workouts/${userId}/summary`);
export const getWorkoutTargets = (userId) => API.get(`/api/workouts/${userId}/targets`);

// Transparency
export const getTransparency = (userId) => API.get(`/api/transparency/${userId}`);

// SSE Chat helper
export const streamChat = async (endpoint, userId, message, history, onText, onTool, onDone) => {
  const response = await fetch(`http://localhost:8000/api/chat/${endpoint}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id: userId, message, history })
  });

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    const lines = decoder.decode(value).split('\n');
    for (const line of lines) {
      if (!line.startsWith('data: ')) continue;
      try {
        const data = JSON.parse(line.slice(6));
        if (data.type === 'text') onText(data.content);
        else if (data.type === 'tool') onTool(data);
        else if (data.type === 'done') onDone();
      } catch {}
    }
  }
};
```

---

## src/store.js — Zustand Store

```javascript
import { create } from 'zustand';

const useStore = create((set, get) => ({
  // Current user
  selectedUserId: 'zahoor',
  users: [],
  setSelectedUser: (id) => set({ selectedUserId: id }),
  setUsers: (users) => set({ users }),

  // Profile data
  profile: null,
  setProfile: (profile) => set({ profile }),

  // Dashboard data
  dashboard: null,
  setDashboard: (data) => set({ dashboard: data }),

  // Gamification
  gamification: null,
  setGamification: (data) => set({ gamification: data }),

  // Reminders & Alerts
  reminders: [],
  alerts: [],
  setReminders: (r) => set({ reminders: r }),
  setAlerts: (a) => set({ alerts: a }),

  // UI state
  loading: false,
  setLoading: (l) => set({ loading: l }),
  toast: null,
  showToast: (message, type = 'success') => {
    set({ toast: { message, type } });
    setTimeout(() => set({ toast: null }), 5000);
  },
}));

export default useStore;
```

---

## src/App.jsx

```jsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { useEffect } from 'react';
import Sidebar from './components/Sidebar';
import TopBar from './components/TopBar';
import AlertBanner from './components/AlertBanner';
import Dashboard from './pages/Dashboard';
import DataIngest from './pages/DataIngest';
import Insights from './pages/Insights';
import Mental from './pages/Mental';
import Nutrition from './pages/Nutrition';
import FutureSelf from './pages/FutureSelf';
import Activity from './pages/Activity';
import Gamification from './pages/Gamification';
import Transparency from './pages/Transparency';
import Family from './pages/Family';
import Settings from './pages/Settings';
import useStore from './store';
import { getUsers, getDashboard, getGamification, getAlerts } from './api';

export default function App() {
  const { selectedUserId, setUsers, setDashboard, setGamification, setAlerts, toast } = useStore();

  useEffect(() => {
    getUsers().then(r => setUsers(r.data));
  }, []);

  useEffect(() => {
    if (!selectedUserId) return;
    getDashboard(selectedUserId).then(r => setDashboard(r.data));
    getGamification(selectedUserId).then(r => setGamification(r.data));
    getAlerts(selectedUserId).then(r => setAlerts(r.data));
  }, [selectedUserId]);

  return (
    <BrowserRouter>
      <div className="flex min-h-screen bg-slate-50">
        <Sidebar />
        <div className="flex-1 ml-64">
          <TopBar />
          <AlertBanner />
          <main className="max-w-7xl mx-auto px-6 py-6">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/ingest" element={<DataIngest />} />
              <Route path="/insights" element={<Insights />} />
              <Route path="/mental" element={<Mental />} />
              <Route path="/nutrition" element={<Nutrition />} />
              <Route path="/future" element={<FutureSelf />} />
              <Route path="/activity" element={<Activity />} />
              <Route path="/gamification" element={<Gamification />} />
              <Route path="/transparency" element={<Transparency />} />
              <Route path="/family" element={<Family />} />
              <Route path="/settings" element={<Settings />} />
            </Routes>
          </main>
        </div>

        {/* Toast notification — fixed top-right, auto-dismiss after 5s */}
        {toast && (
          <div className={`fixed top-4 right-4 z-50 px-4 py-3 rounded-lg shadow-lg text-white text-sm font-medium transition-all ${
            toast.type === 'success' ? 'bg-emerald-500' :
            toast.type === 'error' ? 'bg-red-500' :
            toast.type === 'warning' ? 'bg-amber-500' : 'bg-blue-500'
          }`}>
            {toast.message}
          </div>
        )}
      </div>
    </BrowserRouter>
  );
}
```

---

## COMPONENT SPECIFICATIONS

Every component below must be created as a complete, working React component. Do NOT leave any as stubs. Use the exact Tailwind classes specified. Import icons from `lucide-react`. Handle loading, empty, and error states in every component.

---

### components/Sidebar.jsx

**Behavior**: Fixed left sidebar, width `w-64`, full height `h-screen`, bg `bg-slate-900`, text white. Sticky/fixed position so it stays while scrolling.

**Structure**:
1. **Logo area** (top, `p-6`): Text "EirView" in `text-xl font-bold text-white`. Below it in `text-xs text-slate-400`: "Health Intelligence".
2. **Navigation links** (`mt-6 space-y-1 px-3`): Each link is a `NavLink` from react-router-dom. Each link has:
   - Icon (24px, from lucide-react) + label text
   - Classes: `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-slate-300 hover:bg-slate-800 hover:text-white transition`
   - Active state (use NavLink's className function): `bg-slate-800 text-white`
   - Navigation items in order:
     - LayoutDashboard icon -> "Dashboard" -> path "/"
     - Upload icon -> "Data Ingest" -> path "/ingest"
     - Lightbulb icon -> "Insights" -> path "/insights"
     - Brain icon -> "Mental Health" -> path "/mental"
     - Apple icon -> "Nutrition" -> path "/nutrition"
     - Sparkles icon -> "Future Self" -> path "/future"
     - Activity icon -> "Activity" -> path "/activity"
     - Trophy icon -> "Gamification" -> path "/gamification"
     - Search icon -> "Transparency" -> path "/transparency"
3. **Divider**: `border-t border-slate-700 my-4 mx-3`
4. **Bottom links** (same style as nav):
   - Users icon -> "Family" -> path "/family"
   - SettingsIcon icon -> "Settings" -> path "/settings"

---

### components/TopBar.jsx

**Structure**: Horizontal bar at top of main content, `bg-white border-b border-slate-200 px-6 py-3`. Flex row with `justify-between items-center`.

**Left side**: Page title (dynamically set based on current route using `useLocation` from react-router-dom). Map paths to titles:
- "/" -> "Dashboard"
- "/ingest" -> "Data Ingest"
- "/insights" -> "Insights"
- "/mental" -> "Mental Health"
- "/nutrition" -> "Nutrition"
- "/future" -> "Future Self"
- "/activity" -> "Activity"
- "/gamification" -> "Gamification"
- "/transparency" -> "Transparency"
- "/family" -> "Family"
- "/settings" -> "Settings"

Title text: `text-lg font-semibold text-slate-900`

**Right side** (`flex items-center gap-4`):
- `<UserSelector />` component
- `<StreakBadge />` component
- Bell icon button (`text-slate-400 hover:text-slate-600`) with red dot indicator if alerts exist

---

### components/UserSelector.jsx

**Structure**: A `<select>` dropdown styled with `border border-slate-300 rounded-lg px-3 py-1.5 text-sm bg-white`.

**Behavior**:
- Read `users` and `selectedUserId` from Zustand store
- Options: map over `users` array, each `<option value={user.id}>{user.name}</option>`
- On change: call `setSelectedUser(e.target.value)` from store

---

### components/StreakBadge.jsx

**Structure**: Inline flex container with Flame icon + streak number.

**Behavior**:
- Read `gamification` from store
- If gamification exists and `gamification.streak > 0`: Flame icon in `text-orange-500` + `{gamification.streak}` in `text-sm font-semibold text-orange-600`
- If streak is 0 or no data: Flame icon in `text-slate-300` + "0" in `text-slate-400`
- Wrap in a `<div>` with `title` attribute for tooltip: "X-day streak! Complete 3 health actions today to keep it going."

---

### components/AlertBanner.jsx

**Structure**: Renders above page content when alerts exist in the store. Full width banner.

**Behavior**:
- Read `alerts` from store
- If `alerts` is empty or null: render nothing (return null)
- For each alert, render a banner:
  - Container: `bg-red-50 border-l-4 border-red-500 p-4 mb-4`
  - Flex row: AlertTriangle icon (red-500) + message text + action buttons
  - Message: `text-red-800 text-sm font-medium` — "ALERT: {alert.metric} reading of {alert.value} is critically {alert.direction}."
  - Buttons: "Dismiss" (secondary button style) and "Notify Doctor" (red bg button), only show "Notify Doctor" if alert has `doctor_available: true`
  - For PHQ-9 alerts with value > 20: show additional line below in `text-red-700 text-xs mt-2`: "Crisis helplines: Vandrevala Foundation 1860-2662-345 | iCall 9152987821 | AASRA 9820466726"
- "Dismiss" removes that alert from the store's alerts array
- "Notify Doctor" calls `notifyDoctor(userId, alertId)` from api.js

---

### components/ReminderCards.jsx

**Structure**: Horizontal scrollable row of dismissable notification cards.

**Container**: `flex gap-4 overflow-x-auto pb-2 mb-6`. Only render if `reminders` array in store has entries.

**Each card**:
- `flex-shrink-0 w-80 rounded-lg p-4 border-l-4` + bg color based on urgency:
  - urgency "critical" or "overdue": `border-red-500 bg-red-50`
  - urgency "warning" or "due_soon": `border-amber-500 bg-amber-50`
  - urgency "info": `border-blue-500 bg-blue-50`
- Top-right: X button (lucide X icon, `text-slate-400 hover:text-slate-600 cursor-pointer`) to dismiss
- Text: `text-sm text-slate-700` — reminder message
- Below text: `text-xs text-slate-500 mt-1` — due date or context

**Behavior**: Load reminders on mount by calling `getReminders(selectedUserId)` and storing in Zustand. Dismiss removes from local state.

---

### components/AgeComparison.jsx

**Props**: Receives dashboard data (or reads from store).

**Structure**: Three vertical bars side by side inside a card (`bg-white rounded-xl shadow-sm border border-slate-200 p-6`).

**Layout**: `flex items-end justify-center gap-8` with height `h-[280px]`.

**Each bar**:
1. "Chronological" — color `bg-slate-400` — value = `profile.age` (from dashboard data)
2. "Biological" — color `bg-emerald-500` if bio_age < chrono_age (good), `bg-red-500` if bio_age > chrono_age (bad) — value = `dashboard.bio_age_overall`
3. "Face Age" — color `bg-blue-500` — value = `dashboard.face_age` (show "---" if null)

**Bar rendering**:
- Calculate scale: `maxVal = Math.max(age + 10, bio_age + 10, face_age + 10)` (use 0 for null face_age)
- Each bar: `w-16 rounded-t-lg` with height as percentage of maxVal relative to container height (e.g., `style={{ height: '${(value / maxVal) * 100}%' }}`)
- Below each bar: value in `font-mono font-medium text-lg text-slate-900` + label in `text-xs text-slate-500 mt-1`

**Below the bars**: A summary sentence:
- If bio_age < chrono_age: `text-emerald-600 font-medium` — "You are X.X years younger than your biological age"
- If bio_age > chrono_age: `text-red-600 font-medium` — "You are X.X years older biologically"
- Use `.toFixed(1)` for the difference

---

### components/SubSystemAges.jsx

**Props**: Receives dashboard data (or reads from store).

**Structure**: Card with 4 horizontal progress bars.

**Each bar** represents a body subsystem:
1. Cardiovascular — icon: Heart — value: `chrono_age + cv_delta`
2. Metabolic — icon: Flame — value: `chrono_age + met_delta`
3. Musculoskeletal — icon: Bone — value: `chrono_age + msk_delta`
4. Neurological — icon: Brain — value: `chrono_age + neuro_delta`

**Bar layout** (each row, `space-y-4`):
- Row: `flex items-center gap-3`
- Icon (20px, `text-slate-500`) + Name (`text-sm font-medium text-slate-700 w-36`) + Progress bar (flex-1) + Value (`font-mono text-sm w-16 text-right`)
- Progress bar: outer `h-3 bg-slate-100 rounded-full`, inner `h-3 rounded-full` with width proportional to subsystem age / max_age_scale
- Inner bar color:
  - Delta < 0 (younger than chrono): `bg-emerald-500`
  - Delta 0 to +2: `bg-amber-500`
  - Delta > +2: `bg-red-500`
- Below bar: small text showing delta: e.g., "1.2 years younger" in emerald or "0.8 years older" in red

---

### components/MetricCard.jsx

**Props**: `{ label, value, unit, delta, icon: Icon, status }`

**Structure**: Card `bg-white rounded-xl shadow-sm border border-slate-200 p-4`.

**Layout**:
- Top row: `flex items-center justify-between`
  - Left: Icon component (20px) in `text-slate-400`
  - Right: Status dot — a small circle `w-2.5 h-2.5 rounded-full`:
    - status "good": `bg-green-500`
    - status "warning": `bg-amber-500`
    - status "critical": `bg-red-500`
    - status "neutral": `bg-slate-400`
- Label: `text-sm text-slate-500 mt-3`
- Value: `text-2xl font-mono font-medium tabular-nums text-slate-900 mt-1` — display using `toLocaleString()` for large numbers, `.toFixed(1)` for decimals
- Bottom row: unit in `text-xs text-slate-400` + delta (if provided):
  - Positive improvement: `text-green-600 text-xs font-medium` with ArrowUp icon (12px)
  - Negative decline: `text-red-600 text-xs font-medium` with ArrowDown icon (12px)

---

### components/StepProgressRing.jsx

**Props**: `{ current, goal, size }` (size defaults to 160)

**Structure**: SVG circular progress indicator.

**SVG details**:
- ViewBox: `0 0 ${size} ${size}`
- Center: `size / 2`, Radius: `(size - 16) / 2`, strokeWidth: 8
- Background circle: stroke `#e2e8f0` (slate-200), fill none
- Progress arc: Use SVG `stroke-dasharray` and `stroke-dashoffset` to show percentage
  - Color: `#10b981` (emerald-500) if progress > 70%, `#f59e0b` (amber-500) if 40-70%, `#ef4444` (red-500) if < 40%
  - `stroke-linecap: round`
  - Add CSS transition for animation on mount
- Center text (SVG `<text>`):
  - Current steps: `font-mono font-medium` size 20
  - "/" + goal: `text-slate-400` size 12
- Below the SVG ring: `text-sm text-slate-500 text-center` — "steps today"

---

### components/WorkoutSummary.jsx

**Props**: Receives workout summary data.

**Structure**: Card containing a Recharts `BarChart`.

**Chart**:
- `<ResponsiveContainer width="100%" height={250}>`
- `<BarChart>` with data for Mon-Sun (7 bars)
- X-axis: day names (Mon, Tue, Wed, Thu, Fri, Sat, Sun)
- Y-axis: minutes
- Bars: `fill="#10b981"` (emerald-500), `radius={[4, 4, 0, 0]}`
- `<Tooltip>` and `<CartesianGrid strokeDasharray="3 3">`
- Below chart: summary text — "X sessions | Y total minutes | Z calories burned this week" in `text-sm text-slate-600`

---

### components/ActivityNudge.jsx

**Props**: `{ currentSteps, stepGoal, message }`

**Behavior**: Only renders if `currentSteps < stepGoal`.

**Structure**: Card with amber left border `border-l-4 border-amber-500 bg-amber-50 p-4 rounded-r-lg`.
- Footprints icon (amber-500) + message text
- Message example: "You're 2,766 steps behind your goal. A 20-minute walk would get you there!"
- `text-sm text-amber-800`

---

### components/WorkoutTargets.jsx

**Props**: Receives workout targets data (array of recommended workouts).

**Structure**: Card with list of recommended workouts.

**Each workout recommendation**:
- Icon (based on type: running = PersonStanding, yoga = Heart, strength = Dumbbell) + workout name + frequency
- Below: `text-xs text-slate-500` — reasoning (e.g., "your resting HR is 67, aerobic exercise will lower it + help with LDL 121")
- Separated by `border-b border-slate-100` between items

---

### components/SpecialistCards.jsx

**Behavior**: Only renders if specialist recommendations exist. Fetch from `getSpecialists(userId)` on mount.

**Structure**: Section with heading "Specialist Recommendations" + cards.

**Each card**:
- Border color: `border-amber-500` for "recommended", `border-red-500` for "urgent"
- Content: specialist type (e.g., "Cardiologist"), reason, nearby hospitals list
- "Schedule Reminder" secondary button

---

### components/HabitSliders.jsx

**Structure**: Card with 5 range sliders and a Simulate button.

**Sliders** (each row: `space-y-6`):
1. **Sleep**: range 4-10, step 0.5, label "Sleep (hours)", display current value + slider value
2. **Exercise**: range 0-14, step 1, label "Exercise (hours/week)"
3. **Diet**: range 1-4, step 1, label "Diet Quality" — map 1="Poor", 2="Average", 3="Good", 4="Excellent"
4. **Stress**: range 1-10, step 1, label "Stress Level"
5. **Screen Time**: range 0-16, step 1, label "Screen Time (hours)"
6. **Exam Stress**: range 1-10, step 1, label "Academic Stress" — only show if profile.academic_year exists and is not "Not a student"

**Each slider row**:
- Label on left (`text-sm font-medium text-slate-700`)
- `<input type="range">` with Tailwind styling: `w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-emerald-500`
- Right side: current value in `text-sm text-slate-500` + "(current: X)" in `text-xs text-slate-400`

**Simulate button**: `bg-emerald-500 hover:bg-emerald-600 text-white rounded-lg px-6 py-2.5 font-medium transition mt-4`
- On click: call `simulate(userId, { sleep, exercise, diet, stress, screen_time, exam_stress })` from api.js
- While loading: show spinner in button
- Result: render a result card below:
  - If improvement: `bg-emerald-50 border border-emerald-200 rounded-lg p-4` — "Bio age: 17.2 -> 15.8 (improvement: 1.4 years)" in `text-emerald-700 font-medium`
  - If worse: `bg-red-50 border border-red-200 rounded-lg p-4` — red text

---

### components/RiskChart.jsx

**Props**: Receives risk projection data (array of yearly data points with 4 risk values each).

**Structure**: Card with Recharts `LineChart`.

**Chart**:
- `<ResponsiveContainer width="100%" height={350}>`
- `<LineChart>` with data: array of `{ year: 1, diabetes: X, cvd: X, metabolic: X, mental: X }` for years 1-15
- 4 `<Line>` components:
  - Diabetes: `stroke="#3b82f6"` (blue-500), name "Diabetes"
  - CVD: `stroke="#ef4444"` (red-500), name "Cardiovascular"
  - Metabolic: `stroke="#f59e0b"` (amber-500), name "Metabolic Syndrome"
  - Mental Decline: `stroke="#8b5cf6"` (purple-500), name "Mental Decline"
- Each line: `type="monotone"`, `strokeWidth={2}`, `dot={{ r: 3 }}`, `activeDot={{ r: 5 }}`
- `<XAxis dataKey="year" label={{ value: "Year", position: "bottom" }} />`
- `<YAxis domain={[0, 50]} tickFormatter={(v) => v + '%'} />`
- `<Tooltip formatter={(value) => value.toFixed(1) + '%'} />`
- `<Legend />`
- `<CartesianGrid strokeDasharray="3 3" />`
- Animate on mount: `isAnimationActive={true}`

---

### components/WellnessGauge.jsx

**Props**: `{ score, breakdown }` — score is 0-100, breakdown is array of `{ name, penalty }`

**Structure**: Card with SVG gauge + breakdown list.

**SVG Gauge**:
- SVG viewBox `0 0 200 160`
- Arc: 270-degree arc (from 135deg to 405deg), radius 80, center at (100, 100)
- Background arc: stroke `#e2e8f0`, strokeWidth 12
- Foreground arc: stroke-dasharray/offset based on score percentage
  - Color: `#ef4444` (red) if score 0-30, `#f59e0b` (amber) if 31-60, `#10b981` (emerald) if 61-100
  - stroke-linecap: round
- Center text: score number in `font-mono text-3xl font-bold`
- Below number: "Mental Wellness" in `text-sm text-slate-500`
- Animate on mount from 0 to actual score

**Breakdown list** (below gauge):
- Each item: `flex justify-between py-1.5 border-b border-slate-100`
- Left: name in `text-sm text-slate-600`
- Right: penalty value in `text-sm font-mono text-red-500` (e.g., "-7.5")

---

### components/ChatInterface.jsx

**Props**: `{ chatType, userId, title, placeholder }`
- chatType: "mental" | "future" | "coach" — passed to `streamChat` as the endpoint
- title: displayed at top of chat area
- placeholder: for the input field

**Structure**: Card with fixed height (`h-[500px]` normally, `h-[600px]` for future self), flex column.

**Layout**:
1. **Header**: `px-4 py-3 border-b border-slate-200` — title text in `font-semibold text-slate-900`
2. **Messages area**: `flex-1 overflow-y-auto p-4 space-y-4` — scrolls to bottom on new message
3. **Input area**: `border-t border-slate-200 p-4 flex gap-2`

**Messages**:
- User messages: `flex justify-end` -> bubble `bg-emerald-100 text-emerald-900 rounded-2xl rounded-br-md px-4 py-2.5 max-w-[75%] text-sm`
- Assistant messages: `flex justify-start` -> bubble `bg-white border border-slate-200 text-slate-700 rounded-2xl rounded-bl-md px-4 py-2.5 max-w-[75%] text-sm`
- Tool call cards: `bg-amber-50 border border-amber-200 rounded-lg px-3 py-2 text-xs text-amber-700 my-1` — show tool name + brief result

**Typing indicator**: 3 dots in assistant bubble style, each dot is `w-2 h-2 bg-slate-400 rounded-full typing-dot` (uses the CSS animation defined in index.css).

**Input**: `<input>` with classes `flex-1 border border-slate-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 outline-none` + Send button with `bg-emerald-500 hover:bg-emerald-600 text-white rounded-lg px-4 py-2 font-medium transition`. Send icon (lucide Send).

**Behavior**:
- Maintain local state: `messages` array of `{ role: 'user'|'assistant'|'tool', content: string }`
- On send:
  1. Add user message to messages array
  2. Clear input
  3. Show typing indicator
  4. Call `streamChat(chatType, userId, message, messages, onText, onTool, onDone)`
  5. `onText`: append to current assistant message (streaming effect)
  6. `onTool`: add a tool message card
  7. `onDone`: hide typing indicator
  8. Auto-scroll to bottom after each update
- Enter key also sends (not shift+enter)
- Disable send button while streaming

---

### components/FileUpload.jsx

**Props**: `{ onUpload, accept, label, endpoint }`

**Structure**: Drag-and-drop zone.

**Drop zone**:
- Default: `border-2 border-dashed border-slate-300 rounded-xl p-8 text-center cursor-pointer hover:border-slate-400 transition`
- On drag over: `border-emerald-500 bg-emerald-50`
- Icon: Upload icon (lucide, 48px, `text-slate-300`)
- Text: `text-sm text-slate-500` — "Drag and drop your file here, or click to browse"
- Subtext: `text-xs text-slate-400 mt-1` — "Accepted: {accept}" (e.g., "PDF, PNG, JPG, XML")
- Hidden `<input type="file">` triggered by click on the zone

**After file selected**:
- Show file name + size in `text-sm text-slate-700` with FileText icon
- Upload button: `bg-emerald-500 hover:bg-emerald-600 text-white rounded-lg px-4 py-2 font-medium transition mt-3`

**During upload**: Spinner animation + "Processing..." text

**On success**: Call `onUpload(responseData)` prop. The parent component handles displaying the results.

**On error**: Red text `text-red-500 text-sm` with error message + "Retry" button.

---

### components/ManualEntryForm.jsx

**Structure**: Accordion-style form with collapsible sections.

**Accordion section** (reusable pattern):
- Header: `flex items-center justify-between cursor-pointer py-3 border-b border-slate-200`
  - Section name in `font-medium text-slate-700`
  - ChevronRight icon that rotates 90deg when open: `transform transition-transform ${open ? 'rotate-90' : ''}`
- Body: conditionally rendered, `py-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4`

**Sections** (each with specific fields):

1. **Blood Work** (section header click toggles open/closed):
   - Fields: LDL (number), HDL (number), Triglycerides (number), Total Cholesterol (number), Fasting Glucose (number), HbA1c (number), Vitamin D (number), Iron/Ferritin (number), Vitamin B12 (number), TSH (number), CRP (number), Hemoglobin (number)
   - Each field: `<label class="text-xs text-slate-500">` + `<input type="number" class="border border-slate-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 w-full">`

2. **Body Composition**:
   - Fields: Weight kg (number), Height cm (number), BMI (number, computed if possible), Body Fat % (number), Muscle Mass Ratio (number), Waist Circumference (number), Hip Circumference (number)

3. **Vitals (HealthKit)**:
   - Fields: Resting HR (number), HRV ms (number), VO2max (number), SpO2 % (number), Blood Pressure Systolic (number), Blood Pressure Diastolic (number), Respiratory Rate (number)

4. **Lifestyle**:
   - Exercise hours/week (number), Sleep hours average (number), Sleep target (number), Smoking (`<select>`: Never/Former/Current), Alcohol drinks/week (number), Screen time hours/day (number), Stress level 1-10 (range), Water intake ml/day (number)

5. **Academic** (collapsible section, open by default):
   - Current GPA/CGPA (number, step 0.01, min 0, max 4.0), Study hours per day (number, step 0.5), Exam/Academic stress 1-10 (range input with labels "Relaxed" to "Overwhelming"), Academic year (`<select>`: Year 1/Year 2/Year 3/Year 4/Postgrad/Not a student)
   - Header: "Academic" with a graduation cap icon (SVG)
   - If "Not a student" is selected, hide GPA, study hours, and exam stress fields

6. **Family History**:
   - Checkboxes (`<input type="checkbox">`): Diabetes, Heart Disease, Hypertension, Cancer, Mental Health Conditions, Stroke, Kidney Disease
   - Each: `flex items-center gap-2` with `text-sm text-slate-700`

7. **Medical Contacts**:
   - Doctor name (text), Doctor email (email), Doctor phone (tel)
   - Emergency contact name (text), Emergency phone (tel)

**Save button** at bottom: `bg-emerald-500 hover:bg-emerald-600 text-white rounded-lg px-6 py-2.5 font-medium transition w-full md:w-auto`
- On click: call `updateProfile(userId, formData)` from api.js
- On success: `showToast('Profile updated successfully')` from store
- On error: `showToast('Failed to update profile', 'error')`

**Initialize form**: On mount, call `getProfile(userId)` and populate all fields with existing values.

---

### components/NutritionTargets.jsx

**Props**: Receives nutrition target data.

**Structure**: Row of 5 mini cards showing daily macro targets.

**Layout**: `grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4`

**Each card** (`bg-white rounded-xl shadow-sm border border-slate-200 p-4 text-center`):
- Macro name: `text-xs text-slate-500 font-medium uppercase tracking-wide`
- Current/Target: `text-lg font-mono font-medium tabular-nums text-slate-900` — "1575/2205"
- Progress bar: `h-2 bg-slate-100 rounded-full mt-2` with inner `h-2 rounded-full` colored:
  - < 50%: `bg-red-400`
  - 50-80%: `bg-amber-400`
  - 80-100%: `bg-emerald-400`
  - > 100%: `bg-red-500` (over target)
- Percentage: `text-xs text-slate-500 mt-1` — "71%"
- Checkmark if within healthy range

**Below the cards**: Note text in `text-sm text-slate-500 italic` — e.g., "Sat fat limited to 13g because your LDL is 121 mg/dL"

---

### components/NutritionTracker.jsx

**Structure**: Water tracking section.

**Layout**: Card with water drop icon, progress bar, and quick-add buttons.

**Content**:
- Header: Droplets icon (blue-500) + "Water Tracker" in `font-medium text-slate-700`
- Current: `text-2xl font-mono font-medium text-slate-900` — "1,750ml" + `text-sm text-slate-500` — "/ 2,450ml"
- Progress bar: `h-3 bg-slate-100 rounded-full` with inner `h-3 bg-blue-500 rounded-full` + percentage
- Quick-add buttons: `flex gap-2 mt-3`
  - "+250ml" button (secondary style)
  - "+500ml" button (secondary style)
  - "Custom" button (secondary style) — opens small input for custom amount
- Each button calls `logWater(userId, amount)` from api.js

---

### components/MealAnalysis.jsx

**Props**: `{ analysis }` — the response from meal upload/analysis

**Structure**: Card showing analyzed meal data in a table.

**Table**:
- Headers: Item, Portion, Calories, Protein, Sat Fat — `text-xs text-slate-500 uppercase tracking-wide font-medium`
- Rows: each item with values in `font-mono text-sm`
  - Sub-row: USDA code reference in `text-xs text-slate-400 pl-4` — e.g., "USDA #172818"
- Footer row: TOTAL in bold with summed values
- Separator: `border-t-2 border-slate-300` before total row

**Flags section** (below table):
- Each flag: icon + text
  - Warning (exceeds target): AlertTriangle icon (amber) + `text-amber-700 text-sm`
  - Good (within target): CheckCircle icon (emerald) + `text-emerald-700 text-sm`
- Score: `text-lg font-semibold` — "Score: 7.2/10"

---

### components/XPBar.jsx

**Props**: `{ level, levelName, currentXP, nextLevelXP }`

**Structure**: Level display + XP progress bar.

**Layout**:
- Level: `text-2xl font-bold text-slate-900` — "Level {level}"
- Level name: `text-sm text-slate-500` — e.g., "Data Conscious"
- Progress bar: `h-4 bg-slate-100 rounded-full mt-3` with inner `h-4 bg-emerald-500 rounded-full transition-all` width = `(currentXP / nextLevelXP) * 100%`
- Below bar: `text-xs text-slate-500` — "{currentXP} / {nextLevelXP} XP"

---

### components/DailyChecklist.jsx

**Props**: Receives checklist data (array of `{ action, xp, completed }`)

**Structure**: Card with "Today's Health Actions" heading + list of checkable items.

**Each item**:
- `flex items-center gap-3 py-2.5 border-b border-slate-100`
- Checkbox: if completed, CheckCircle icon (`text-emerald-500`); if not, Circle icon (`text-slate-300`)
- Action text: `text-sm` — struck through + `text-slate-400` if completed, `text-slate-700` if not
- XP badge: `text-xs bg-emerald-100 text-emerald-700 px-2 py-0.5 rounded-full` — "+{xp} XP"
- Clicking an uncompleted item calls `logAction(userId, action)` from api.js and marks it complete

**Footer**: `text-xs text-slate-500 mt-2` — "Complete 3 actions for streak day"

---

### components/AchievementGrid.jsx

**Props**: Receives achievements data (array of `{ id, name, icon_emoji, earned, description }`)

**Structure**: Grid of achievement badges.

**Layout**: `grid grid-cols-5 gap-4`

**Each badge** (`text-center`):
- Circle: `w-16 h-16 rounded-full flex items-center justify-center mx-auto text-2xl`
  - If earned: `bg-emerald-100 border-2 border-emerald-500`
  - If locked: `bg-slate-100 border-2 border-slate-200 opacity-40 grayscale`
- Icon: emoji character inside the circle
- Name: `text-xs text-slate-700 mt-1 font-medium` (or `text-slate-400` if locked)

**Summary**: `text-sm text-slate-500 mt-4` — "Earned: X/Y"

---

### components/Leaderboard.jsx

**Structure**: Table showing family/global leaderboard.

**Behavior**: Fetch from `getLeaderboard()` on mount.

**Table**:
- Headers: #, Name, Level, Streak, XP, Bio Age Delta — styled `text-xs text-slate-500 uppercase tracking-wide font-medium text-left py-3 border-b border-slate-200`
- Rows: `py-3 border-b border-slate-100`
  - Rank: `font-medium text-slate-900` — highlight #1 with `text-amber-500`
  - Name: `text-sm text-slate-700`
  - Level: `text-sm text-slate-600`
  - Streak: fire emoji + number in `text-sm`
  - XP: `font-mono text-sm text-slate-700`
  - Bio Age Delta: `font-mono text-sm` — emerald if negative (younger), red if positive (older)

---

### components/WeeklyChallenge.jsx

**Props**: `{ name, description, current, target }`

**Structure**: Card with challenge info + progress bar.

**Content**:
- Target icon (amber-500) + challenge name in `font-medium text-slate-700`
- Description: `text-sm text-slate-500`
- Progress bar: `h-3 bg-slate-100 rounded-full mt-3` with inner `h-3 bg-amber-500 rounded-full`
- Below bar: `text-sm text-slate-600` — "{current}/{target} days"

---

### components/WorkoutLog.jsx

**Props**: Receives array of workout entries.

**Structure**: List of recent workouts.

**Each entry** (`py-4 border-b border-slate-100`):
- Top row: `flex items-center justify-between`
  - Left: workout type icon + type name in `font-medium text-slate-700` + date in `text-xs text-slate-400 ml-2`
  - Right: `text-sm text-slate-500` — duration + calories
- Bottom row: `text-xs text-emerald-600 mt-1` — Impact line, e.g., "Impact: Cardiovascular age -0.3 years"

---

### components/FamilyDashboard.jsx

**Props**: Receives family data.

**Structure**: Shows family member cards, health alerts, comparison, and join code.

**Member cards** (`grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4`):
- Each card: name, relationship, bio age, streak, privacy level indicator
- Privacy: if "summary" — show only bio age + streak; if "full" — show all metrics; if "minimal" — show only streak

**Family health alerts**: derived conditions section — amber cards showing shared family risk factors

**Join code**: `bg-slate-100 rounded-lg px-4 py-3 text-center font-mono text-lg text-slate-700` — the code with a "Copy" button

**Leave Family**: `text-red-500 text-sm hover:text-red-700 cursor-pointer mt-4` — "Leave Family"

---

### components/AgentTrace.jsx

**Props**: Receives transparency log data.

**Structure**: Table with expandable rows.

**Table columns**: Timestamp, Agent, Tool, Model, Latency

**Row styling** by model:
- Claude calls: `bg-blue-50` (very subtle)
- Gemini calls: `bg-purple-50`
- Deterministic (no model): `bg-slate-50`

**Each row**:
- Timestamp: `font-mono text-xs text-slate-500`
- Agent: `text-sm text-slate-700 font-medium`
- Tool: `text-sm text-slate-600 font-mono`
- Model: Badge — `px-2 py-0.5 rounded-full text-xs font-medium` — blue bg for Claude, purple for Gemini, gray for deterministic
- Latency: `font-mono text-xs` — colored red if > 3s, amber if > 1s, green if < 1s

**Expandable**: Click row to expand and show full tool input/output JSON in `bg-slate-50 p-3 rounded text-xs font-mono overflow-x-auto whitespace-pre-wrap`

**Load More** button at bottom if more entries available.

---

## PAGE IMPLEMENTATIONS

---

### pages/Dashboard.jsx

The most important page. Shows everything at a glance. Read dashboard data from Zustand store.

**Layout (top to bottom, full code required)**:

1. **ReminderCards** — horizontal scrollable row, only if reminders exist. Fetch reminders on mount.
2. **Age section**: `grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6`
   - Left (1 col): `<AgeComparison />` — reads from `dashboard`
   - Right (2 cols, `lg:col-span-2`): `<SubSystemAges />` — reads from `dashboard`
3. **Metrics grid**: `grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6`
   - 8 MetricCards, each pulling from `dashboard.metrics`:
     - Resting HR (Heart icon, bpm)
     - HRV (Activity icon, ms)
     - Steps (Footprints icon)
     - Sleep (Moon icon, hours)
     - VO2max (Wind icon)
     - SpO2 (Droplets icon, %)
     - Exercise Minutes (Timer icon, min)
     - Flights Climbed (TrendingUp icon)
4. **Activity section**: `grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6`
   - Left (1 col): `<StepProgressRing current={dashboard.metrics.steps} goal={dashboard.step_goal || 7500} size={200} />`
   - Right (2 cols): `<WorkoutSummary />` + `<ActivityNudge />` if steps behind goal
5. **SpecialistCards** — only if specialist data exists
6. **Cross-domain insight**: `bg-white rounded-xl shadow-sm border border-slate-200 p-6 mt-6` with a Brain icon and `text-sm text-slate-600 italic` AI-generated insight text from `dashboard.cross_domain_insight`

**Loading state**: If `dashboard` is null, show a grid of 8 skeleton cards (pulsing `bg-slate-200 animate-pulse rounded-xl h-32`).

**Empty state**: If dashboard loads but has no data, show centered message: "No health data yet. Go to Data Ingest to add your first data."

---

### pages/DataIngest.jsx

**Layout (top to bottom)**:

1. **Data source selector**: `grid grid-cols-2 md:grid-cols-4 gap-4 mb-6`
   - 4 cards, each clickable, one highlighted when selected:
     - "Blood Report" — FileText icon — accepts PDF
     - "Cult.fit Report" — Image icon — accepts PNG/JPG
     - "Apple Health" — Smartphone icon — accepts XML
     - "Face Age Selfie" — Camera icon — accepts JPG/PNG or webcam
   - Selected card: `ring-2 ring-emerald-500 bg-emerald-50`
   - Unselected: `bg-white border border-slate-200 hover:border-slate-300 cursor-pointer`

2. **FileUpload component**: Renders below source selector. The `endpoint` prop changes based on selected source:
   - Blood Report -> `uploadFile`
   - Cult.fit -> `uploadFile`
   - Apple Health -> `uploadAppleHealth`
   - Face Age -> `uploadFaceAge`

3. **Upload results**: When upload completes, show extracted data in a results table:
   - For blood report: table of metric name, value, unit, reference range, flag (green check / red flag)
   - For face age: large display of estimated face age + comparison with chrono age
   - For Apple Health: summary of imported records count

4. **Divider**: `border-t border-slate-200 my-8`

5. **ManualEntryForm**: Full manual entry form component

---

### pages/Insights.jsx

**Layout (top to bottom)**:

1. **Health Narrative**: `bg-white rounded-xl shadow-sm border border-slate-200 p-6 mb-6 border-l-4 border-l-emerald-500`
   - Text from `dashboard.narrative` (or fetch separately)
   - Styled: `text-sm text-slate-600 italic leading-relaxed`
   - If no narrative: "Complete your profile to get a personalized health narrative."

2. **HabitSliders**: Full simulation component. Fetch current values from profile to set initial slider positions.

3. **RiskChart**: 15-year risk projection chart. Data from `dashboard.risk_projections` or fetch from insights endpoint.

4. **WorkoutTargets**: Recommended workouts based on profile analysis.

---

### pages/Mental.jsx

**Layout**: `grid grid-cols-1 lg:grid-cols-3 gap-6`

- Left (1 col):
  - `<WellnessGauge score={dashboard.wellness_score} breakdown={dashboard.wellness_breakdown} />`
  - Below gauge (if profile has academic data): **Academic Stress Card** in `bg-amber-50 border border-amber-200 rounded-xl p-4 mt-4`
    - Header: "Academic Pressure" in `text-sm font-semibold text-amber-800` with graduation cap icon
    - Show: GPA badge (`bg-white rounded-full px-3 py-1 text-sm font-medium`), Study hours/day, Exam stress as mini progress bar (amber-500), Academic year
    - If exam_stress > 7: show warning text in `text-amber-700 text-xs mt-2`: "High academic stress detected — this may be affecting your overall wellness score."
    - If exam_stress > 7 AND sleep < 6h: show burnout alert in `text-red-600 text-xs mt-1 font-medium`: "Burnout risk: High study load + insufficient sleep. Consider talking to the coach about balance strategies."
- Right (2 cols, `lg:col-span-2`): `<ChatInterface chatType="mental" userId={selectedUserId} title="Mental Health Chat" placeholder="How are you feeling today?" />`

If no wellness data: show the gauge with score 0 and message "Complete a mental health check-in to see your wellness score."

---

### pages/Nutrition.jsx

**Layout (top to bottom)**:

1. **NutritionTargets**: Daily macro targets with progress bars. Fetch from dashboard or nutrition endpoint.
2. **NutritionTracker**: Water tracking section.
3. **Meal upload/input section**: Card with two options:
   - Photo upload: `<FileUpload>` component for meal photos, calls `uploadMeal`
   - Text input: `<input>` for typing what you ate + "Analyze" button, calls `uploadMeal` with text
4. **MealAnalysis**: Shows latest meal analysis result (if available).
5. **Recent Meals**: List of past meal analyses, most recent first. Each shows date, items, total calories, score.

---

### pages/FutureSelf.jsx

**Layout**:

1. **Info card**: `bg-blue-50 border border-blue-200 rounded-xl p-6 mb-6`
   - Sparkles icon (blue-500) + heading "Talk to Your Future Self"
   - Description: `text-sm text-blue-700` — "You're chatting with {age+15}-year-old you — the version that lived through the next 15 years with your current data."

2. **ChatInterface**: `<ChatInterface chatType="future" userId={selectedUserId} title="Future Self" placeholder="Ask your future self anything..." />`
   - This instance should use the taller height: override with a wrapper div `h-[600px]`

---

### pages/Activity.jsx

**Layout (top to bottom)**:

1. **Top section**: `grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6`
   - Left (1 col): `<StepProgressRing size={200} />` (large) + daily step count text
   - Right (2 cols): `<WorkoutSummary />` — this week's bar chart

2. **WorkoutTargets**: Recommended workouts card. Fetch from `getWorkoutTargets(userId)`.

3. **Log a Workout**: Card with form:
   - Type: `<select>` — Running, Walking, Cycling, Swimming, Yoga, Strength Training, HIIT, Other
   - Duration: `<input type="number">` minutes
   - Calories: `<input type="number">` (optional)
   - "Log Workout" button -> calls `logWorkout(userId, { type, duration_min, calories })`

4. **WorkoutLog**: History list. Fetch from `getWorkouts(userId)`.

5. **ActivityNudge**: Shows at bottom if behind on daily step goal.

---

### pages/Gamification.jsx

**Layout (top to bottom)**:

1. **Top section**: `grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6`
   - Left (1 col): `<XPBar />` with level info from gamification store data
   - Right (2 cols): Streak display with fire emoji + calendar heatmap (simple grid of 7x5 cells, green = active, red = missed, gray = future)

2. **DailyChecklist**: Today's health actions.

3. **WeeklyChallenge**: Current weekly challenge with progress.

4. **AchievementGrid**: Earned badges.

5. **Leaderboard**: Ranking table.

---

### pages/Transparency.jsx

**Layout (top to bottom)**:

1. **Model Usage Summary**: `grid grid-cols-1 md:grid-cols-3 gap-4 mb-6`
   - 3 cards showing Claude 4.6, Gemini 2.5 Flash, and Deterministic stats:
     - Call count, token usage, estimated cost
   - Each card styled with the model's color (blue for Claude, purple for Gemini, gray for deterministic)

2. **AgentTrace**: Full execution log table.

3. **Architecture Description**: Card with `bg-slate-50 rounded-xl p-6` describing the system:
   - "Frontend (React) -> FastAPI Backend -> Agent System (Collector, Mirror, Coach, Social) -> SQLite"
   - Each agent labeled with which model it uses

4. **Alert History**: Table showing past alerts with columns: Date, Metric, Value, Threshold, Doctor Notified (yes/no badge)

---

### pages/Family.jsx

**Two states**:

**State 1 — No family** (check if `profile.family_id` is null):
- Card with two sections separated by "-- or --":
  - **Create a Family**: Family name input + "Create" button -> calls `createFamily(name, userId)`
  - **Join a Family**: Join code input + Relationship dropdown (Father, Mother, Sibling, Spouse, Child, Other) + Privacy dropdown (Full, Summary, Minimal) + "Join" button -> calls `joinFamily(code, userId, relationship, privacy)`

**State 2 — Has family**:
- `<FamilyDashboard />` component
- Fetch family data from `getFamily(profile.family_id)` on mount

---

### pages/Settings.jsx

**Layout** (card sections, `space-y-6`):

1. **Server Configuration**: Card with IP input + Port input — for mobile app connectivity

2. **Medical Contacts**: Card with doctor name, email, phone inputs + emergency contact name, phone — "Save" button calls `updateProfile`

3. **Spotify Integration**: Card with "Connect Spotify" button (opens OAuth flow) + status indicator

4. **Privacy Settings**: Card with family sharing level dropdown (Full, Summary, Minimal)

5. **Danger Zone**: Card with `border border-red-200` — "Delete My Data" button in `bg-red-500 hover:bg-red-600 text-white` with confirmation dialog before proceeding

---

## CRITICAL IMPLEMENTATION NOTES

1. **Every component must handle three states**: loading (show skeleton/spinner), empty (show helpful message), and error (show error with retry button). Do NOT leave any component that crashes on null data.

2. **All API calls must be wrapped in try/catch**. On error, call `showToast(error.message, 'error')` from the store.

3. **Responsive design**: Use Tailwind responsive prefixes. Grid columns: `grid-cols-1 md:grid-cols-2 lg:grid-cols-4`. Test that layouts don't break on narrow viewports.

4. **Icons**: Import individually from lucide-react, e.g., `import { Heart, Brain, Flame } from 'lucide-react'`. Common icons used:
   - Heart, Brain, Bone, Flame, Activity, Moon, Footprints, Wind
   - Upload, Camera, FileText, Droplets, Image, Smartphone
   - Trophy, Target, Star, Zap, CheckCircle, Circle
   - AlertTriangle, Bell, ChevronRight, ArrowUp, ArrowDown, X, Send
   - LayoutDashboard, Lightbulb, Sparkles, Search, Users, Settings as SettingsIcon
   - Timer, TrendingUp, Dumbbell, PersonStanding

5. **Recharts**: Always wrap charts in `<ResponsiveContainer width="100%" height={N}>`. Use `<LineChart>`, `<BarChart>` with `<Tooltip>`, `<Legend>`, `<CartesianGrid>`.

6. **Number formatting**: Use `toLocaleString()` for large numbers (steps: "8,234"), `.toFixed(1)` for decimals (bio age: "17.2"). All metric numbers use `font-mono font-medium tabular-nums`.

7. **Tailwind v4**: Uses CSS-first configuration via `@tailwindcss/vite` plugin. The `index.css` file uses `@import "tailwindcss";`. No `tailwind.config.js` needed unless custom theme extensions are required.

8. **Do NOT use placeholder/dummy data inline**. All data comes from API calls stored in Zustand. Components should gracefully handle when data is null/undefined/loading.

9. **SSE streaming in ChatInterface**: The `streamChat` function returns text chunks via the `onText` callback. Accumulate these into the current assistant message to create a typewriter/streaming effect. Each chunk should be appended to the existing text.

10. **Sidebar active state**: Use react-router-dom's `NavLink` component with its `className` function that receives `{ isActive }` to conditionally apply `bg-slate-800 text-white` for the active route.

11. **Toast component**: Already rendered in App.jsx. Components use `useStore().showToast(message, type)` to trigger notifications. Types: 'success' (emerald), 'error' (red), 'warning' (amber), 'info' (blue).

12. **All files must be complete and production-ready**. No TODO comments, no placeholder implementations, no "implement this later" stubs. Every file must contain full working code.
