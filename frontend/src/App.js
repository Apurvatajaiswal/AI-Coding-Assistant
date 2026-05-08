import React, { useState } from "react";
import "./App.css";
import { motion } from "framer-motion";

<motion.h1
  initial={{ opacity: 0, y: 50 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.8 }}
>
   AI Coding Assistant
</motion.h1>

function App() {
  const [result, setResult] = useState("");

  // Voice
  const speak = (text) => {
    const utterance = new SpeechSynthesisUtterance(text);
    window.speechSynthesis.speak(utterance);
  };
  

  // Send to backend
  const sendToBackend = async (image) => {
    try {
      const res = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ image }),
      });

      const data = await res.json();
      setResult(data.result);
      speak(data.result);

    } catch (err) {
      console.error(err);
      setResult("Error connecting to backend");
    }
  };

  //Screen capture
  const scanScreen = async () => {
    try {
      const stream = await navigator.mediaDevices.getDisplayMedia({
        video: true,
      });

      const video = document.createElement("video");
      video.srcObject = stream;

      await video.play();

      await new Promise((resolve) => {
        video.onloadedmetadata = resolve;
      });

      const canvas = document.createElement("canvas");
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;

      const ctx = canvas.getContext("2d");
      ctx.drawImage(video, 0, 0);

      const image = canvas.toDataURL("image/png");

      // stop screen share
      stream.getTracks().forEach((track) => track.stop());

      sendToBackend(image);

    } catch (err) {
      console.error(err);
      setResult("Screen capture failed");
    }
  };

  //Voice command
  const startListening = () => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert("Speech Recognition not supported");
      return;
    }

    const recognition = new SpeechRecognition();

    recognition.onresult = (event) => {
      const command = event.results[0][0].transcript.toLowerCase();

      if (command.includes("scan")) {
        scanScreen();
      }
    };

    recognition.start();
  };

  return(
    <div className="container">
      <h1>AI Coding Assistant</h1>
      <p>Scan your screen and detect coding errors instantly</p>

      <div className="card">
        <h2>Scan & Analyze</h2>
        <button onClick={scanScreen}>Scan Screen</button>
        <button onClick={startListening}>Voice Command</button>

        <div className="result-box">
          {result || "Result will appear here..."}
        </div>
      </div>
    </div>
  );
}

export default App;
