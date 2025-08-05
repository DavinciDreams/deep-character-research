import React, { useState } from "react";

export default function Compare() {
  const [characterName, setCharacterName] = useState("");
  const [message, setMessage] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setResult(null);
    setError(null);
    setLoading(true);
    try {
      const response = await fetch("http://localhost:8000/compare_ai_responses", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          character_name: characterName,
          message: message,
        }),
      });
      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || "Unknown error");
      }
      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section>
      <h2>Compare AI Responses</h2>
      <form onSubmit={handleSubmit} style={{ marginBottom: "1rem" }}>
        <div>
          <label>
            Character Name:
            <input
              type="text"
              value={characterName}
              onChange={(e) => setCharacterName(e.target.value)}
              required
              style={{ marginLeft: "0.5rem" }}
            />
          </label>
        </div>
        <div style={{ marginTop: "0.5rem" }}>
          <label>
            Message:
            <input
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              required
              style={{ marginLeft: "0.5rem", width: "300px" }}
            />
          </label>
        </div>
        <button type="submit" disabled={loading} style={{ marginTop: "1rem" }}>
          {loading ? "Comparing..." : "Compare"}
        </button>
      </form>
      {error && (
        <div style={{ color: "red", marginBottom: "1rem" }}>
          Error: {error}
        </div>
      )}
      {result && (
        <div>
          <h3>Comparison Result</h3>
          <pre style={{ background: "#f4f4f4", padding: "1em", borderRadius: "4px", overflowX: "auto" }}>
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}
    </section>
  );
}