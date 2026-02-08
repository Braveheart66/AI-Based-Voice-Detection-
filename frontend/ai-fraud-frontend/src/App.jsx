import DeepfakeImage from "./components/DeepfakeImage";
import DeepfakeVideo from "./components/DeepfakeVideo";
import FraudAudio from "./components/FraudAudio";

export default function App() {
  return (
    <div className="container">
      <h1>🔍 AI Fraud & Deepfake Detection</h1>
      <DeepfakeImage />
      <DeepfakeVideo />
      <FraudAudio />
    </div>
  );
}
