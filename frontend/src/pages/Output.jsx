import Navbar from "./components/Navbar";

export default function Output() {
  return (
    <div className="bg">
      <div className="layer">
        <Navbar />
        <div className="container" style={{ padding: "36px 0" }}>
          <div className="card" style={{ padding: 18 }}>
            <h2 style={{ marginTop: 0 }}>Output</h2>
            <p style={{ color: "rgba(255,255,255,0.75)", lineHeight: 1.7 }}>
              This page will show published outputs (timestamped links) once backend is connected.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
