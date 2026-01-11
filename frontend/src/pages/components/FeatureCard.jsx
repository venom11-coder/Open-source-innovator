export default function FeatureCard({ title, text }) {
  return (
    <div className="featureCard">
      <div className="featureTitle">{title}</div>
      <div className="featureText">{text}</div>
    </div>
  );
}
