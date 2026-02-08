import { useState } from "react";
import api from "../api/api";

export default function DeepfakeImage() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const submit = async () => {
    if (!file) return;
    setLoading(true);

    const formData = new FormData()
    formData.append("file", file) // 🔴 MUST be "file"

    await api.post("/fraud/audio", formData, {
      headers: { "Content-Type": "multipart/form-data" }
    })


    const res = await api.post("/api/deepfake/image", formData);
    setResult(res.data);
    setLoading(false);
  };

  return (
    <div className="card">
      <h2>🖼️ Deepfake Image Detection</h2>
      <input type="file" accept="image/*" onChange={e => setFile(e.target.files[0])} />
      <button onClick={submit}>Analyze</button>

      {loading && <p>Analyzing...</p>}

      {result && (
        <p>
          Result: <b>{result.deepfake ? "DEEPFAKE" : "REAL"}</b><br/>
          Confidence: {(result.confidence * 100).toFixed(2)}%
        </p>
      )}
    </div>
  );
}
