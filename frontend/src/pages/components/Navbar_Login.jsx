import { Link, NavLink } from "react-router-dom";

export default function Navbar() {
  return (
    <div className="navbar">
      <div className="container">
        <div className="navRow">
          <Link to="/" style={{ display: "flex", gap: 10, alignItems: "center" }}>
            <div className="iconBadge">OI</div>
            <div>
              <div style={{ fontSize: 12, color: "rgba(255,255,255,0.65)" }}>
                Open Innovation
              </div>
              <div style={{ fontWeight: 900, letterSpacing: "-0.01em" }}>
                Prior-Art Generator
              </div>
            </div>
          </Link>

          <div className="navLinks">
            <NavLink to="/Combinations">Combinations</NavLink>
            <NavLink to="/about">About</NavLink>
            <NavLink to="/how">How to use</NavLink>
            <NavLink to="/output">Output</NavLink>
          </div>
        </div>
      </div>
    </div>
  );
}
