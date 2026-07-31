import { Link, useLocation } from "react-router-dom";
import { API_BASE } from "../api/client";

export default function Layout({ children }) {
  const { pathname } = useLocation();

  return (
    <div className="app-layout">
      <nav className="app-nav">
        <Link to="/" className="app-nav__brand">
          <span className="app-nav__logo">S</span>
          Searchie
        </Link>
        <div className="app-nav__links">
          <Link
            to="/"
            className={`app-nav__link ${pathname === "/" ? "app-nav__link--active" : ""}`}
          >
            Research
          </Link>
          <a
            href={`${API_BASE}/docs`}
            target="_blank"
            rel="noreferrer"
            className="app-nav__link"
          >
            API Docs
          </a>
        </div>
      </nav>
      <main className="app-main">{children}</main>
    </div>
  );
}
