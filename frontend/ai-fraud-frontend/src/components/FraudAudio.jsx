import { useState } from "react";
import api from "../api/api";

export default function FraudAudio() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const submit = async () => {
    const formData = new FormData();
    formData.append("file", file); // MUST be "file"

    const res = await api.post("/fraud/audio", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    setResult(res.data);
  };

  return (
    <div className="card">
      <h2>📞 Fraud Call Detection</h2>
      <input type="file" accept="audio/*" onChange={e => setFile(e.target.files[0])} />
      <button onClick={submit}>Analyze</button>

      {result && (
        <p>
          Result: <b>{result.result.toUpperCase()}</b><br/>
          Confidence: {(result.confidence * 100).toFixed(2)}%<br/>
          Source: {result.source}
        </p>
      )}
    </div>
  );
}
