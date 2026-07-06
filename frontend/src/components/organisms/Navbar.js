import { NavLink, Link } from "react-router-dom";

function Navbar() {
  return (
    <nav>
      <Link to="/" className="nav-brand" aria-label="Home">
        <span className="nav-brand__mark">T</span>
        <span className="nav-brand__text">
          <span>Toxicity Shield</span>
          <span>Moderation intelligence</span>
        </span>
      </Link>

      <div className="nav-links">
        <NavLink to="/" end>
          Home
        </NavLink>
        <NavLink to="/toxic">Toxic Comments</NavLink>
        <NavLink to="/bot">Bot Detection</NavLink>
        <NavLink to="/combined">Combined Analysis</NavLink>
      </div>
    </nav>
  );
}

export default Navbar;
