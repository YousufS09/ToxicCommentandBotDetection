import { useState } from "react";
import { analyzeCombined } from "../../services/combinedService";
import Button from "../atoms/Button";
import FormField from "../molecules/FormField";

function CombinedAnalysis() {
  const [comment, setComment] = useState("");
  const [userMeta, setUserMeta] = useState({
    description: "",
    followers: "",
    following: "",
    tweets: "",
    accountAge: "",
  });

  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [fieldErrors, setFieldErrors] = useState({});

  const validate = () => {
    const errors = {};

    if (comment.trim().length < 5) {
      errors.comment = "Enter at least 5 characters to analyze the comment.";
    }

    const numericFields = [
      ["followers", "Followers count"],
      ["following", "Following count"],
      ["tweets", "Tweet count"],
      ["accountAge", "Account age"],
    ];

    numericFields.forEach(([key, label]) => {
      if (userMeta[key] !== "" && Number(userMeta[key]) < 0) {
        errors[key] = `${label} cannot be negative.`;
      }
    });

    return errors;
  };

  const toRiskLabel = (score) => {
    if (score >= 0.75) return "High concern";
    if (score >= 0.45) return "Needs review";
    return "Low concern";
  };

  const handleAnalyze = async () => {
    const errors = validate();
    setFieldErrors(errors);

    if (Object.keys(errors).length > 0) {
      setError("Please fix the highlighted fields before analyzing.");
      return;
    }

    setError("");
    setResult(null);
    setLoading(true);

    try {
      const analysis = await analyzeCombined({
        comment,
        description: userMeta.description,
        followers_count: Number(userMeta.followers),
        following_count: Number(userMeta.following),
        tweet_count: Number(userMeta.tweets),
        account_age_days: Number(userMeta.accountAge),
      });

      const toxicityLabel = analysis.toxic?.label ?? "Unknown";
      const toxicityConfidence = analysis.toxic?.confidence ?? 0;
      const botLabel = analysis.bot?.prediction ?? "Unknown";
      const botConfidence = analysis.bot?.confidence ?? 0;

      setResult({
        toxicityLabel,
        toxicityConfidence,
        botLabel,
        botConfidence,
        toxicityRisk: analysis.toxicity_risk ?? 0,
        botRisk: analysis.bot_risk ?? 0,
        finalRiskScore: analysis.risk_score ?? 0,
        finalRisk: analysis.risk_level ?? "Low Risk",
        summary: analysis.summary ?? "",
        recommendation: analysis.recommendation ?? "",
      });
    } catch (err) {
      console.error(err);
      setError("Failed to perform combined analysis.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container">
      <h2>Combined Toxic & Bot Analysis</h2>

      <section>
        <h3>Comment Analysis</h3>
        <FormField
          label="Comment"
          as="textarea"
          rows="4"
          placeholder="Enter a comment"
          value={comment}
          onChange={(e) => setComment(e.target.value)}
          hint="Use a full comment or post, not a single word."
          error={fieldErrors.comment}
        />
      </section>

      <section>
        <h3>User Metadata</h3>

        <FormField
          label="Profile Description"
          type="text"
          placeholder="Short bio or description"
          value={userMeta.description}
          onChange={(e) =>
            setUserMeta({ ...userMeta, description: e.target.value })
          }
          hint="Optional, but it improves bot detection."
        />

        <FormField
          label="Followers Count"
          type="number"
          min="0"
          placeholder="0"
          value={userMeta.followers}
          onChange={(e) =>
            setUserMeta({ ...userMeta, followers: e.target.value })
          }
          error={fieldErrors.followers}
        />

        <FormField
          label="Following Count"
          type="number"
          min="0"
          placeholder="0"
          value={userMeta.following}
          onChange={(e) =>
            setUserMeta({ ...userMeta, following: e.target.value })
          }
          error={fieldErrors.following}
        />

        <FormField
          label="Tweet Count"
          type="number"
          min="0"
          placeholder="0"
          value={userMeta.tweets}
          onChange={(e) =>
            setUserMeta({ ...userMeta, tweets: e.target.value })
          }
          error={fieldErrors.tweets}
        />

        <FormField
          label="Account Age (days)"
          type="number"
          min="0"
          placeholder="0"
          value={userMeta.accountAge}
          onChange={(e) =>
            setUserMeta({ ...userMeta, accountAge: e.target.value })
          }
          hint="Leave empty to use the creation date if available."
          error={fieldErrors.accountAge}
        />
      </section>

      <Button onClick={handleAnalyze} disabled={loading || !comment.trim()}>
        {loading ? "Analyzing..." : "Analyze User"}
      </Button>

      {loading && <p>Processing request, please wait...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {result && (
        <div className="result-box">
          <p>
            <strong>Toxicity:</strong> {result.toxicityLabel} (
            {(result.toxicityConfidence * 100).toFixed(2)}%)
          </p>
          <p className="result-note">{toRiskLabel(result.toxicityRisk)} toxicity signal.</p>

          <p>
            <strong>Bot Detection:</strong> {result.botLabel} (
            {(result.botConfidence * 100).toFixed(2)}%)
          </p>
          <p className="result-note">{toRiskLabel(result.botRisk)} bot signal.</p>

          <p>
            <strong>Final Risk:</strong>{" "}
            <span
              className={
                result.finalRisk === "High Risk"
                  ? "high-risk"
                  : result.finalRisk === "Medium Risk"
                  ? "medium-risk"
                  : "low-risk"
              }
            >
              {result.finalRisk}
            </span>
          </p>
          <p className="result-score">
            Combined score: {(result.finalRiskScore * 100).toFixed(1)}%
          </p>
          {result.summary && <p>{result.summary}</p>}
          {result.recommendation && <p><strong>Recommendation:</strong> {result.recommendation}</p>}
        </div>
      )}
    </div>
  );
}

export default CombinedAnalysis;
