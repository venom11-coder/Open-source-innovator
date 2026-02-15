import { useEffect, useState } from "react";
import Navbar from "./components/Navbar_Login";
import { getRecentOutputs, clearRecentOutputs } from "./recentOutputs";

export default function OutputPage() {
  const [outputs, setOutputs] = useState([]);

  useEffect(() => {
    setOutputs(getRecentOutputs());
  }, []);

  return (
    <div className="bg">
      <div className="layer">
        <Navbar />

        <main className="container hero">
          <div className="card" style={{ padding: "clamp(20px, 5vw, 40px)" }}>
            <div style={{ fontWeight: 950, fontSize: 22, marginBottom: 12 }}>
              Previous outputs
            </div>

            <div style={{ color: "rgba(255,255,255,0.6)", marginBottom: 18 }}>
              Last 10 published outputs stored on this device.
            </div>

            {outputs.length === 0 ? (
              <div style={{ color: "rgba(255,255,255,0.55)" }}>
                No outputs yet.
              </div>
            ) : (
              <div style={{ display: "grid", gap: 10 }}>
                {outputs.map((o, i) => {
                  const d = new Date(o.created_at);
                  const label = d.toLocaleString(undefined, {
                    year: "numeric",
                    month: "short",
                    day: "numeric",
                    hour: "2-digit",
                    minute: "2-digit",
                  });

                  return (
                    <div
                      key={i}
                      style={{
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "center",
                        padding: "12px 14px",
                        borderRadius: 14,
                        background: "rgba(255,255,255,0.04)",
                        border: "1px solid rgba(255,255,255,0.08)",
                      }}
                    >
                      <div style={{ fontWeight: 850, color: "rgba(255,255,255,0.85)" }}>
                        {label}
                      </div>

                      <button
                        className="pill"
                        onClick={() => window.open(o.osf_url, "_blank", "noopener,noreferrer")}
                        style={{
                          padding: "8px 12px",
                          borderRadius: 10,
                          background: "rgba(106,217,255,0.12)",
                          border: "1px solid rgba(106,217,255,0.30)",
                          color: "white",
                          fontWeight: 900,
                          cursor: "pointer",
                        }}
                      >
                        View →
                      </button>
                    </div>
                  );
                })}
              </div>
            )}

            {outputs.length > 0 && (
              <div style={{ marginTop: 16, display: "flex", justifyContent: "flex-end" }}>
                <button
                  className="pill"
                  onClick={() => {
                    clearRecentOutputs();
                    setOutputs([]);
                  }}
                  style={{
                    padding: "10px 12px",
                    borderRadius: 12,
                    background: "rgba(255,70,90,0.10)",
                    border: "1px solid rgba(255,70,90,0.25)",
                    color: "white",
                    cursor: "pointer",
                    fontWeight: 900,
                  }}
                >
                  Clear history
                </button>
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  );
}
