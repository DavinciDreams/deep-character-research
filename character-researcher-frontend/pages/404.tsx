import React from "react";

const Custom404: React.FC = () => (
  <div style={{
    minHeight: "100vh",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    background: "#f8fafc",
    color: "#1e293b",
    fontFamily: "inherit"
  }}>
    <h1 style={{ fontSize: "4rem", marginBottom: "1rem" }}>404</h1>
    <h2 style={{ fontSize: "2rem", marginBottom: "1rem" }}>Page Not Found</h2>
    <p style={{ fontSize: "1.25rem", marginBottom: "2rem", textAlign: "center" }}>
      Sorry, the page you are looking for does not exist.<br />
      Please check the URL or return to the homepage.
    </p>
    <a href="/" style={{
      padding: "0.75rem 1.5rem",
      background: "#2563eb",
      color: "#fff",
      borderRadius: "0.5rem",
      textDecoration: "none",
      fontWeight: 600
    }}>
      Go Home
    </a>
  </div>
);

export default Custom404;