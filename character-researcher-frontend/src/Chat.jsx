import React, { useState } from "react";

export default function Chat() {
  const [characterName, setCharacterName] = useState("");
  const [message, setMessage] = useState("");
  const [aiProvider, setAiProvider] = useState("");
  const [model, setModel] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setResult(null);
    setError(null);
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/chat_with_character", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          character_name: characterName,
          message,
          ai_provider: aiProvider || undefined,
          model: model || undefined,
        }),
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.detail || "Unknown error");
      } else if (data.response) {
        setResult(data.response);
      } else if (data.result) {
        setResult(data.result);
      } else {
        setError("Unexpected response format");
      }
    } catch (err) {
      setError("Network error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section>
      <h2>Chat</h2>
      <form onSubmit={handleSubmit} style={{ maxWidth: 400 }}>
        <div>
          <label>
            Character Name<span style={{ color: "red" }}>*</span>
            <input
              type="text"
              value={characterName}
              onChange={e => setCharacterName(e.target.value)}
              required
              autoComplete="off"
            />
          </label>
        </div>
        <div>
          <label>
            Message<span style={{ color: "red" }}>*</span>
            <textarea
              value={message}
              onChange={e => setMessage(e.target.value)}
              required
              rows={3}
            />
          </label>
        </div>
        <div>
          <label>
            AI Provider
            <input
              type="text"
              value={aiProvider}
              onChange={e => setAiProvider(e.target.value)}
              placeholder="(optional)"
              autoComplete="off"
            />
          </label>
        </div>
        <div>
          <label>
            Model
            <input
              type="text"
              value={model}
              onChange={e => setModel(e.target.value)}
              placeholder="(optional)"
              autoComplete="off"
            />
          </label>
        </div>
        <button type="submit" disabled={loading}>
          {loading ? "Sending..." : "Send"}
        </button>
      </form>
      {result && (
        <div style={{ marginTop: 16, whiteSpace: "pre-wrap" }}>
          <strong>Character Response:</strong>
          <div>{result}</div>
        </div>
      )}
      {error && (
        <div style={{ marginTop: 16, color: "red" }}>
          <strong>Error:</strong> {error}
        </div>
      )}
    </section>
  );
}