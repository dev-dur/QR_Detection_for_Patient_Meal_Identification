# QR_Detection_for_Patient_Meal_Identification
A lightweight app that scans a QR code to identify a patient and instantly retrieve their meal assignment from a local database. Built for offline-first use in hospitals and care facilities.

✨ What it does
- Uses the device camera to scan QR codes (web or desktop).
- Looks up patient by number (e.g., 123) in a local DB.
- Displays name, health problem, and meal identity (e.g., abc) with clear visual status.
- Logs scans for audit and nutrition tracking.

🔐 Safety & privacy
- No cloud—all data is local (txt file).
- Access is limited to the local machine/network.
- Optionally add a passcode screen for staff devices.

✅ Acceptance criteria
 - Scans a QR and resolves patient record offline.
 - Shows name, health problem, meal identity clearly.
 - Handles not found / invalid QR gracefully.
 - Works with camera on common desktop/mobile browsers.

🧭 Future enhancements
- Meal rules engine (e.g., auto-flag conflicts with health problem).
- Role-based access and PIN lock.
- Import/export CSV for patients.

Printable QR badges/cards.

PWA install + background sync.
