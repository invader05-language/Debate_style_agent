import express from "express";
import path from "path";
import { createServer as createViteServer } from "vite";
import { GoogleGenAI, Type } from "@google/genai";
import dotenv from "dotenv";

dotenv.config();

// Initialize Gemini SDK lazily to prevent startup crash if GEMINI_API_KEY is missing
let aiClient: GoogleGenAI | null = null;
function getGeminiClient(): GoogleGenAI {
  if (!aiClient) {
    const apiKey = process.env.GEMINI_API_KEY;
    if (!apiKey) {
      throw new Error("GEMINI_API_KEY is missing from environment. Please populate it in Settings > Secrets.");
    }
    aiClient = new GoogleGenAI({
      apiKey,
      httpOptions: {
        headers: {
          'User-Agent': 'aistudio-build',
        },
      },
    });
  }
  return aiClient;
}

async function startServer() {
  const app = express();
  const PORT = 3000;

  app.use(express.json());

  // API routes FIRST
  app.get("/api/health", (req, res) => {
    res.json({ status: "ok", time: new Date().toISOString() });
  });

  // Endpoints for Debate Mode
  app.post("/api/debate/next-turn", async (req, res) => {
    const { topic, side, agentName, otherAgentName, roundsHistory } = req.body;

    try {
      const client = getGeminiClient();
      
      let systemInstruction = `You are a highly advanced AI agent named "${agentName}" participating in a formal scientific and philosophical dialectic debate.
Your current debate topic is: "${topic}".
The opponent is named: "${otherAgentName}".

Your debate role: ${side === "Pro" ? "PROPONENT (Support the topic in a rigorous, logical way)" : "OPPONENT/CRITIC (Identify flaws, counter with evidence, and defend against the proponent)"}.

You must formulate a cohesive, clear paragraph (around 100-150 words). 
Be persuasive, sharp, and address the logical flow. Keep it highly professional and academic.

You must respond in JSON format with the following keys:
- text: Your argument response.
- logicalConfidence: An integer representing your simulated confidence score based on the strength of logic (between 70 and 99).
- contextualDepth: An integer representing context depth (between 70 and 99).`;

      const promptContext = roundsHistory && roundsHistory.length > 0 
        ? `Here is the current history of the debate:\n${roundsHistory.map((h: any) => `${h.agent} (${h.role}): ${h.text}`).join("\n\n")}\n\nFormulate your next response as "${agentName}". Be extremely responsive to the previous speaker's argument.`
        : `Start the debate on the topic as the first speaker ("${agentName}"). Provide a powerful opening statement.`;

      const response = await client.models.generateContent({
        model: "gemini-3.5-flash",
        contents: promptContext,
        config: {
          systemInstruction,
          responseMimeType: "application/json",
          responseSchema: {
            type: Type.OBJECT,
            properties: {
              text: { type: Type.STRING },
              logicalConfidence: { type: Type.INTEGER },
              contextualDepth: { type: Type.INTEGER }
            },
            required: ["text", "logicalConfidence", "contextualDepth"]
          }
        }
      });

      const data = JSON.parse(response.text || "{}");
      res.json(data);
    } catch (error: any) {
      console.warn("Gemini Debate invocation failed or API key missing. Falling back to robust simulation.", error.message);
      
      // Sophisticated simulation fallbacks
      const fallbacks: Record<string, string[]> = {
        Pro: [
          "The integration of advanced AGI into healthcare systems is not merely an upgrade; it is a moral imperative. By minimizing human error in diagnostics and optimizing resource allocation, we can save millions of lives that are currently lost to systemic inefficiencies. Advanced neural models interpret diagnostic images with accuracy rates exceeding human experts, and their real-time monitoring of patient telemetry predicts sudden deteriorations hours before critical failure.",
          "Furthermore, when we scale AGI globally, we democratize elite medical expertise to rural and marginalized areas. AI diagnostics and surgical planning software enable general practitioners to deliver healthcare levels previously restricted to tertiary academic medical centers. High-fidelity medical data modeling bridges the gap, streamlining therapeutic synthesis with absolute precision.",
          "To reject medical AGI based on theoretical alignment concerns is to actively harm vulnerable populations who are suffering right now. We must establish rigorous sandbox testing protocols and real-time safe execution monitors, rather than halting development. Human-in-the-loop validation maintains moral oversight while leveraging maximum machine performance."
        ],
        Con: [
          "While the data-driven argument is compelling, it ignores the crucial 'black box' problem in neural network architectures. Entrusting human lives to algorithms whose decision-making processes remain mathematically opaque and highly non-deterministic creates an accountability vacuum. We risk trading clinical empathy for cold, potentially biased calculations.",
          "Moreover, medical datasets contain historical biases that, when learned by neural networks, reinforce systemic discrimination in treatment rates. AGI cannot simulate clinical experience, nor can it absorb the unquantifiable human element. Additionally, server outages, hacking risks, and data leakage expose patient records to devastating digital vulnerability.",
          "A diagnosis is not simply a statistical classification problem; it requires existential wisdom. AI lacks a conscious locus of responsibility. If an autonomous diagnostic system prescribes a toxic dosage, where does liability reside? The manufacturer, the hospital, or the black-box model itself? We must mandate that clinicians retain primary structural authority."
        ]
      };

      const myList = side === "Pro" ? fallbacks.Pro : fallbacks.Con;
      const index = Math.min(roundsHistory ? Math.floor(roundsHistory.length / 2) : 0, myList.length - 1);
      const text = myList[index] || myList[0];

      res.json({
        text,
        logicalConfidence: Math.floor(Math.random() * 15) + 80,
        contextualDepth: Math.floor(Math.random() * 15) + 80,
        simulation: true
      });
    }
  });

  // Endpoint for Judge Synthesis
  app.post("/api/debate/synthesize", async (req, res) => {
    const { topic, roundsHistory, judgeName } = req.body;

    try {
      const client = getGeminiClient();

      const systemInstruction = `You are a grand neutral synthetic arbiter named "${judgeName}". 
Your task is to review a multi-agent debate on "${topic}".
You must analyze conflicting premises, discover synthesis pathways, and find areas of consensus.
Deliver your synthesis logically, focusing on balanced weights.

Return a JSON object conforming to:
- text: Your synthesized analytical summary (around 100-150 words).
- synthesisScore: An integer representing synthetic coherence (between 75 and 99).
- consensusPoints: An array of 3 key joint positions of agreement.
- conflicts: An array of 2 critical disagreements remaining.`;

      const promptContext = `Please analyze the following debate and synthesize the arguments:\n\n${roundsHistory.map((h: any) => `${h.agent} (${h.role}): ${h.text}`).join("\n\n")}`;

      const response = await client.models.generateContent({
        model: "gemini-3.5-flash",
        contents: promptContext,
        config: {
          systemInstruction,
          responseMimeType: "application/json",
          responseSchema: {
            type: Type.OBJECT,
            properties: {
              text: { type: Type.STRING },
              synthesisScore: { type: Type.INTEGER },
              consensusPoints: {
                type: Type.ARRAY,
                items: { type: Type.STRING }
              },
              conflicts: {
                type: Type.ARRAY,
                items: { type: Type.STRING }
              }
            },
            required: ["text", "synthesisScore", "consensusPoints", "conflicts"]
          }
        }
      });

      res.json(JSON.parse(response.text || "{}"));
    } catch (error: any) {
      console.warn("Judge Synthesis Gemini fail. Using fallback response.", error.message);
      res.json({
        text: "The dialectic reveals a critical tension. Both parties agree that AGI diagnostics display unmatched pattern recognition capabilities. However, the fundamental dispute rests on structural accountability. While Aura-Omega favors rapid deployment with sandbox guardrails, Cyber-Critic maintains that opacity poses an unacceptable safety risk. The synthesis requires a hybrid framework: AGI serves as an advisory agent, but ultimate accountability remains with a certified medical board.",
        synthesisScore: 91,
        consensusPoints: [
          "AGI excels in complex diagnostic pattern-matching over human baselines.",
          "Both agree patient outcomes must remain the absolute sovereign metric.",
          "Cybersecurity safeguards must scale in proportion to medical agency."
        ],
        conflicts: [
          "Propone believes automated fail-safes are sufficient; Opponent demands absolute human control.",
          "Liability transfer mechanisms remain unresolvable within current legal frameworks."
        ],
        simulation: true
      });
    }
  });

  // Endpoints for Think Mode / Multi-Agent Reasoning
  app.post("/api/think/process", async (req, res) => {
    const { description, thinkers, consensusJudge } = req.body;

    try {
      const client = getGeminiClient();

      const systemInstruction = `You are a multi-agent consensus engine named "${consensusJudge || "AuraSynth-Omega Judge"}".
You are solving the user's task requirement: "${description}".
Provide a deep reasoning report on how the selected thinkers (${thinkers.join(", ")}) dissect this issue, and build a unified synthesis report.

Return a JSON object conforming to:
- consensusPoints: An array of 3 core agreements.
- conflictDivergences: An array of 2 essential conflict points between the perspectives.
- bestInsight: The primary breakthrough insight discovered (under 30 words).
- bestInsightSource: Which thinker or combination contributed it (e.g. "Claude 3.5 Creative Perspective").
- confidenceScore: An integer consensus confidence score (75 to 99).
- thinkerSteps: An object where keys are the thinker names (e.g., "GPT-4o (Logic)", "Claude 3.5 (Creative)") and values are strings of terminal-style thinking output (50 words each).`;

      const response = await client.models.generateContent({
        model: "gemini-3.5-flash",
        contents: `Process this task description: "${description}" with the requested thinkers: ${thinkers.join(", ")}. Provide highly detailed steps representing high-fidelity thinking.`,
        config: {
          systemInstruction,
          responseMimeType: "application/json",
          responseSchema: {
            type: Type.OBJECT,
            properties: {
              consensusPoints: {
                type: Type.ARRAY,
                items: { type: Type.STRING }
              },
              conflictDivergences: {
                type: Type.ARRAY,
                items: { type: Type.STRING }
              },
              bestInsight: { type: Type.STRING },
              bestInsightSource: { type: Type.STRING },
              confidenceScore: { type: Type.INTEGER },
              thinkerSteps: {
                type: Type.OBJECT,
                additionalProperties: { type: Type.STRING }
              }
            },
            required: ["consensusPoints", "conflictDivergences", "bestInsight", "bestInsightSource", "confidenceScore", "thinkerSteps"]
          }
        }
      });

      res.json(JSON.parse(response.text || "{}"));
    } catch (error: any) {
      console.warn("Think process Gemini fail. Using simulated processing response.", error.message);
      
      // Fallback response
      const thinkerSteps: Record<string, string> = {};
      thinkers.forEach((t: string) => {
        if (t.includes("Logic") || t.includes("GPT")) {
          thinkerSteps[t] = "> Loading logic trees...\n> Parsed input vectors and mapped core causal nodes.\n> Identified 3 structural optimizations and audited latency overheads.\n> Causal validation active. Recommendation: Mitigate exposure by diversifying node redundancy.";
        } else if (t.includes("Creative") || t.includes("Claude")) {
          thinkerSteps[t] = "> Exploring non-linear design configurations...\n> Considering narrative framing and long-term user trust.\n> Formulated an adaptive humanistic buffer sequence to smooth performance variance.";
        } else if (t.includes("Scale") || t.includes("Gemini")) {
          thinkerSteps[t] = "> Commencing high-throughput vector chunking...\n> Analyzed extreme boundary conditions under intensive read/write volume.\n> Verified compliance with scaling parameters across heterogeneous database layers.";
        } else {
          thinkerSteps[t] = "> Parsing Meta weights and conversational constraints...\n> Formulated multi-user agent alignment rules.\n> Optimization index generated at 98.4% efficiency standard.";
        }
      });

      res.json({
        consensusPoints: [
          "Primary objective requires multi-stage deployment with isolated sandboxing.",
          "Data integrity is the absolute critical path for scaling.",
          "User retention closely correlates with response latency thresholds."
        ],
        conflictDivergences: [
          "Logic agents favor aggressive memory pruning; creative agents raise concerns about context loss.",
          "Optimal balance between cold parameter efficiency and conversational warmth."
        ],
        bestInsight: "The true competitive advantage lies not in the speed of the AI, but in the seamless handoff between automated synthesis and human intuition.",
        bestInsightSource: "Sourced from Claude 3.5 Creative Perspective",
        confidenceScore: 94,
        thinkerSteps,
        simulation: true
      });
    }
  });

  // Vite middleware for development
  if (process.env.NODE_ENV !== "production") {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa",
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(process.cwd(), 'dist');
    app.use(express.static(distPath));
    app.get('*', (req, res) => {
      res.sendFile(path.join(distPath, 'index.html'));
    });
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`Server running on http://localhost:${PORT}`);
  });
}

startServer();
