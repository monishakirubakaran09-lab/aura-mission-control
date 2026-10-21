# 🚀  Aura Mission Control — Autonomous Mission Commander

**When Earth can't respond, our AI Mission Commander helps the spacecraft decide what to do next.**

Mission Control is an AI-powered, multi-agent spacecraft simulation designed to demonstrate autonomous decision-making during deep-space missions. When communication with Earth is delayed or unavailable, multiple specialized AI agents collaborate to analyze spacecraft conditions, evaluate mission priorities, and recommend safe actions.

Instead of relying on a single AI model, Mission Control uses specialized agents coordinated by a central Mission Commander to respond to unexpected events and dynamically re-plan mission operations.

> **Note:** This is a simulation and decision-support prototype, not software designed to control a real spacecraft.

## 🌌 The Problem

Deep-space missions face challenges that require rapid decision-making:

- Communication delays or temporary loss of contact with Earth.
- Limited resources, including battery power and fuel.
- Unexpected navigation uncertainties.
- Conflicting scientific objectives and spacecraft safety requirements.

Waiting for instructions from Earth may not always be practical. Spacecraft need systems that can evaluate available information and identify appropriate responses within predefined mission constraints.

## 💡 Our Solution

Mission Control simulates an autonomous spacecraft supported by multiple AI agents, each responsible for a specific mission domain.

The agents analyze spacecraft telemetry, propose actions, evaluate trade-offs, and collaborate through a central Mission Commander.

The system generates an updated mission plan based on current conditions, mission objectives, available resources, and safety constraints.

## 🤖 Multi-Agent Architecture

### 1. 🧭 Navigation Agent
- Monitors simulated navigation and trajectory conditions.
- Evaluates navigation uncertainty.
- Recommends appropriate trajectory adjustments.

### 2. 🔋 Resource Agent
- Monitors battery, fuel, and resource availability.
- Estimates the impact of proposed actions on resource levels.
- Recommends power-saving measures and resource allocation.

### 3. 🔬 Science Agent
- Tracks scientific objectives and their priorities.
- Evaluates experiments based on mission value.
- Recommends which objectives should continue, pause, or be deferred.

### 4. 🛡️ Safety Agent
- Evaluates proposed actions against predefined mission constraints.
- Identifies unsafe or conflicting recommendations.
- Rejects or flags actions that violate the simulation's safety rules.

### 5. 🧠 Mission Commander
- Coordinates the specialized agents.
- Evaluates conflicting recommendations.
- Selects a mission plan that respects safety constraints and resource limits.
- Explains the reasoning behind its decision.
- Produces an updated plan for the simulated spacecraft.

## ⚙️ How It Works

```text
Simulated Spacecraft Telemetry
              |
              v
      Anomaly Detection
              |
              v
  +-----------+-----------+
  |           |           |
  v           v           v
Navigation  Resource    Science
  Agent      Agent       Agent
  |           |           |
  +-----------+-----------+
              |
              v
       Safety Agent
              |
              v
      Mission Commander
              |
              v
     Updated Mission Plan
              |
              v
      Mission Control UI
```

The architecture is a proposed design; the final implementation may adjust the order of agent
