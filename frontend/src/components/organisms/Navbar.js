import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav>
      <Link to="/">Home</Link>
      <Link to="/toxic">Toxic Comments</Link>
      <Link to="/bot">Bot Detection</Link>
      <Link to="/combined">Combined Analysis</Link>
    </nav>
  );
}

export default Navbar;
