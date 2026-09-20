import { useEffect, useState } from "react";
import "./App.css";

export default function App() {
  const API = "http://127.0.0.1:8000";

  const [mission, setMission] = useState(null);
  const [decision, setDecision] = useState(null);
  const [timeline, setTimeline] = useState([]);

  const load = async () => {
    const state = await fetch(`${API}/mission/state`).then(r => r.json());
    const ai = await fetch(`${API}/mission/decide`, {
      method: "POST",
    }).then(r => r.json());
    const log = await fetch(`${API}/mission/log`).then(r => r.json());

    setMission(state);
    setDecision(ai);
    setTimeline(log.timeline);
  };

  useEffect(() => {
    load();
    const i = setInterval(load, 3000);
    return () => clearInterval(i);
  }, []);

  if (!mission) return <div className="loading">Launching Aura...</div>;

  return (
    <div className="app">

      <div className="grid-lines"></div>

      <nav className="navbar">

        <div className="logo">
          <div className="planet-icon"></div>
          <span>AURA</span>
        </div>

        <div className="nav-links">
          <span>Overview</span>
          <span>Telemetry</span>
          <span>Recovery</span>
          <span>Timeline</span>
        </div>

        <button className="live-btn">
          ● Mission Live
        </button>

      </nav>

      <section className="hero">

        <div className="hero-left">

          <p className="eyebrow">
            NEXT GENERATION SPACE OPERATIONS
          </p>

          <h1>
            AURA
            <br />
            MISSION CONTROL
          </h1>

          <p className="subtitle">
            Intelligent spacecraft monitoring with live telemetry,
            automated recovery actions and real-time mission insights.
          </p>

          <div className="hero-buttons">

            <button className="launch-btn">
              🚀 Launch Dashboard
            </button>

            <div className="mission-chip">
              <div className="mars"></div>

              <div>
                <small>Mission</small>
                <strong>Mars Soil Analysis</strong>
              </div>
            </div>

          </div>

        </div>

        <div className="hero-right">

          <div className="orbit o1"></div>
          <div className="orbit o2"></div>
          <div className="orbit o3"></div>

          <div className="astronaut"></div>

          <div className="planet-glow"></div>

        </div>

      </section>

      <section className="cards">

        <div className="card blue">

          <div className="icon">🔋</div>

          <div>
            <p>Battery</p>
            <h2>{mission.battery}%</h2>
          </div>

          <div className="progress">
            <span style={{ width: `${mission.battery}%` }}></span>
          </div>

        </div>

        <div className="card pink">

          <div className="icon">⛽</div>

          <div>
            <p>Fuel</p>
            <h2>{mission.fuel}%</h2>
          </div>

          <div className="progress">
            <span style={{ width: `${mission.fuel}%` }}></span>
          </div>

        </div>

        <div className="card green">

          <div className="icon">📡</div>

          <div>
            <p>Communication</p>
            <h2>{mission.communication ? "ONLINE" : "OFFLINE"}</h2>
          </div>

        </div>

        <div className="card orange">

          <div className="icon">🧭</div>

          <div>
            <p>Navigation</p>
            <h2>{mission.navigation_uncertainty}</h2>
            <small>Uncertainty (m)</small>
          </div>

        </div>

      </section>

      <section className="bottom">

        <div className="panel">

          <h3>⚡ Recovery Actions</h3>

          {mission.actions.length === 0 ? (
            <>
              <div className="action">Adjusting orbit parameters</div>
              <div className="action">Running diagnostics</div>
              <div className="action">Monitoring systems</div>
            </>
          ) : (
            mission.actions.map((a, i) => (
              <div key={i} className="action">{a}</div>
            ))
          )}

        </div>

        <div className="panel">

          <h3>🧠 AI Decision Engine</h3>

          <div className="decision">
            <strong>{decision.decision}</strong>
            <p>Priority Level: {decision.priority}</p>
          </div>

          {decision.reasoning.map((r, i) => (
            <div key={i} className="reason">{r}</div>
          ))}

        </div>

        <div className="panel">

          <h3>🕒 Mission Timeline</h3>

          {timeline.length === 0 ? (
            <>
              <div className="timeline-item">Mission initialized</div>
              <div className="timeline-item">Awaiting events</div>
            </>
          ) : (
            timeline.map((e, i) => (
              <div key={i} className="timeline-item">{e}</div>
            ))
          )}

        </div>

      </section>

    </div>
  );
}