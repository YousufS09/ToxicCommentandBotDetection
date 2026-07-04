function Button({ className = "", variant = "primary", children, ...props }) {
  const classes = ["atomic-button", `atomic-button--${variant}`, className]
    .filter(Boolean)
    .join(" ");

  return (
    <button className={classes} {...props}>
      {children}
    </button>
  );
}

export default Button;
