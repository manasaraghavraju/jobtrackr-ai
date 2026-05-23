import {Link}  from "react-router-dom";
function Navbar() {
  return (
    <nav className="navbar">
        <h2>JobTracker AI</h2>
        <div className="nav-links">
          <Link to="/">Dashboard</Link>
          <Link to="/leetcode">LeetCode</Link>
          <Link to="/applications">Applications</Link>
          <Link to="/contacts">Contacts</Link>
        </div>
      </nav>
  );
}

export default Navbar;