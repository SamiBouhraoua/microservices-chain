import express from "express";
import bodyParser from "body-parser";
import fetch from "node-fetch"; // ✅ AJOUT

const app = express();
app.use(bodyParser.json());

app.post("/stepA", async (req, res) => {
  try {
    let { message, trace } = req.body;

    const transformed = message.toUpperCase();

    trace.push({
      service: "service-a",
      language: "JavaScript",
      info: { uppercased: true },
      timestamp: Date.now()
    });

    const response = await fetch("http://127.0.0.1:9002/stepB", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: transformed, trace })
    });

    if (!response.ok) {
      return res.status(502).json({ error: "Bad Gateway from B" });
    }

    const result = await response.json();
    res.json(result);
  } catch (err) {
    res.status(502).json({ error: err.message });
  }
});

app.get("/ping", (req, res) => res.json({ status: "A up" }));
app.listen(9001, () => console.log("Service A running on port 9001"));
