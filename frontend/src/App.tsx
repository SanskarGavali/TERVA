
import { useState } from "react";

type Page =
  | "Overview"
  | "Evidence Explorer"
  | "AI Assistant"
  | "Web Security"
  | "Network Security"
  | "Reverse Engineering"
  | "Malware Analysis"
  | "Activity & Audit"
  | "Settings";

const navigation: { name: Page; icon: string; section: string }[] = [
  { name: "Overview", icon: "◫", section: "WORKSPACE" },
  { name: "Evidence Explorer", icon: "◈", section: "WORKSPACE" },
  { name: "AI Assistant", icon: "✧", section: "INTELLIGENCE" },
  { name: "Web Security", icon: "⌘", section: "SECURITY TOOLS" },
  { name: "Network Security", icon: "⌁", section: "SECURITY TOOLS" },
  { name: "Reverse Engineering", icon: "⌬", section: "SECURITY TOOLS" },
  { name: "Malware Analysis", icon: "⬡", section: "SECURITY TOOLS" },
  { name: "Activity & Audit", icon: "≡", section: "SYSTEM" },
  { name: "Settings", icon: "⚙", section: "SYSTEM" },
];

const evidence = [
  {
    id: "TERVA-EVD-001",
    title: "HTTP Security Header Review",
    asset: "demo.example.local",
    source: "Manual review",
    status: "UNVERIFIED",
  },
  {
    id: "TERVA-EVD-002",
    title: "TLS Configuration Observation",
    asset: "demo.example.local",
    source: "Configuration review",
    status: "UNVERIFIED",
  },
  {
    id: "TERVA-EVD-003",
    title: "Access Control Observation",
    asset: "Internal demo application",
    source: "Manual review",
    status: "UNVERIFIED",
  },
];

const moduleInfo: Record<string, string> = {
  "Web Security":
    "Review web application security observations and evidence.",
  "Network Security":
    "Organise authorised network assessment workflows.",
  "Reverse Engineering":
    "Inspect binaries and document static analysis findings.",
  "Malware Analysis":
    "Review suspicious files through safe static analysis workflows.",
};

function App() {
  const [activePage, setActivePage] = useState<Page>("Overview");
  const [darkMode, setDarkMode] = useState(false);
  const [search, setSearch] = useState("");

  const sections = [...new Set(navigation.map((item) => item.section))];

  const filteredEvidence = evidence.filter((item) =>
    `${item.id} ${item.title} ${item.asset} ${item.source}`
      .toLowerCase()
      .includes(search.toLowerCase())
  );

  function renderOverview() {
    return (
      <>
        <div className="welcome-row">
          <div>
            <div className="eyebrow">
              SECURITY INTELLIGENCE WORKSPACE
            </div>
            <h1>Good morning, Operator.</h1>
            <p className="page-subtitle">
              Your security intelligence workspace is ready.
            </p>
          </div>
          <div className="date-chip">
            ◷ &nbsp; LOCAL WORKSPACE
          </div>
        </div>

        <div className="notice">
          <span className="notice-icon">ⓘ</span>
          <div>
            <strong>Demonstration environment</strong>
            <p>
              Dashboard metrics and evidence below are sample data.
              No live security scans or target assessments are
              currently running.
            </p>
          </div>
        </div>

        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-top">
              <span>Evidence Records</span>
              <span className="stat-icon purple">◈</span>
            </div>
            <div className="stat-number">03</div>
            <div className="stat-note">
              Sample records in this interface
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-top">
              <span>Verified Findings</span>
              <span className="stat-icon green">✓</span>
            </div>
            <div className="stat-number">00</div>
            <div className="stat-note">
              No findings verified yet
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-top">
              <span>Active Engagements</span>
              <span className="stat-icon blue">⌁</span>
            </div>
            <div className="stat-number">00</div>
            <div className="stat-note">
              No active engagements
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-top">
              <span>Security Modules</span>
              <span className="stat-icon orange">⬡</span>
            </div>
            <div className="stat-number">04</div>
            <div className="stat-note">
              Interface modules available
            </div>
          </div>
        </div>

        <div className="content-grid">
          <section className="panel evidence-panel">
            <div className="panel-heading">
              <div>
                <h2>Recent Evidence</h2>
                <p>
                  Latest evidence records in your workspace
                </p>
              </div>

              <button
                className="text-button"
                onClick={() =>
                  setActivePage("Evidence Explorer")
                }
              >
                View all →
              </button>
            </div>

            {evidence.map((item) => (
              <div className="evidence-row" key={item.id}>
                <div className="record-icon">◈</div>

                <div className="record-info">
                  <strong>{item.title}</strong>
                  <span>
                    {item.id} · {item.asset}
                  </span>
                </div>

                <span className="status status-pending">
                  {item.status}
                </span>
              </div>
            ))}
          </section>

          <section className="panel system-panel">
            <div className="panel-heading">
              <div>
                <h2>System Overview</h2>
                <p>Current application state</p>
              </div>
              <span className="online-dot" />
            </div>

            <div className="system-item">
              <span>Frontend interface</span>
              <strong className="healthy">Available</strong>
            </div>

            <div className="system-item">
              <span>Backend API</span>
              <strong className="muted">Not connected</strong>
            </div>

            <div className="system-item">
              <span>AI provider</span>
              <strong className="muted">Not configured</strong>
            </div>

            <div className="system-item">
              <span>Security engine</span>
              <strong className="muted">Not implemented</strong>
            </div>
          </section>
        </div>

        <section className="panel modules-panel">
          <div className="panel-heading">
            <div>
              <h2>Security Workbench</h2>
              <p>
                Choose a module to explore its workspace
              </p>
            </div>
          </div>

          <div className="module-grid">
            {[
              [
                "Web Security",
                "⌘",
                "Application security workspace",
              ],
              [
                "Network Security",
                "⌁",
                "Network assessment workspace",
              ],
              [
                "Reverse Engineering",
                "⌬",
                "Binary inspection workspace",
              ],
              [
                "Malware Analysis",
                "⬡",
                "Static analysis workspace",
              ],
            ].map(([name, icon, description]) => (
              <button
                className="module-card"
                key={name}
                onClick={() => setActivePage(name as Page)}
              >
                <span className="module-icon">{icon}</span>
                <strong>{name}</strong>
                <span>{description}</span>
                <span className="module-arrow">
                  Explore →
                </span>
              </button>
            ))}
          </div>
        </section>
      </>
    );
  }

  function renderEvidence() {
    return (
      <>
        <div className="page-heading">
          <div>
            <div className="eyebrow">
              EVIDENCE MANAGEMENT
            </div>
            <h1>Evidence Explorer</h1>
            <p className="page-subtitle">
              Review and organise collected security evidence.
            </p>
          </div>

          <span className="status status-pending">
            SAMPLE DATA
          </span>
        </div>

        <section className="panel">
          <div className="search-row">
            <input
              className="search-input"
              placeholder="Search evidence by ID, title or asset..."
              value={search}
              onChange={(event) =>
                setSearch(event.target.value)
              }
            />

            <span className="result-count">
              {filteredEvidence.length} records
            </span>
          </div>

          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>Evidence ID</th>
                  <th>Title</th>
                  <th>Asset</th>
                  <th>Source</th>
                  <th>Status</th>
                </tr>
              </thead>

              <tbody>
                {filteredEvidence.map((item) => (
                  <tr key={item.id}>
                    <td className="table-id">{item.id}</td>
                    <td>{item.title}</td>
                    <td>{item.asset}</td>
                    <td>{item.source}</td>
                    <td>
                      <span className="status status-pending">
                        {item.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

            {filteredEvidence.length === 0 && (
              <div className="empty-state">
                No matching evidence records.
              </div>
            )}
          </div>
        </section>
      </>
    );
  }

  function renderAssistant() {
    return (
      <>
        <div className="page-heading">
          <div>
            <div className="eyebrow">
              INTELLIGENCE LAYER
            </div>
            <h1>AI Assistant</h1>
            <p className="page-subtitle">
              A future interface for evidence-based security reasoning.
            </p>
          </div>

          <span className="status status-pending">
            NOT CONNECTED
          </span>
        </div>

        <section className="assistant-panel">
          <div className="assistant-symbol">✧</div>

          <h2>TERVA Intelligence</h2>

          <p>
            The AI reasoning layer is not connected yet.
            This interface is currently a frontend prototype.
          </p>

          <div className="assistant-message">
            <strong>Design principle</strong>
            <p>
              AI can help analyse evidence and explain risks.
              It cannot grant permissions, expand authorised
              scope or override the permission controller.
            </p>
          </div>

          <div className="assistant-input-row">
            <input
              placeholder="AI chat will be enabled after backend integration..."
              disabled
            />
            <button
              className="primary-button"
              type="button"
              disabled
            >
              Send ↗
            </button>
          </div>
        </section>
      </>
    );
  }

  function renderSecurityModule() {
    return (
      <>
        <div className="page-heading">
          <div>
            <div className="eyebrow">
              SECURITY WORKBENCH
            </div>
            <h1>{activePage}</h1>
            <p className="page-subtitle">
              {moduleInfo[activePage]}
            </p>
          </div>

          <span className="status status-pending">
            NOT IMPLEMENTED
          </span>
        </div>

        <section className="panel module-detail">
          <div className="large-module-icon">⬡</div>

          <h2>{activePage} Workspace</h2>

          <p>
            This module's interface is reserved for future
            implementation. No targets are being scanned and
            no security operations are currently executed.
          </p>

          <div className="module-checklist">
            <div>○ Authorised scope management</div>
            <div>○ Permission-controlled execution</div>
            <div>○ Evidence collection and provenance</div>
            <div>○ Independent verification</div>
            <div>○ Audit logging</div>
          </div>
        </section>
      </>
    );
  }

  function renderActivity() {
    return (
      <>
        <div className="page-heading">
          <div>
            <div className="eyebrow">
              SYSTEM TRANSPARENCY
            </div>
            <h1>Activity & Audit</h1>
            <p className="page-subtitle">
              Review the current prototype's operational state.
            </p>
          </div>
        </div>

        <section className="panel">
          <h2>Application Activity</h2>

          <div className="evidence-row">
            <div className="record-icon">✓</div>

            <div className="record-info">
              <strong>Frontend workspace available</strong>
              <span>Local React interface</span>
            </div>

            <span className="status status-success">
              AVAILABLE
            </span>
          </div>

          <div className="evidence-row">
            <div className="record-icon">ⓘ</div>

            <div className="record-info">
              <strong>Security operations</strong>
              <span>
                No live security operations have been executed.
              </span>
            </div>

            <span className="status status-pending">
              INACTIVE
            </span>
          </div>
        </section>
      </>
    );
  }

  function renderSettings() {
    return (
      <>
        <div className="page-heading">
          <div>
            <div className="eyebrow">PREFERENCES</div>
            <h1>Settings</h1>
            <p className="page-subtitle">
              Configure the appearance of your TERVA workspace.
            </p>
          </div>
        </div>

        <section className="panel settings-panel">
          <div>
            <h2>Appearance</h2>
            <p>Choose your preferred interface theme.</p>
          </div>

          <div className="setting-row">
            <div>
              <strong>Dark mode</strong>
              <p>
                Use a darker interface throughout the workspace.
              </p>
            </div>

            <button
              className={`toggle ${darkMode ? "toggle-on" : ""}`}
              onClick={() => setDarkMode(!darkMode)}
              aria-label="Toggle dark mode"
              aria-pressed={darkMode}
            >
              <span />
            </button>
          </div>

          <div className="divider" />

          <div className="setting-row">
            <div>
              <strong>Application</strong>
              <p>
                TERVA — Threat Evidence & Risk Verification Architecture
              </p>
            </div>

            <span className="status status-success">
              v0.1.0
            </span>
          </div>
        </section>
      </>
    );
  }

  function renderPage() {
    switch (activePage) {
      case "Overview":
        return renderOverview();

      case "Evidence Explorer":
        return renderEvidence();

      case "AI Assistant":
        return renderAssistant();

      case "Activity & Audit":
        return renderActivity();

      case "Settings":
        return renderSettings();

      default:
        return renderSecurityModule();
    }
  }

  return (
    <div className={`app-shell ${darkMode ? "dark" : ""}`}>
      <aside className="sidebar">
        {/* TERVA BRAND LOGO */}
        <div className="brand">
          <img
            src="/TERVA.png"
            alt="TERVA Logo"
            className="brand-logo"
          />

          <div className="brand-text">
            <strong>TERVA</strong>
            <span>SECURITY INTELLIGENCE</span>
          </div>
        </div>

        <div className="workspace-label">
          WORKSPACE
        </div>

        <nav className="navigation">
          {sections.map((section) => (
            <div className="nav-section" key={section}>
              <div className="nav-section-title">
                {section}
              </div>

              {navigation
                .filter((item) => item.section === section)
                .map((item) => (
                  <button
                    key={item.name}
                    className={`nav-item ${
                      activePage === item.name
                        ? "nav-active"
                        : ""
                    }`}
                    onClick={() => {
                      setActivePage(item.name);
                      setSearch("");
                    }}
                  >
                    <span className="nav-icon">
                      {item.icon}
                    </span>

                    <span>{item.name}</span>

                    {activePage === item.name && (
                      <span className="active-indicator" />
                    )}
                  </button>
                ))}
            </div>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <div className="operator-avatar">O</div>

          <div className="operator-info">
            <strong>Local Operator</strong>
            <span>Personal Workspace</span>
          </div>

          <span className="operator-menu">•••</span>
        </div>
      </aside>

      <main className="main-area">
        <header className="topbar">
          <div className="breadcrumb">
            <span>TERVA</span>
            <span className="breadcrumb-separator">/</span>
            <strong>{activePage}</strong>
          </div>

          <div className="topbar-actions">
            <span className="environment-label">
              <span className="environment-dot" />
              LOCAL ENVIRONMENT
            </span>

            <button
              className="topbar-avatar"
              onClick={() => setActivePage("Settings")}
              aria-label="Open settings"
            >
              O
            </button>
          </div>
        </header>

        <div className="page-content" key={activePage}>
          {renderPage()}

          <footer className="footer">
            <span>TERVA © 2026</span>
            <span>
              Evidence-driven. Scope-controlled. Verifiable.
            </span>
            <span>VERSION 0.1.0</span>
          </footer>
        </div>
      </main>
    </div>
  );
}

export default App;
