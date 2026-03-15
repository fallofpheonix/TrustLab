# Raw Proposal Data: ISSR (Task 3)

**Humanlike AI Systems and Trust Attribution**

**Description**
This project will build an open-source, modular experimentation engine for studying trust calibration in AI-assisted decision systems. The platform will allow researchers to systematically manipulate humanlike and authority-signaling interface cues (e.g., assistant name, tone, confidence framing) and log user behavior at high temporal resolution to measure reliance vs. override decisions.
The end product will be a reusable research infrastructure for human–AI trust, calibration, and adoption studies.

**Motivation**
As AI assistants increasingly adopt humanlike names, conversational tone, avatars, and confidence framing, users infer competence, agency, and intentionality from interface design alone. These inferences can lead to appropriate reliance, underuse, or overtrust. Most existing research relies heavily on self-report trust scales. This project focuses on behavioral trust metrics, grounded in observable decision behavior and structured logging.

**Scope of Work**
1) Experimental Web Application (React/Next.js): Participant ID, Randomized conditions, Logging backend.
2) Cue Manipulation System: Manipulate Agent naming (neutral vs humanlike), Tone (formal vs social), Confidence framing.
3) Behavioral Task Module: Recommendation Acceptance Task.
4) Instrumentation and Logging: Chronologically structured event schema (JSON/CSV).
5) Dataset Export + Analysis Notebook: Jupyter Notebook evaluating reliance rate, override rate, mean latency.

**Required Skills**
JavaScript, React/Next.js, Basic backend logging, JSON/CSV structuring, Experimental logic / A/B testing, Basic statistics.

**Screening Test (2-4 Hours)**
Build a minimal working prototype (web page with A/B conditions, one decision task, logging to JSON). Submit GitHub repo link, short README, sample output file.

**Mentors**
* Andrya Allen (University of Alabama)
* Dr. Xinyue Ye (University of Alabama)
* Dr. Kelsey Chappetta (University of Alabama)
* Dr. Andrea Underhill (University of Alabama)
