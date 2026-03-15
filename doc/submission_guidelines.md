# Submission Guidelines & Constraints: ISSR (Task 3 - Humanlike AI Systems)

## What to Build (Deliverables)
1. **Experimental Web Application**: A lightweight frontend (React/Next.js) supporting participant ID assignment, randomized condition assignment, and task presentation.
2. **Cue Manipulation System**: A framework to systematically manipulate at least 3 cue dimensions (Name, Tone, Confidence framing).
3. **Behavioral Task Module**: Implement a "Recommendation Acceptance Task" where an AI provides a suggestion and the participant chooses to accept or override.
4. **Instrumentation/Logging**: A clean event schema capturing ID, condition, decision, timestamp, and latency_ms. Exportable to JSON/CSV.
5. **Analysis Notebook**: A Python or R notebook demonstrating reliance rates, override rates, and mean response latency from the collected JSON data.

## Screening Task (Required for Application)
Applicants must build a minimal working prototype (2-4 hours).
**Requirements**:
- A simple web page with A/B conditions differing in one cue (e.g., name + tone).
- One decision task (Accept/Reject AI recommendation).
- Logging to JSON/CSV including participant_id, condition, decision, timestamp, latency_ms.

## What to Submit to Mentor
Applicants should submit the following to **human-ai@cern.ch** with **"Project Title"** in the subject line:
- A current CV or resume.
- GitHub repo link to the screening task.
- A short README explaining condition logic, logging implementation, and how to run locally.
- Sample JSON/CSV output file from the screening task.
- **Do NOT contact mentors directly.**

## Constraints
- **Required Stack**: JavaScript, React/Next.js (or similar frontend framework), basic backend logging, Python/R (for analysis).
- **Difficulty**: Moderate (175 hours). Requires integration of frontend development, experimental conditional logic, and behavioral logging.
