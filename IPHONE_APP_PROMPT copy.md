# Build a Minimal iPhone HealthKit Export App

## What This App Does
A simple iOS app that reads health data from Apple HealthKit and sends it as encrypted JSON to a backend server over the local network. This is for a hackathon demo — it runs on the developer's own iPhone via Xcode, no App Store submission.

## Requirements

### 1. HealthKit Data to Read
Request authorization and query the following HealthKit data types:

**Quantity Types (latest value or today's aggregate):**
- Resting Heart Rate (HKQuantityTypeIdentifier.restingHeartRate) — latest
- Heart Rate Variability SDNN (HKQuantityTypeIdentifier.heartRateVariabilitySDNN) — latest
- Step Count (HKQuantityTypeIdentifier.stepCount) — today's total + 7-day daily average
- Active Energy Burned (HKQuantityTypeIdentifier.activeEnergyBurned) — today's total
- Apple Exercise Time (HKQuantityTypeIdentifier.appleExerciseTime) — today's total in minutes
- VO2 Max (HKQuantityTypeIdentifier.vo2Max) — latest
- Respiratory Rate (HKQuantityTypeIdentifier.respiratoryRate) — latest
- Walking Asymmetry Percentage (HKQuantityTypeIdentifier.walkingAsymmetryPercentage) — latest
- Flights Climbed (HKQuantityTypeIdentifier.flightsClimbed) — today's total
- Body Mass (HKQuantityTypeIdentifier.bodyMass) — latest
- Height (HKQuantityTypeIdentifier.height) — latest
- Blood Pressure Systolic + Diastolic — latest (if available)

**Category Types:**
- Sleep Analysis (HKCategoryTypeIdentifier.sleepAnalysis) — last night's total sleep duration, and if available break down into: asleep core, asleep deep, asleep REM, awake

**Workout Type:**
- HKWorkoutType — last 7 days of workouts (type, duration, calories)

### 2. UI (Keep it dead simple)
- **Screen 1: Server Configuration**
  - Text field for server IP address (default: "192.168.x.x")
  - Text field for server port (default: "8000")
  - Text field for user name/ID (e.g., "zahoor") — this identifies whose data this is
  - A "Save" button

- **Screen 2: Main Screen**
  - Large "Sync Now" button
  - Status label showing: "Ready" / "Syncing..." / "Success ✓" / "Error: ..."
  - Last sync timestamp
  - A scrollable list showing all fetched values (for debugging/demo)
  - Small "Auto-sync" toggle (when ON, sync every 30 minutes using BackgroundTasks)

- **Screen 3: Permissions**
  - On first launch, request HealthKit permissions for all types above
  - Show a clear message: "This app reads your health data to send to your personal health dashboard"

### 3. Data Format — JSON Payload
Send this exact JSON structure to the backend:

```json
{
  "user_id": "zahoor",
  "timestamp": "2026-03-28T10:30:00+05:30",
  "device": "iPhone 15 Pro",
  "data": {
    "resting_hr_bpm": 68,
    "hrv_sdnn_ms": 45.2,
    "steps_today": 8234,
    "steps_avg_7d": 7500,
    "active_energy_kcal": 420.5,
    "exercise_minutes_today": 35,
    "vo2max_ml_kg_min": 42.5,
    "respiratory_rate_bpm": 15.2,
    "walking_asymmetry_pct": 3.2,
    "flights_climbed_today": 4,
    "body_mass_kg": 66.9,
    "height_cm": 178.0,
    "blood_pressure_systolic": null,
    "blood_pressure_diastolic": null,
    "sleep_last_night": {
      "total_hours": 7.2,
      "deep_pct": 18,
      "rem_pct": 22,
      "core_pct": 48,
      "awake_pct": 12
    },
    "workouts_7d": [
      {
        "type": "running",
        "duration_min": 30,
        "calories": 280,
        "date": "2026-03-27"
      }
    ]
  }
}
```

Use `null` for any value that is not available (user didn't grant permission or no data exists).

### 4. Network Communication
- Send via HTTP POST to `http://{server_ip}:{port}/api/healthkit`
- Content-Type: application/json
- **Encryption**: Since this is local network (hackathon demo), use HTTPS if possible but HTTP is acceptable. However, the JSON payload body should be encrypted:
  - Use AES-256-GCM encryption on the JSON body before sending
  - Use a pre-shared key (hardcoded for hackathon, stored in both app and backend)
  - Send the encrypted payload as base64 in a wrapper:
    ```json
    {
      "encrypted": true,
      "iv": "<base64 IV>",
      "data": "<base64 encrypted JSON>",
      "tag": "<base64 auth tag>"
    }
    ```
  - Pre-shared key: `"healthhack2026secretkey1234567890"` (32 bytes for AES-256)
  - This way even on HTTP, the actual health data is encrypted in transit

### 5. Security & Privacy
- All data processing happens in-memory, no local database or file storage on iPhone
- Clear the fetched data from memory after successful sync
- HealthKit usage description in Info.plist:
  - NSHealthShareUsageDescription: "This app reads your health data to provide personalized health insights on your dashboard."
- No third-party analytics or tracking SDKs
- No data sent anywhere except the configured server IP

### 6. Xcode Project Setup
- Target: iOS 17.0+
- Swift 5.9+
- SwiftUI for the UI
- No external dependencies (use only Apple frameworks: HealthKit, CryptoKit, Foundation)
- Enable HealthKit capability in Signing & Capabilities
- Enable Background Modes → Background fetch (for auto-sync)

### 7. Error Handling
- If HealthKit permission denied for a specific type → set that field to null, don't crash
- If server is unreachable → show "Error: Cannot reach server at {ip}:{port}" and retry option
- If partial data (some types available, others not) → send whatever is available
- Network timeout: 10 seconds

### 8. File Structure
```
HealthExporter/
├── HealthExporterApp.swift      # App entry point
├── ContentView.swift            # Main screen with Sync button
├── SettingsView.swift           # Server IP/port configuration
├── HealthKitManager.swift       # All HealthKit queries
├── NetworkManager.swift         # HTTP POST + AES encryption
├── Models.swift                 # HealthData struct, JSON encoding
└── Info.plist                   # HealthKit usage descriptions
```

### 9. Key Implementation Notes
- Use `HKStatisticsQuery` for aggregate values (steps, calories, exercise time, flights)
- Use `HKSampleQuery` with `sortDescriptors: [NSSortDescriptor(key: HKSampleSortIdentifierStartDate, ascending: false)]` and `limit: 1` for latest values (heart rate, HRV, VO2max, etc.)
- For sleep: query `HKCategoryTypeIdentifier.sleepAnalysis` for yesterday 8 PM to today 12 PM, filter by `HKCategoryValueSleepAnalysis` cases
- For 7-day step average: use `HKStatisticsCollectionQuery` with daily interval for last 7 days, then compute mean
- Use `CryptoKit` for AES-GCM encryption (import CryptoKit, SymmetricKey, AES.GCM)
- The pre-shared key should be: `SymmetricKey(data: "healthhack2026secretkey1234567890".data(using: .utf8)!)`
