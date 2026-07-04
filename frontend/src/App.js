import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import ToxicCommentsPage from "./pages/ToxicCommentsPage";
import BotPage from "./pages/BotPage";
import CombinedAnalysisPage from "./pages/CombinedAnalysisPage";
import Navbar from "./components/organisms/Navbar";
import "./App.css";

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <div className="app-container">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/toxic" element={<ToxicCommentsPage />} />
          <Route path="/bot" element={<BotPage />} />
          <Route path="/combined" element={<CombinedAnalysisPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
