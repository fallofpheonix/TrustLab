# Architecture & Roadmap Plan: ISSR (Task 3 - Humanlike AI Systems)

## 1. Roadmap
- **Phase 1: React Component Prototyping**
  - Scaffold the frontend framework (Next.js recommended).
  - Build discrete, reusable UI components for the "Recommendation Acceptance Task".
- **Phase 2: State Tracking & Context Management**
  - Implement a global context (Redux or Context API) to manage `participant_id`, start/end timestamps, and active A/B conditions seamlessly across views without prop-drilling.
- **Phase 3: Backend Logging API**
  - Build a lightweight Node/Express (or Next.js API Routes) backend that accepts POST requests from frontend interaction events and serializes them cleanly to NDJSON or CSV.
- **Phase 4: Analytics Pipeline**
  - Write a Python (Pandas/Seaborn) or R notebook that ingests the JSON/CSV output and plots behavioral reliance versus latency grouped by manipulated cues.

## 2. Architecture Plan
- **Presentation Layer**: Next.js single-page application handling routing and dynamic conditional rendering based on assigned `conditionID` logic.
- **Data Collection Layer**: A custom Javascript instrumentation hook (e.g., `useTelemetry`) that measures precise `latency_ms` between the time a recommendation renders and the time an `onClick` event is fired.
- **Persistence Layer**: Abstracted file-system logger handling concurrent writes to local CSV/JSON files, capable of being easily swapped out for PostgreSQL if scaled in the future.

## 3. Changes Needed
- The project is greenfield (new build). Architecture must strictly isolate the experimental cue variables (Name, Tone) into configurable JSON files so non-technical researchers can design new experiments without modifying the React source code.

## 4. Current Problems
- Measuring trust is inherently difficult; self-reporting is flawed. The new platform *must* guarantee millisecond-accurate timestamping to validate hesitated interactions.

## 5. Problems It Can Cause
- **Drift & Latency Errors**: Browser-based millisecond timing relies on standard Javascript engine ticks, which can be throttled by the OS or background tabs, skewing the `latency_ms` metric artificially.

## 6. Future Work
- Integration of webcam-based eye-tracking (via WebGazer.js) to correlate visual attention dwell time on the AI UI cues with final reliance decisions.
