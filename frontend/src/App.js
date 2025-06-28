import React, { useState, useEffect, useRef } from "react";

function App() {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [history, setHistory] = useState([]);
  const [historyLoading, setHistoryLoading] = useState(false);
  const chatEndRef = useRef(null);

  useEffect(() => {
    fetchHistory();
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [history]);

  const handleSend = async () => {
    if (!question.trim()) return;
    setLoading(true);
    setError("");
    try {
      const res = await fetch("http://localhost:8000/api/v1/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });
      if (!res.ok) throw new Error("Failed to get response");
      setQuestion("");
      fetchHistory();
    } catch (err) {
      setError("Failed to send question. Make sure the backend is running.");
      console.error("Error:", err);
    } finally {
      setLoading(false);
    }
  };

  const fetchHistory = async () => {
    setHistoryLoading(true);
    try {
      const res = await fetch(
        "http://localhost:8000/api/v1/history?page=1&per_page=100"
      );
      if (!res.ok) throw new Error("Failed to fetch history");
      const data = await res.json();
      setHistory(data.questions || []);
    } catch (err) {
      setError("Failed to load conversation history.");
      console.error("Error fetching history:", err);
    } finally {
      setHistoryLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleString();
  };

  return (
    <div className="main-container">
      <div className="chatbot-wrapper">
        {/* Header */}
        <div className="chatbot-header">
          <div className="chatbot-title">🧪 Crewmind Assistant</div>
          <div className="chatbot-subtitle">
            Ask me anything and I'll help you out!
          </div>
        </div>

        {/* Chat History */}
        <div className="chat-area custom-scrollbar">
          {historyLoading ? (
            <div className="loading-container">
              <div className="loading-spinner"></div>
              <p style={{ marginTop: "10px" }}>Loading history...</p>
            </div>
          ) : history.length === 0 ? (
            <div className="empty-state">
              No conversation history yet. <br />
              <span className="empty-state-highlight">
                Ask your first question!
              </span>
            </div>
          ) : (
            <div className="chat-messages">
              {history
                .slice()
                .reverse()
                .map((item, idx) => (
                  <div key={idx}>
                    {/* User message */}
                    <div className="message-container user">
                      <div className="message-bubble user">
                        <div className="message-content">
                          <span className="message-label user">You:</span>
                          {item.question}
                        </div>
                        <div className="message-timestamp user">
                          {formatTimestamp(item.timestamp)}
                        </div>
                      </div>
                    </div>

                    {/* Assistant response */}
                    <div className="message-container assistant">
                      <div className="message-bubble assistant">
                        <div className="message-content">
                          <span className="message-label assistant">
                            Assistant:
                          </span>
                          {item.response}
                        </div>
                        <div className="message-timestamp assistant">
                          {formatTimestamp(item.timestamp)}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              <div ref={chatEndRef} />
            </div>
          )}
        </div>

        {/* Input Area */}
        <div className="input-area">
          <form
            className="input-form"
            onSubmit={(e) => {
              e.preventDefault();
              handleSend();
            }}
          >
            <div className="input-field">
              <textarea
                id="question"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Type your message..."
                rows={1}
                className="input-textarea"
                disabled={loading}
              />
            </div>
            <button
              type="submit"
              disabled={loading || !question.trim() || question.length > 1000}
              className="send-button"
            >
              {loading ? "Sending..." : "Send"}
            </button>
          </form>

          <div className="input-footer">
            <div className="character-count">
              {question.length}/1000 characters
            </div>
            {error && <div className="error-message">{error}</div>}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
