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
      <main className="app-container">
        <div className="page-shell">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/toxic" element={<ToxicCommentsPage />} />
            <Route path="/bot" element={<BotPage />} />
            <Route path="/combined" element={<CombinedAnalysisPage />} />
          </Routes>
        </div>
      </main>
    </BrowserRouter>
  );
}

export default App;
