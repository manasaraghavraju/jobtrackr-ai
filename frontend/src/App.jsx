import {Routes, Route} from "react-router-dom";
import Navbar from "./components/Navbar";
import Dashboard from "./pages/Dashboard";
import LeetCode from "./pages/LeetCode";
import Applications from "./pages/Applications";
import Contacts from "./pages/Contacts";
import "./index.css";

function App() {
  return (
    <div>
      <Navbar />
      <main className="page-container">
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/leetcode" element={<LeetCode />} />
        <Route path="/applications" element={<Applications />} />
        <Route path="/contacts" element={<Contacts />} />
      </Routes>
      </main>
    </div>
  );
}

export default App;