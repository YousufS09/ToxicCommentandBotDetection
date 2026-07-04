import { useState } from "react";
import { predictBot } from "../../services/botService";
import Button from "../atoms/Button";
import FormField from "../molecules/FormField";

function BotDetection() {
  const [formData, setFormData] = useState({
    description: "",
    followers_count: "",
    following_count: "",
    tweet_count: "",
    created_at: "",
  });

  const [result, setResult] = useState(null);
  const [confidence, setConfidence] = useState(null);
  const [interpretation, setInterpretation] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [fieldErrors, setFieldErrors] = useState({});

  const validate = () => {
    const errors = {};

    if (
      !formData.description.trim() &&
      formData.followers_count === "" &&
      formData.following_count === "" &&
      formData.tweet_count === "" &&
      !formData.created_at
    ) {
      errors.form = "Enter at least one profile field before analyzing.";
    }

    ["followers_count", "following_count", "tweet_count"].forEach((field) => {
      if (formData[field] !== "" && Number(formData[field]) < 0) {
        errors[field] = "Values cannot be negative.";
      }
    });

    return errors;
  };

  const interpret = (prediction, score) => {
    if (prediction === "Bot") {
      if (score >= 0.8) return "High bot likelihood.";
      if (score >= 0.6) return "Moderate bot likelihood.";
      return "Some bot-like signals were found.";
    }

    if (score >= 0.8) return "Strong human-like profile.";
    if (score >= 0.6) return "Mostly human-like profile.";
    return "Profile looks human, but review with context.";
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleAnalyze = async () => {
    setError("");
    const errors = validate();
    setFieldErrors(errors);

    if (Object.keys(errors).length > 0) {
      setError("Please fix the highlighted fields before analyzing.");
      return;
    }

    setResult(null);
    setConfidence(null);
    setInterpretation("");
    setLoading(true);

    try {
      const response = await predictBot({
        description: formData.description,
        followers_count: Number(formData.followers_count),
        following_count: Number(formData.following_count),
        tweet_count: Number(formData.tweet_count),
        created_at: formData.created_at,
      });

      setResult(response.prediction ?? "Unknown");
      setConfidence(response.confidence ?? null);
      setInterpretation(response.interpretation ?? "");
    } catch (err) {
      setError("Failed to analyze user. Backend not reachable.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container">
      <p>Check whether a Twitter account is a bot or human.</p>

      <FormField
        label="User bio / description"
        name="description"
        type="text"
        placeholder="Short bio or description"
        value={formData.description}
        onChange={handleChange}
        hint="Optional, but useful for bot detection."
      />

      <FormField
        label="Followers count"
        name="followers_count"
        type="number"
        min="0"
        placeholder="0"
        value={formData.followers_count}
        onChange={handleChange}
        error={fieldErrors.followers_count}
      />

      <FormField
        label="Following count"
        name="following_count"
        type="number"
        min="0"
        placeholder="0"
        value={formData.following_count}
        onChange={handleChange}
        error={fieldErrors.following_count}
      />

      <FormField
        label="Tweet count"
        name="tweet_count"
        type="number"
        min="0"
        placeholder="0"
        value={formData.tweet_count}
        onChange={handleChange}
        error={fieldErrors.tweet_count}
      />

      <FormField
        label="Created at"
        name="created_at"
        type="date"
        value={formData.created_at}
        onChange={handleChange}
        hint="Leave blank if you only know account age."
      />

      <Button onClick={handleAnalyze} disabled={loading}>
        {loading ? "Analyzing..." : "Analyze User"}
      </Button>

      {fieldErrors.form && <p className="result-danger">{fieldErrors.form}</p>}
      {result && (
        <div className="result-box">
          <strong>Prediction:</strong> {result}
          {confidence !== null && (
            <p>
              <strong>Confidence:</strong> {(confidence * 100).toFixed(2)}%
            </p>
          )}
          <p>{interpretation || interpret(result, confidence ?? 0)}</p>
        </div>
      )}

      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

export default BotDetection;
