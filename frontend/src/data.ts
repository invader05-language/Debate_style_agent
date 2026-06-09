import { ActivityItem, ModelStatus, HistoryItem, MemoryInsight } from "./types";

export const INITIAL_ACTIVITIES: ActivityItem[] = [
  {
    id: "act-1",
    title: "The Ethicality of Synthetic Data",
    type: "Debate",
    agentsCount: 12,
    timeAgo: "14m ago",
    status: "Completed"
  },
  {
    id: "act-2",
    title: "Optimization Logic for Mars Habitation",
    type: "Think",
    agentName: "Claude 3.5 Sonnet",
    timeAgo: "2h ago",
    status: "In Progress"
  },
  {
    id: "act-3",
    title: "Refactoring Legacy ERP Cluster",
    type: "Think",
    agentName: "GPT-4o",
    timeAgo: "5h ago",
    status: "Failed"
  }
];

export const INITIAL_MODELS: ModelStatus[] = [
  {
    id: "mimo-4",
    name: "MIMO-4 Turbo",
    provider: "AuraLabs",
    contextWindow: "128k Tokens",
    apiFormat: "REST / JSON",
    status: "Healthy",
    toggle: true,
    latency: "124ms"
  },
  {
    id: "deepseek-coder",
    name: "DeepSeek Coder",
    provider: "DeepSeek AI",
    contextWindow: "32k Tokens",
    apiFormat: "OpenAI Schema",
    status: "Healthy",
    toggle: true,
    latency: "192ms"
  },
  {
    id: "llama-3-70b",
    name: "Llama 3 70B",
    provider: "Meta AI",
    contextWindow: "8k Tokens",
    apiFormat: "vLLM / gRPC",
    status: "Inactive",
    toggle: false,
    latency: "N/A"
  },
  {
    id: "claude-35-sonnet",
    name: "Claude 3.5 Sonnet",
    provider: "Anthropic",
    contextWindow: "200k Tokens",
    apiFormat: "Anthropic SDK",
    status: "Healthy",
    toggle: true,
    latency: "145ms"
  }
];

export const INITIAL_HISTORY: HistoryItem[] = [
  {
    id: "hist-1",
    title: "User Login Scheme Design",
    type: "DEBATE",
    status: "COMPLETED",
    description: "Security architecture analysis for a multi-tenant enterprise portal.",
    agents: ["Aura-Omega", "Cyber-Critic"],
    timestamp: "Oct 24, 2023 • 14:30"
  },
  {
    id: "hist-2",
    title: "Cloud Latency Optimization Strategy",
    type: "THINK",
    status: "IN PROGRESS",
    description: "Deep reasoning task evaluating edge-node distributions across APAC regions.",
    agents: ["Solon-7 Reasoning Engine"],
    timestamp: "Started 4m ago"
  },
  {
    id: "hist-3",
    title: "Q4 Market Sentiment Consensus",
    type: "SYNTHESIS",
    status: "COMPLETED",
    description: "Unified report generated from 12 distinct AI analyst perspectives.",
    agents: ["Multi-Agent Swarm"],
    timestamp: "Oct 23, 2023 • 09:15"
  }
];

export const INITIAL_MEMORIES: MemoryInsight[] = [
  {
    id: "mem-1",
    title: "JWT vs Session Auth",
    sourceType: "DEBATE",
    date: "Oct 24, 2023 • 14:20 GMT",
    confidence: 98,
    lessons: [
      "Use JWT for stateless scalability in distributed microservices.",
      "Prefer Sessions for monolithic apps to simplify revocation logic.",
      "Always implement Refresh Token rotation to mitigate CSRF risks."
    ],
    tags: ["Auth", "Security"]
  },
  {
    id: "mem-2",
    title: "Optimizing Vector Queries",
    sourceType: "THINK",
    date: "Oct 23, 2023 • 09:12 GMT",
    confidence: 84,
    lessons: [
      "HNSW indexing provides the best balance of recall and latency.",
      "Normalize embeddings to unit length for faster cosine similarity.",
      "Batch updates to reduce re-indexing overhead during high load."
    ],
    tags: ["AI", "Search"]
  },
  {
    id: "mem-3",
    title: "Zero-Knowledge Architecture",
    sourceType: "SYNTHESIS",
    date: "Oct 22, 2023 • 18:45 GMT",
    confidence: 92,
    lessons: [
      "Client-side encryption using SubtleCrypto API.",
      "Secret sharing using Shamir's algorithm for recovery.",
      "ZK-Proofs for authentication without data disclosure.",
      "Deterministic key derivation from master passwords."
    ],
    tags: ["Cryptography", "Privacy", "Web3"],
    imageUrl: "https://lh3.googleusercontent.com/aida/AP1WRLtObHhZ9HjQ02-dfCEVQQLVkYp2xnFsb5EcV_AlPE-w-USHT2dpeCgeiDtdTGqUvHgy6YMx4UQta-byP3ATVcmVMpZPKo0r0cWFi78iwWlupGAFQPVDZIC48yeVZ4FeOPSRacO1v3lEQO7PNtXZjzOG2j3Qo5MxnLDiNBIIMae40CkrRqGWgN-6aKuiVPM5QxfphgTdikYr6QSI3N1lLNvS1nreWbtaaIbE2Klr3umhicD9zy-rnPjbEr01"
  },
  {
    id: "mem-4",
    title: "Tailwind vs CSS Modules",
    sourceType: "DEBATE",
    date: "Oct 21, 2023 • 11:05 GMT",
    confidence: 76,
    lessons: [
      "Tailwind wins for rapid prototyping and consistent design tokens.",
      "CSS Modules offer better isolation for legacy code integration."
    ],
    tags: ["Frontend", "Styling"]
  }
];

export const FAQS = [
  {
    question: "How do I switch between different LLM models?",
    answer: "You can switch models in the 'Workspace' sidebar or through the 'Model Configuration' settings. AuraSynth supports seamless switching between GPT-4, Claude 3.5, and Gemini Pro during an active session. Note that switching models may impact your session token count."
  },
  {
    question: "Can multiple agents debate on the same topic simultaneously?",
    answer: "Yes, that is a core feature of the AuraSynth platform. By entering 'Debate Mode', you can assign different personas or model providers to opposing sides of an argument. Our orchestration layer ensures coherent turns and logical progression."
  },
  {
    question: "Is my data used to train the underlying models?",
    answer: "No. By default, AuraSynth uses Enterprise-grade APIs that do not utilize customer data for training purposes. Your session history is encrypted and only accessible by your account."
  },
  {
    question: "How do I reset my API secret key?",
    answer: "Go to Settings > Developer > API Management. Click 'Revoke' on your existing key and generate a new one. Remember to update your integration scripts immediately as the old key will cease to function instantly."
  }
];

export const DEBATE_TOPICS = [
  "e.g. The ethical implications of AGI in healthcare",
  "Is open-source AI safer than closed-source proprietary models?",
  "Should autonomous AI agents hold property and digital assets?",
  "The tradeoff between parameter scaling and architectural efficiency",
  "Coping with hallucination rates in legally-binding contract generators"
];

export const PRO_COMPONENTS = [
  "Aura-Omega (Logic-Centric)",
  "GPT-4o (Empirical Analyst)",
  "Claude 3.5 Sonnet (Nuanced Philosopher)",
  "Llama 3 70B (High-Volume Synthesizer)"
];

export const CON_COMPONENTS = [
  "Cyber-Critic (Adversarial)",
  "DeepSeek-R1 (Frugal Realist)",
  "Gemini 3.5 Flash (Swift Debunker)",
  "Judge-GPT (Synthesis-Driven)"
];

export const NEUTRAL_ARBITERS = [
  "Judge-GPT (Synthesis)",
  "AuraSynth-Omega (Platform Neutral)",
  "Human Observer (Active Intervention)"
];
