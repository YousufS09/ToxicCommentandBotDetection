function Input({ className = "", ...props }) {
  const classes = ["atomic-input", className].filter(Boolean).join(" ");

  return <input className={classes} {...props} />;
}

export default Input;
