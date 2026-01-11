export default function PrimaryButton({ children, variant = "solid", ...props }) {
  const cls = variant === "ghost" ? "btn btnGhost" : "btn";
  return (
    <button className={cls} {...props}>
      {children}
    </button>
  );
}
