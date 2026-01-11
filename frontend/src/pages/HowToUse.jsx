import Navbar from "./components/Navbar";

export default function HowToUse() {
  return (
    <div className="bg">
      <div className="layer">
        <Navbar />
        <div className="container" style={{ padding: "36px 0" }}>
          <div className="card" style={{ padding: 18 }}>
            <h2 style={{ marginTop: 0 }}>How to use</h2>
            <ol style={{ color: "rgba(255,255,255,0.75)", lineHeight: 1.8 }}>
              <li>Sign in (or use manual mode).</li>
              <li>Paste lists of materials/concepts.</li>
              <li>Choose combination rules.</li>
              <li>Generate and publish timestamped output.</li>
            </ol>
          </div>
        </div>
      </div>
    </div>
  );
}
