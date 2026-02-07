// src/pages/components/Navbar_Login.jsx
import { Link, useNavigate } from "react-router-dom";
import { useAuthUser } from "../../firebase/useAuthUser";
import { getAuth, signOut } from "firebase/auth";
import { useEffect, useRef, useState } from "react";

export default function Navbar_Login() {
  const { user } = useAuthUser();
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);
  const menuRef = useRef(null);

  useEffect(() => {
    const onDown = (e) => {
      if (!menuRef.current) return;
      if (!menuRef.current.contains(e.target)) setOpen(false);
    };
    window.addEventListener("mousedown", onDown);
    return () => window.removeEventListener("mousedown", onDown);
  }, []);

  const doSignOut = async () => {
    await signOut(getAuth());
    setOpen(false);
    navigate("/", { replace: true });
  };

  const initials = (user?.displayName || user?.email || "U").slice(0, 1).toUpperCase();
  const photo = user?.photoURL;

  return (
    <div
      style={{
        position: "sticky",
        top: 0,
        zIndex: 50,
        backdropFilter: "blur(10px)",
        background: "rgba(8,10,16,0.55)",
        borderBottom: "1px solid rgba(255,255,255,0.08)",
      }}
    >
      <div className="container" style={{ padding: "14px 0", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        {/* LEFT BRAND */}
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <div
            style={{
              width: 34,
              height: 34,
              borderRadius: 12,
              background: "rgba(255,255,255,0.06)",
              border: "1px solid rgba(255,255,255,0.10)",
              display: "grid",
              placeItems: "center",
              fontWeight: 950,
            }}
          >
            OI
          </div>
          <div style={{ lineHeight: 1.1 }}>
            <div style={{ fontWeight: 900, fontSize: 14, color: "rgba(255,255,255,0.9)" }}>Open Innovation</div>
            <div style={{ fontWeight: 950, fontSize: 16 }}>Prior-Art Generator</div>
          </div>
        </div>

        {/* RIGHT LINKS */}
        <div style={{ display: "flex", alignItems: "center", gap: 18 }}>
          <NavItem to="/combinations">Combinations</NavItem>
          <NavItem to="/about">About</NavItem>
          <NavItem to="/how">How to use</NavItem>
          <NavItem to="/output">Output</NavItem>

          {/* PROFILE DROPDOWN */}
          <div ref={menuRef} style={{ position: "relative" }}>
            <button
              onClick={() => setOpen((v) => !v)}
              className="pill"
              style={{
                display: "inline-flex",
                alignItems: "center",
                gap: 10,
                padding: "8px 10px",
                borderRadius: 14,
                background: "rgba(255,255,255,0.06)",
                border: "1px solid rgba(255,255,255,0.10)",
                color: "white",
                cursor: "pointer",
                fontWeight: 900,
              }}
            >
              <div
                style={{
                  width: 28,
                  height: 28,
                  borderRadius: 10,
                  overflow: "hidden",
                  background: "rgba(255,255,255,0.08)",
                  border: "1px solid rgba(255,255,255,0.10)",
                  display: "grid",
                  placeItems: "center",
                  fontWeight: 950,
                }}
              >
                {photo ? (
                  <img src={photo} alt="avatar" style={{ width: "100%", height: "100%", objectFit: "cover" }} />
                ) : (
                  initials
                )}
              </div>
              <span style={{ opacity: 0.9 }}>Profile</span>
              <span style={{ opacity: 0.6 }}>▾</span>
            </button>

            {open && (
              <div
                style={{
                  position: "absolute",
                  right: 0,
                  marginTop: 10,
                  width: 260,
                  borderRadius: 16,
                  background: "rgba(12,14,20,0.92)",
                  border: "1px solid rgba(255,255,255,0.10)",
                  boxShadow: "0 22px 70px rgba(0,0,0,0.55)",
                  overflow: "hidden",
                }}
              >
                <div style={{ padding: 14, borderBottom: "1px solid rgba(255,255,255,0.08)" }}>
                  <div style={{ fontWeight: 950, fontSize: 13, color: "rgba(255,255,255,0.9)" }}>
                    {user?.displayName || "Account"}
                  </div>
                  <div style={{ marginTop: 4, fontSize: 12, color: "rgba(255,255,255,0.60)" }}>
                    {user?.email || "—"}
                  </div>
                </div>

                <MenuBtn
                  label="Account details"
                  onClick={() => {
                    setOpen(false);
                    navigate("/profile");
                  }}
                />
                <MenuBtn
                  label="Previous outputs"
                  onClick={() => {
                    setOpen(false);
                    navigate("/output");
                  }}
                />
                <div style={{ borderTop: "1px solid rgba(255,255,255,0.08)" }} />
                <MenuBtn label="Sign out" danger onClick={doSignOut} />
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

function NavItem({ to, children }) {
  return (
    <Link
      to={to}
      style={{
        textDecoration: "none",
        color: "rgba(255,255,255,0.85)",
        fontWeight: 800,
        fontSize: 14,
      }}
    >
      {children}
    </Link>
  );
}

function MenuBtn({ label, onClick, danger }) {
  return (
    <button
      onClick={onClick}
      style={{
        width: "100%",
        textAlign: "left",
        padding: "12px 14px",
        background: danger ? "rgba(255,70,90,0.10)" : "transparent",
        border: "none",
        color: "white",
        cursor: "pointer",
        fontWeight: 900,
        fontSize: 13,
      }}
    >
      {label}
    </button>
  );
}
