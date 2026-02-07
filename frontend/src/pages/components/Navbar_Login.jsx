import { useState } from "react";
import { useAuthUser } from "../../firebase/useAuthUser";
import { getAuth, signOut } from "firebase/auth";
import { useNavigate } from "react-router-dom";



export default function Profile() {
  const { user } = useAuthUser();
  const navigate = useNavigate();
  const [tab, setTab] = useState("account");

  const doSignOut = async () => {
    await signOut(getAuth());
    navigate("/");
  };

  return (
    <div className="bg">
      <div className="layer">
        <Navbar />

        <div className="container" style={{ paddingTop: 40 }}>
          <div style={{ display: "flex", gap: 28 }}>

            {/* LEFT SIDEBAR */}
            <div
              style={{
                width: 260,
                borderRadius: 18,
                background: "rgba(255,255,255,0.03)",
                border: "1px solid rgba(255,255,255,0.08)",
                padding: 18,
                height: "fit-content"
              }}
            >
              <div style={{ fontWeight: 900, marginBottom: 18 }}>
                Account
              </div>

              <SidebarItem
                label="Account Details"
                active={tab === "account"}
                onClick={() => setTab("account")}
              />

              <SidebarItem
                label="Previous Outputs"
                active={tab === "outputs"}
                onClick={() => setTab("outputs")}
              />

              <SidebarItem
                label="Sign Out"
                danger
                onClick={doSignOut}
              />
            </div>

            {/* RIGHT CONTENT */}
            <div style={{ flex: 1 }}>
              {tab === "account" && (
                <AccountCard user={user} />
              )}

              {tab === "outputs" && (
                <OutputsCard />
              )}
            </div>

          </div>
        </div>
      </div>
    </div>
  );
}

/* ---------------- COMPONENTS ---------------- */

function SidebarItem({ label, active, onClick, danger }) {
  return (
    <div
      onClick={onClick}
      style={{
        padding: "12px 14px",
        borderRadius: 12,
        cursor: "pointer",
        marginBottom: 6,
        fontWeight: 800,
        background: active
          ? "rgba(106,217,255,0.15)"
          : danger
          ? "rgba(255,70,90,0.08)"
          : "transparent",
        border: active
          ? "1px solid rgba(106,217,255,0.35)"
          : "1px solid transparent",
        color: "white"
      }}
    >
      {label}
    </div>
  );
}

function AccountCard({ user }) {
  return (
    <div
      style={{
        borderRadius: 18,
        background: "rgba(255,255,255,0.03)",
        border: "1px solid rgba(255,255,255,0.08)",
        padding: 24
      }}
    >
      <h2 style={{ marginTop: 0 }}>Account Information</h2>

      <InfoRow label="Email" value={user?.email} />
      <InfoRow label="User ID" value={user?.uid} />
      <InfoRow label="Provider" value={user?.providerData?.[0]?.providerId} />
    </div>
  );
}

function OutputsCard() {
  return (
    <div
      style={{
        borderRadius: 18,
        background: "rgba(255,255,255,0.03)",
        border: "1px solid rgba(255,255,255,0.08)",
        padding: 24
      }}
    >
      <h2>Previous Outputs</h2>
      <p style={{ opacity: 0.7 }}>
        Here you can later show OSF timestamped outputs.
      </p>
    </div>
  );
}

function InfoRow({ label, value }) {
  return (
    <div style={{ marginBottom: 18 }}>
      <div style={{ opacity: 0.6, fontSize: 13 }}>{label}</div>
      <div
        style={{
          marginTop: 6,
          padding: 12,
          borderRadius: 12,
          background: "rgba(0,0,0,0.25)",
          border: "1px solid rgba(255,255,255,0.08)"
        }}
      >
        {value || "—"}
      </div>
    </div>
  );
}
