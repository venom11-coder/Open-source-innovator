import { useMemo, useState } from "react";
import { motion } from "framer-motion";
import Navbar from "../components/Navbar";
import PrimaryButton from "../components/PrimaryButton";

const fadeUp = {
  hidden: { opacity: 0, y: 16 },
  show: (i = 0) => ({
    opacity: 1,
    y: 0,
    transition: {
      delay: 0.06 * i,
      duration: 0.55,
      ease: [0.215, 0.61, 0.355, 1],
    },
  }),
};

export default function Submit() {
  const [current, setCurrent] = useState("");
  const [items, setItems] = useState([]);

  const cleanedItems = useMemo(() => items.map((x) => x.trim()).filter(Boolean), [items]);

  const addItem = () => {
    const v = current.trim();
    if (!v) return;

    // prevent exact duplicates (case-insensitive)
    const exists = cleanedItems.some((x) => x.toLowerCase() === v.toLowerCase());
    if (exists) {
      setCurrent("");
      return;
    }

    setItems((prev) => [...prev, v]);
    setCurrent("");
  };

  const removeItem = (idx) => {
    setItems((prev) => prev.filter((_, i) => i !== idx));
  };

  const clearAll = () => {
    setItems([]);
    setCurrent("");
  };

  const onKeyDown = (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      addItem();
    }
  };

  return (
    <div className="bg">
      <div className="layer">
        <Navbar />

        <main className="container hero">
          <motion.div
            className="card"
            style={{ padding: "clamp(20px, 5vw, 40px)", textAlign: "left" }}
            initial="hidden"
            animate="show"
            variants={fadeUp}
          >
            <div style={{ display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap", marginBottom: 18 }}>
              <div className="pill">Input • One per line</div>
              <div className="pill">Timestamp-ready</div>
              <div className="pill">Open innovation</div>
            </div>

            <motion.h1 className="h1" variants={fadeUp} custom={1}>
              Add your materials / concepts
              <span style={{ display: "block", color: "#6ad9ff" }}>
                one at a time
              </span>
            </motion.h1>

            <motion.p className="sub" variants={fadeUp} custom={2} style={{ maxWidth: 820, marginBottom: 24 }}>
              Enter items like polymers, additives, chemicals, or concepts. Press <strong>Enter</strong> after each one.
              We’ll store your list and use it to generate combinatorial innovations with time-date stamps for prior art.
            </motion.p>

            <motion.div variants={fadeUp} custom={3} className="heroGrid" style={{ alignItems: "start" }}>
              {/* LEFT: instructions / context */}
              <div style={{ display: "grid", gap: 16 }}>
                <div className="featureCard" style={{ background: "rgba(255,255,255,0.03)" }}>
                  <div style={{ fontWeight: 900, marginBottom: 10, fontSize: 16 }}>Examples</div>
                  <div style={{ color: "rgba(255,255,255,0.70)", lineHeight: 1.7, fontSize: 14 }}>
                    <p>• PLA</p>
                    <p>• Graphene</p>
                    <p>• Silica</p>
                    <p>• PETG</p>
                    <div style={{ marginTop: 12, fontSize: 13, opacity: 0.8, borderTop: "1px solid rgba(255,255,255,0.1)", paddingTop: 12 }}>
                      Tip: keep each entry short and specific.
                    </div>
                  </div>
                </div>

                <div className="featureCard" style={{ background: "rgba(255,255,255,0.03)" }}>
                  <div style={{ fontWeight: 900, marginBottom: 10, fontSize: 16 }}>Why we collect this</div>
                  <div style={{ color: "rgba(255,255,255,0.70)", lineHeight: 1.7, fontSize: 14 }}>
                    You’re helping create a public, timestamped record of “obvious” combinations so future innovation stays open.
                  </div>
                </div>
              </div>

              {/* RIGHT: input + list */}
              <div
                className="card authBox"
                style={{
                  background: "rgba(255,255,255,0.02)",
                  border: "1px solid rgba(255,255,255,0.08)",
                }}
              >
                <div style={{ marginBottom: 14 }}>
                  <div style={{ fontWeight: 900, fontSize: 18 }}>Your list</div>
                  <div style={{ marginTop: 4, color: "rgba(255,255,255,0.55)", fontSize: 13 }}>
                    Press Enter to add. We’ll store everything you add below.
                  </div>
                </div>

                <div style={{ display: "grid", gap: 10 }}>
                  <div style={{ display: "flex", gap: 10 }}>
                    <input
                      value={current}
                      onChange={(e) => setCurrent(e.target.value)}
                      onKeyDown={onKeyDown}
                      placeholder="Type one item… then press Enter"
                      className="pill"
                      style={{
                        flex: 1,
                        padding: "12px",
                        borderRadius: 12,
                        background: "rgba(255,255,255,0.05)",
                        color: "white",
                      }}
                    />

                    <button
                      type="button"
                      className="pill"
                      onClick={addItem}
                      style={{
                        padding: "12px 14px",
                        borderRadius: 12,
                        background: "rgba(106,217,255,0.12)",
                        border: "1px solid rgba(106,217,255,0.35)",
                        color: "white",
                        cursor: "pointer",
                        fontWeight: 800,
                      }}
                    >
                      Add
                    </button>
                  </div>

                  <div
                    style={{
                      marginTop: 6,
                      padding: 12,
                      borderRadius: 14,
                      border: "1px solid rgba(255,255,255,0.08)",
                      background: "rgba(0,0,0,0.25)",
                      minHeight: 170,
                      maxHeight: 260,
                      overflow: "auto",
                    }}
                  >
                    {cleanedItems.length === 0 ? (
                      <div style={{ color: "rgba(255,255,255,0.45)", fontSize: 13, lineHeight: 1.6 }}>
                        Nothing added yet. Add your first item above.
                      </div>
                    ) : (
                      <div style={{ display: "grid", gap: 8 }}>
                        {cleanedItems.map((x, idx) => (
                          <div
                            key={`${x}-${idx}`}
                            style={{
                              display: "flex",
                              alignItems: "center",
                              justifyContent: "space-between",
                              gap: 10,
                              padding: "10px 12px",
                              borderRadius: 12,
                              background: "rgba(255,255,255,0.04)",
                              border: "1px solid rgba(255,255,255,0.07)",
                            }}
                          >
                            <div style={{ fontSize: 14, color: "rgba(255,255,255,0.9)" }}>
                              {idx + 1}. {x}
                            </div>

                            <button
                              type="button"
                              onClick={() => removeItem(idx)}
                              className="pill"
                              style={{
                                padding: "6px 10px",
                                borderRadius: 10,
                                background: "rgba(255,70,90,0.10)",
                                border: "1px solid rgba(255,70,90,0.25)",
                                color: "rgba(255,255,255,0.9)",
                                cursor: "pointer",
                                fontSize: 12,
                                fontWeight: 800,
                              }}
                            >
                              Remove
                            </button>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>

                  <div style={{ display: "flex", gap: 10, marginTop: 6 }}>
                    <button
                      type="button"
                      className="pill"
                      onClick={clearAll}
                      style={{
                        padding: "12px",
                        borderRadius: 12,
                        background: "rgba(255,255,255,0.06)",
                        border: "1px solid rgba(255,255,255,0.10)",
                        color: "white",
                        cursor: "pointer",
                        fontWeight: 800,
                        flex: 1,
                      }}
                    >
                      Clear
                    </button>

                    <PrimaryButton
                      style={{ flex: 1 }}
                      onClick={() => {
                        // later: send cleanedItems to backend / store in DB / generate combos
                        console.log("Saved list:", cleanedItems);
                        alert(`Saved ${cleanedItems.length} items`);
                      }}
                    >
                      Continue
                    </PrimaryButton>
                  </div>

                  <div style={{ fontSize: 11, color: "rgba(255,255,255,0.45)", lineHeight: 1.5, marginTop: 4 }}>
                    Next step can generate all pairwise combinations and publish with a timestamp (e.g., OSF).
                  </div>
                </div>
              </div>
            </motion.div>
          </motion.div>

          <footer className="footer" style={{ textAlign: "center", marginTop: 40 }}>
            Built for combinatorial innovation • 2026 • v1.0.4
          </footer>
        </main>
      </div>
    </div>
  );
}
