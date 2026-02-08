import { useState } from "react";
import api from "../api/api";

export default function DeepfakeVideo() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const submit = async () => {
    const formData = new FormData();
    formData.append("file", file);

    const res = await api.post("/api/deepfake/video", formData);
    setResult(res.data);
  };

  return (
    <div className="card">
      <h2>🎥 Deepfake Video Detection</h2>
      <input type="file" accept="video/*" onChange={e => setFile(e.target.files[0])} />
      <button onClick={submit}>Analyze</button>

      {result && (
        <p>
          Result: <b>{result.deepfake ? "DEEPFAKE" : "REAL"}</b><br/>
          Confidence: {(result.confidence * 100).toFixed(2)}%
        </p>
      )}
    </div>
  );
}
