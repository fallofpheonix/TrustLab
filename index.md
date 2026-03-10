---
layout: default
title: HumanAI - Humanlike AI Systems and Trust Attribution
---

<link
  href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
  rel="stylesheet"
  integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH"
  crossorigin="anonymous"
>

<style>
  .hero {
    background: linear-gradient(135deg, #0b2545 0%, #134074 55%, #155e75 100%);
    color: #fff;
    border-radius: 1rem;
    padding: 2rem;
  }
  .section-card {
    border: 1px solid #e9ecef;
    border-radius: 0.75rem;
  }
  .pill {
    margin-right: 0.4rem;
    margin-bottom: 0.4rem;
  }
</style>

<div class="container py-4">
  <div class="hero mb-4">
    <h1 class="h3 mb-1">HumanAI</h1>
    <h2 class="h5 mb-1">Activities</h2>
    <h3 class="h4 mb-3">Humanlike AI Systems and Trust Attribution</h3>
    <span class="badge text-bg-light text-dark pill">Moderate</span>
    <span class="badge text-bg-info text-dark pill">Behavioral Trust Metrics</span>
    <span class="badge text-bg-warning text-dark pill">Screening Test (2-4 Hours)</span>
    <span class="badge text-bg-success pill">ISSR / Alabama</span>
  </div>

  <div class="row g-3 mb-4">
    <div class="col-12 col-lg-6">
      <div class="p-3 section-card h-100">
        <h2 class="h5">Description</h2>
        <p>
          This project will build an open-source, modular experimentation engine for studying trust calibration in AI-assisted decision systems. The platform will allow researchers to systematically manipulate humanlike and authority-signaling interface cues (e.g., assistant name, tone, confidence framing) and log user behavior at high temporal resolution to measure reliance vs. override decisions.
        </p>
        <p class="mb-0">
          The end product will be a reusable research infrastructure for human-AI trust, calibration, and adoption studies.
        </p>
      </div>
    </div>
    <div class="col-12 col-lg-6">
      <div class="p-3 section-card h-100">
        <h2 class="h5">Motivation</h2>
        <p>
          As AI assistants increasingly adopt humanlike names, conversational tone, avatars, and confidence framing, users infer competence, agency, and intentionality from interface design alone. These inferences can lead to appropriate reliance, underuse, or overtrust.
        </p>
        <p class="mb-0">
          Most existing research relies heavily on self-report trust scales. This project focuses on behavioral trust metrics, grounded in observable decision behavior and structured logging.
        </p>
      </div>
    </div>
  </div>

  <div class="accordion mb-4" id="projectAccordion">
    <div class="accordion-item">
      <h2 class="accordion-header">
        <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#goals" aria-expanded="true" aria-controls="goals">
          Project Goals
        </button>
      </h2>
      <div id="goals" class="accordion-collapse collapse show" data-bs-parent="#projectAccordion">
        <div class="accordion-body">
          <p>The contributor will build a modular web-based experimental environment that supports:</p>
          <ul class="mb-0">
            <li>Controlled manipulation of humanlike and authority-signaling cues</li>
            <li>One structured decision task that produces reliance vs. override outcomes</li>
            <li>Fine-grained behavioral instrumentation (decisions + latency + interaction sequence)</li>
            <li>Exportable, analysis-ready datasets (CSV + JSON)</li>
            <li>A reproducible analysis notebook (Python or R)</li>
            <li>Documentation and deployment instructions for reuse</li>
          </ul>
        </div>
      </div>
    </div>

    <div class="accordion-item">
      <h2 class="accordion-header">
        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#scope" aria-expanded="false" aria-controls="scope">
          Scope of Work
        </button>
      </h2>
      <div id="scope" class="accordion-collapse collapse" data-bs-parent="#projectAccordion">
        <div class="accordion-body">
          <h3 class="h6">1) Experimental Web Application</h3>
          <p>Build a lightweight experiment platform (React/Next.js or similar) including:</p>
          <ul>
            <li>Participant ID assignment</li>
            <li>Randomized condition assignment (A/B or multi-condition)</li>
            <li>Task presentation interface</li>
            <li>Logging backend</li>
            <li>Dataset export functionality</li>
          </ul>
          <p>Architecture must support modular cue manipulation.</p>

          <h3 class="h6">2. Cue Manipulation System</h3>
          <p>Implement a condition management framework enabling systematic manipulation of at least 3 cue dimensions, such as:</p>
          <ul>
            <li>Agent naming (neutral label vs. humanlike name)</li>
            <li>Tone (formal/technical vs. conversational/social)</li>
            <li>Confidence framing (calibrated probability vs. overstated certainty)</li>
          </ul>
          <p>The system should be extensible so additional cues (e.g., visual identity, role assignment source) can be added later.</p>

          <h3 class="h6">3. Behavioral Task Module</h3>
          <p>Implement one structured decision task that generates clear behavioral trust outcomes: Recommendation Acceptance Task</p>
          <ul>
            <li>AI provides a recommendation</li>
            <li>Participant chooses to accept or override</li>
            <li>Optional participant confidence rating</li>
          </ul>
          <p>AI accuracy should be experimentally controlled (e.g., fixed accuracy rate) to evaluate trust calibration.</p>

          <h3 class="h6">4. Instrumentation and Logging</h3>
          <p>Design and implement a clean event schema capturing:</p>
          <ul>
            <li><code>participant_id</code></li>
            <li><code>condition</code></li>
            <li><code>decision</code></li>
            <li><code>timestamp</code></li>
            <li><code>latency_ms</code></li>
            <li>optional trust scale responses</li>
          </ul>
          <p>Requirements:</p>
          <ul>
            <li>Chronologically structured logging</li>
            <li>Exportable JSON and CSV formats</li>
            <li>Clear schema documentation</li>
          </ul>

          <h3 class="h6">5. Dataset Export + Analysis Notebook</h3>
          <p>Deliver:</p>
          <ul class="mb-0">
            <li>Clean CSV + JSON exports</li>
            <li>A basic analysis notebook (Python or R) demonstrating:</li>
            <li>reliance rate by condition</li>
            <li>override rate by condition</li>
            <li>mean response latency</li>
            <li>optional trust scale vs. behavior comparison</li>
          </ul>
        </div>
      </div>
    </div>

    <div class="accordion-item">
      <h2 class="accordion-header">
        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#deliverables" aria-expanded="false" aria-controls="deliverables">
          Deliverables and Stretch Goals
        </button>
      </h2>
      <div id="deliverables" class="accordion-collapse collapse" data-bs-parent="#projectAccordion">
        <div class="accordion-body">
          <h3 class="h6">Deliverables</h3>
          <p>By the end of the project, the contributor will provide:</p>
          <ul>
            <li>Functional experimental prototype (local or deployed)</li>
            <li>Condition assignment + cue manipulation module</li>
            <li>Behavioral logging backend</li>
            <li>Structured event schema documentation</li>
            <li>Sample dataset</li>
            <li>Analysis notebook</li>
            <li>"How to Run" documentation</li>
            <li>All code in a public GitHub repository</li>
          </ul>

          <h3 class="h6">Stretch Goals (If Time Allows)</h3>
          <ul class="mb-0">
            <li>Add additional cue dimensions (visual identity, role assignment source)</li>
            <li>Add a second task type (e.g., product choice / willingness-to-pay)</li>
            <li>Add optional post-task trust ratings and richer interaction logging</li>
          </ul>
        </div>
      </div>
    </div>

    <div class="accordion-item">
      <h2 class="accordion-header">
        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#screening" aria-expanded="false" aria-controls="screening">
          Screening Test and Submission
        </button>
      </h2>
      <div id="screening" class="accordion-collapse collapse" data-bs-parent="#projectAccordion">
        <div class="accordion-body">
          <h3 class="h6">Screening Test (2-4 Hours)</h3>
          <p>Applicants must build a minimal working prototype.</p>
          <p>Requirements:</p>
          <ul>
            <li>A simple web page with two conditions (A/B) differing in one cue (e.g., name + tone)</li>
            <li>One decision task: Accept/reject AI recommendation OR choose between two products</li>
            <li>Logging to JSON or CSV including: <code>participant_id</code>, <code>condition</code>, <code>decision</code>, <code>timestamp</code>, <code>latency_ms</code></li>
          </ul>

          <h3 class="h6">Submission</h3>
          <ul>
            <li>A current CV or resume</li>
            <li>Test results</li>
            <li>GitHub repo link</li>
            <li>Short README explaining: condition logic, logging implementation, how to run locally, sample output file</li>
          </ul>
        </div>
      </div>
    </div>
  </div>

  <div class="row g-3 mb-4">
    <div class="col-12 col-lg-6">
      <div class="p-3 section-card h-100">
        <h2 class="h5">Required Skills</h2>
        <ul class="mb-0">
          <li>JavaScript</li>
          <li>React / Next.js (or similar framework)</li>
          <li>Basic backend logging (API endpoints, file output, or lightweight DB)</li>
          <li>JSON/CSV structuring</li>
          <li>Experimental logic / A/B testing fundamentals</li>
          <li>Basic statistical literacy</li>
        </ul>
      </div>
    </div>
    <div class="col-12 col-lg-6">
      <div class="p-3 section-card h-100">
        <h2 class="h5">Project difficulty level</h2>
        <p class="mb-0">Moderate. This project requires integration of frontend development, experimental condition logic, and structured behavioral logging.</p>
      </div>
    </div>
  </div>

  <div class="row g-3 mb-4">
    <div class="col-12 col-lg-6">
      <div class="p-3 section-card h-100">
        <h2 class="h5">Mentorship Expectations</h2>
        <p>Contributors will be expected to:</p>
        <ul class="mb-0">
          <li>Participate in weekly mentor check-ins</li>
          <li>Submit incremental pull requests</li>
          <li>Document design decisions</li>
          <li>Maintain reproducible workflows</li>
        </ul>
      </div>
    </div>
    <div class="col-12 col-lg-6">
      <div class="p-3 section-card h-100">
        <h2 class="h5">Broader Impact</h2>
        <p>This project supports responsible AI by:</p>
        <ul class="mb-0">
          <li>Distinguishing perceived capability from actual capability</li>
          <li>Measuring when humanlike cues alter trust calibration</li>
          <li>Enabling evidence-based interface design for AI-assisted decision systems</li>
        </ul>
      </div>
    </div>
  </div>

  <div class="p-3 section-card">
    <h2 class="h5">Mentors</h2>
    <ul>
      <li>Andrya Allen (University of Alabama)</li>
      <li>Dr. Xinyue Ye (University of Alabama)</li>
      <li>Dr. Kelsey Chappetta (University of Alabama)</li>
      <li>Dr. Andrea Underhill (University of Alabama)</li>
    </ul>
    <p class="mb-1"><strong>Please DO NOT contact mentors directly by email.</strong></p>
    <p class="mb-1">Instead, please email <a href="mailto:human-ai@cern.ch">human-ai@cern.ch</a> with Project Title and include your CV and test results. The mentors will then get in touch with you.</p>
    <p class="mb-1"><strong>Corresponding Project:</strong> ISSR</p>
    <p class="mb-0"><strong>Participating Organizations:</strong> Alabama</p>
  </div>
</div>

<script
  src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
  integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz"
  crossorigin="anonymous"
></script>
