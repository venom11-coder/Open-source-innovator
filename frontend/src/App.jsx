import { Routes, Route, Navigate } from "react-router-dom";
import About from "./pages/About";
import HowToUse from "./pages/HowToUse";
import Output from "./pages/Output";
import Profile from "./pages/Profile"; // adjust if needed
import Landing from "./pages/Landing";
import Combinations from "./pages/components/Combinations.jsx"; // adjust if needed

import { useAuthUser } from "./firebase/useAuthUser";

function RequireAuth({ children }) {
  const { user, loading } = useAuthUser();
  if (loading) return null;
  if (!user) return <Navigate to="/" replace />;
  return children;
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route
        path="/combinations"
        element={
          <RequireAuth>
            <Combinations />
          </RequireAuth>
        }
      />
      <Route path="/about" element={<About />} />
      <Route path="/how" element={<HowToUse />} />
      <Route path="/output" element={<Output />} />
      <Route path="/profile" element={
          <Profile />
      } />
    </Routes>
  );
}
