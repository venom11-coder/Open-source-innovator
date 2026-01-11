import Navbar from "./components/Navbar";

export default function About() {
  return (
    <div className="bg">
      <div className="layer">
        <Navbar />
        <div className="container" style={{ padding: "36px 0" }}>
          <div className="card" style={{ padding: 18 }}>
            <h2 style={{ marginTop: 0 }}>About</h2>
            <p style={{ color: "rgba(255,255,255,0.75)", lineHeight: 1.7 }}>
              This tool helps users generate combinatorial innovation ideas and publish timestamped outputs
              to establish prior art under open licenses.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
