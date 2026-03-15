# Constraints and Restrictions: ISSR - task3

## Technical Constraints

### Required Stack

The screening task assumes:

```
JavaScript or TypeScript
React or Next.js
basic backend logging
JSON or CSV export
Python or R for analysis
```

### Measurement Constraints

The core behavioral fields must be captured per trial:

```
participant_id
condition
decision
timestamp
latency_ms
```

### Experiment Design Constraints

The prototype must manipulate at least one cue dimension during screening and support at least three during full project development:

```
name
tone
confidence framing
```

### Reliability Constraints

Latency must be measured from recommendation render to user action.
The system must tolerate duplicate refreshes, incomplete sessions, and local file-write failures without corrupting prior logs.

### Scope Constraints

The screening deliverable is intentionally small:

```
single decision task
local run only
simple output files
```

No production deployment, authentication, or database integration is required for the first milestone.
