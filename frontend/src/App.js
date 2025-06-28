import React, { useState, useEffect } from "react";

function App() {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [history, setHistory] = useState([]);
  const [showHistory, setShowHistory] = useState(false);
  const [historyLoading, setHistoryLoading] = useState(false);

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

      if (!res.ok) {
        throw new Error("Failed to get response");
      }

      const data = await res.json();
      setResponse(data.response);
      setQuestion(""); // Clear input after sending

      // Refresh history if it's currently shown
      if (showHistory) {
        fetchHistory();
      }
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
        "http://localhost:8000/api/v1/history?page=1&per_page=10"
      );
      if (!res.ok) {
        throw new Error("Failed to fetch history");
      }
      const data = await res.json();
      setHistory(data.questions || []);
    } catch (err) {
      console.error("Error fetching history:", err);
      setError("Failed to load conversation history.");
    } finally {
      setHistoryLoading(false);
    }
  };

  const toggleHistory = () => {
    setShowHistory(!showHistory);
    if (!showHistory) {
      fetchHistory();
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
    <div className="min-h-screen bg-gray-50 p-4 md:p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            🧪 Crewmind Assistant
          </h1>
          <p className="text-gray-600">
            Ask me anything and I'll help you out!
          </p>
        </div>

        {/* Navigation */}
        <div className="flex justify-center mb-6">
          <div className="bg-white rounded-lg shadow-sm p-1 flex">
            <button
              onClick={() => setShowHistory(false)}
              className={`px-4 py-2 rounded-md font-medium transition-colors ${
                !showHistory
                  ? "bg-blue-600 text-white"
                  : "text-gray-600 hover:text-gray-900"
              }`}
            >
              Ask Question
            </button>
            <button
              onClick={toggleHistory}
              className={`px-4 py-2 rounded-md font-medium transition-colors ${
                showHistory
                  ? "bg-blue-600 text-white"
                  : "text-gray-600 hover:text-gray-900"
              }`}
            >
              History ({history.length})
            </button>
          </div>
        </div>

        {!showHistory ? (
          /* Ask Question View */
          <div className="bg-white rounded-lg shadow-lg p-6">
            {/* Input Section */}
            <div className="space-y-4">
              <div>
                <label
                  htmlFor="question"
                  className="block text-sm font-medium text-gray-700 mb-2"
                >
                  Your Question
                </label>
                <textarea
                  id="question"
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Ask something..."
                  rows={4}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none"
                />
                <div className="text-right text-sm text-gray-500 mt-1">
                  {question.length}/1000 characters
                </div>
              </div>

              <button
                onClick={handleSend}
                disabled={loading || !question.trim() || question.length > 1000}
                className={`w-full py-2 px-4 rounded-md font-medium transition-colors ${
                  loading || !question.trim() || question.length > 1000
                    ? "bg-gray-300 text-gray-500 cursor-not-allowed"
                    : "bg-blue-600 text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                }`}
              >
                {loading ? "Sending..." : "Send"}
              </button>
            </div>

            {/* Error Message */}
            {error && (
              <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-md">
                <p className="text-red-700 text-sm">{error}</p>
              </div>
            )}

            {/* Response Section */}
            {response && (
              <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-md">
                <h3 className="text-lg font-semibold text-green-800 mb-2">
                  Response:
                </h3>
                <p className="text-green-700">{response}</p>
              </div>
            )}

            {/* Instructions */}
            <div className="text-center mt-6 text-gray-500 text-sm">
              Press Enter to send • Shift+Enter for new line
            </div>
          </div>
        ) : (
          /* History View */
          <div className="bg-white rounded-lg shadow-lg p-6">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold text-gray-900">
                Conversation History
              </h2>
              <button
                onClick={fetchHistory}
                disabled={historyLoading}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-300 transition-colors"
              >
                {historyLoading ? "Loading..." : "Refresh"}
              </button>
            </div>

            {historyLoading ? (
              <div className="text-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
                <p className="text-gray-500 mt-2">Loading history...</p>
              </div>
            ) : history.length === 0 ? (
              <div className="text-center py-8">
                <p className="text-gray-500">
                  No conversation history yet. Ask your first question!
                </p>
              </div>
            ) : (
              <div className="space-y-4">
                {history.map((item, index) => (
                  <div
                    key={index}
                    className="border border-gray-200 rounded-lg p-4"
                  >
                    <div className="mb-3">
                      <div className="flex justify-between items-start mb-2">
                        <h4 className="font-medium text-gray-900">Question:</h4>
                        <span className="text-xs text-gray-500">
                          {formatTimestamp(item.timestamp)}
                        </span>
                      </div>
                      <p className="text-gray-700 bg-gray-50 p-3 rounded-md">
                        {item.question}
                      </p>
                    </div>
                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">
                        Response:
                      </h4>
                      <p className="text-gray-700 bg-blue-50 p-3 rounded-md">
                        {item.response}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
