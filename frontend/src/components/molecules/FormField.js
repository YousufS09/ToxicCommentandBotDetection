import Input from "../atoms/Input";
import TextArea from "../atoms/TextArea";

function FormField({
  label,
  as = "input",
  className = "",
  labelClassName = "",
  hint,
  error,
  ...props
}) {
  const Control = as === "textarea" ? TextArea : Input;

  return (
    <label className={["form-field", className].filter(Boolean).join(" ")}>
      {label && (
        <span className={["form-field__label", labelClassName].filter(Boolean).join(" ")}>
          {label}
        </span>
      )}
      <Control {...props} />
      {hint && <small className="form-field__hint">{hint}</small>}
      {error && <small className="form-field__error">{error}</small>}
    </label>
  );
}

export default FormField;
