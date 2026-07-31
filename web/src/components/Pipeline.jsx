const STEPS = ["Search", "Extract", "Synthesize", "Fact-check"];

const STEP_KEYS = ["search", "extract", "synthesis", "fact_check"];

function stepState(currentStep, status, index) {
  if (status === "completed") return "done";
  if (status !== "running") return "";
  const activeIdx = STEP_KEYS.indexOf(currentStep);
  if (index < activeIdx) return "done";
  if (index === activeIdx) return "active";
  return "";
}

export default function Pipeline({ step, status }) {
  return (
    <div className="pipeline">
      {STEPS.map((label, i) => {
        const state = stepState(step, status, i);
        return (
          <div key={label} style={{ display: "contents" }}>
            <div className={`pipeline__step pipeline__step--${state}`}>
              <div className="pipeline__circle">
                {state === "done" ? "✓" : i + 1}
              </div>
              <span className="pipeline__label">{label}</span>
            </div>
            {i < STEPS.length - 1 && (
              <div
                className={`pipeline__connector ${
                  stepState(step, status, i) === "done"
                    ? "pipeline__connector--done"
                    : ""
                }`}
              />
            )}
          </div>
        );
      })}
    </div>
  );
}
