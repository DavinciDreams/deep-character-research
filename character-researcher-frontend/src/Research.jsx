import React, { useState } from "react";

export default function Research() {
  const [characterName, setCharacterName] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    setError(null);

    try {
      const response = await fetch("http://localhost:8000/research_character", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ character_name: characterName }),
      });

      if (!response.ok) {
        const err = await response.text();
        throw new Error(err || "Request failed");
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message || "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section>
      <h2>Research</h2>
      <form onSubmit={handleSubmit} style={{ marginBottom: "1rem" }}>
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
        <button type="submit" disabled={loading} style={{ marginLeft: "1rem" }}>
          {loading ? "Researching..." : "Research"}
        </button>
      </form>
      {result && (
        <div className="research-result" style={{ whiteSpace: "pre-wrap", background: "#f6f8fa", padding: "1rem", borderRadius: "6px" }}>
          <strong>Result:</strong>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
      {error && (
        <div className="research-error" style={{ color: "red", marginTop: "1rem" }}>
          <strong>Error:</strong> {error}
        </div>
      )}
    </section>
  );
}