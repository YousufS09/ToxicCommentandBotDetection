import { useState } from "react";
import { predictToxic } from "../../services/api";
import Button from "../atoms/Button";
import TextArea from "../atoms/TextArea";

function ToxicCommentsDetection() {
  const [comment, setComment] = useState("");
  const [result, setResult] = useState(null);
  const [confidence, setConfidence] = useState(null);
  const [interpretation, setInterpretation] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const getInterpretation = (label, score) => {
    if (label === "Toxic") {
      if (score >= 0.8) return "Very strong toxicity signal.";
      if (score >= 0.6) return "Moderate toxicity signal.";
      return "Possible toxic language detected.";
    }

    if (score >= 0.8) return "Very likely non-toxic.";
    if (score >= 0.6) return "Mostly non-toxic.";
    return "Mixed tone, review with context.";
  };

  const handleAnalyze = async () => {
    if (comment.trim().length < 5) {
      setError("Please enter at least 5 characters.");
      return;
    }

    setLoading(true);
    setError(null);
    setInterpretation("");

    try {
      const response = await predictToxic(comment);
      setResult(response.label);
      setConfidence(response.confidence);
      setInterpretation(response.interpretation ?? "");
    } catch (err) {
      setError("Failed to analyze comment. Backend not reachable.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container">
      <p>Analyze whether a comment is toxic or non-toxic.</p>

      <TextArea
        rows="4"
        placeholder="Enter a comment here"
        value={comment}
        onChange={(e) => setComment(e.target.value)}
      />

      <small className="form-field__hint">
        Longer comments produce a more reliable toxicity score.
      </small>

      <Button onClick={handleAnalyze} disabled={loading || !comment.trim()}>
        {loading ? "Analyzing..." : "Analyze"}
      </Button>

      {error && <p className="result-danger">{error}</p>}

      {result && (
        <div className="result-box">
          <p>
            <strong>Result:</strong> {result}
          </p>
          <p>
            <strong>Confidence:</strong>{" "}
            {(confidence * 100).toFixed(2)}%
          </p>
          <p>{interpretation || getInterpretation(result, confidence ?? 0)}</p>
        </div>
      )}
    </div>
  );
}

export default ToxicCommentsDetection;
