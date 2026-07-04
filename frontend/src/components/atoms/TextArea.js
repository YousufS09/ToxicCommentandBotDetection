function TextArea({ className = "", ...props }) {
  const classes = ["atomic-textarea", className].filter(Boolean).join(" ");

  return <textarea className={classes} {...props} />;
}

export default TextArea;
