import { Routes, Route } from "react-router-dom";
import About from "./pages/About";
import HowToUse from "./pages/HowToUse";
import Output from "./pages/Output";
import Landing from "./pages/Landing";
import Combinations from "./pages/components/Combinations.jsx";



export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route path="/Combinations" element={<Combinations />} />
      <Route path="/about" element={<About />} />
      <Route path="/how" element={<HowToUse />} />
      <Route path="/output" element={<Output />} />
    </Routes>
  );
}
