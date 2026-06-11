import { ActivityItem, ModelStatus, HistoryItem, MemoryInsight } from "./types";

export const INITIAL_ACTIVITIES: ActivityItem[] = [];

export const INITIAL_MODELS: ModelStatus[] = [
  {
    id: "qwen35-397b",
    name: "Qwen3.5-397B",
    provider: "SiliconFlow",
    contextWindow: "120k Tokens",
    apiFormat: "OpenAI",
    status: "Healthy",
    toggle: true,
    latency: "~200ms"
  },
  {
    id: "qwen25-72b",
    name: "Qwen2.5-72B",
    provider: "SiliconFlow",
    contextWindow: "120k Tokens",
    apiFormat: "OpenAI",
    status: "Healthy",
    toggle: true,
    latency: "~150ms"
  },
  {
    id: "kimi-k26",
    name: "Kimi K2.6",
    provider: "SiliconFlow",
    contextWindow: "120k Tokens",
    apiFormat: "OpenAI",
    status: "Healthy",
    toggle: true,
    latency: "~180ms"
  },
  {
    id: "deepseek-v4-pro",
    name: "DeepSeek V4 Pro",
    provider: "SiliconFlow",
    contextWindow: "1M Tokens",
    apiFormat: "OpenAI",
    status: "Healthy",
    toggle: true,
    latency: "~250ms"
  },
];

export const INITIAL_HISTORY: HistoryItem[] = [];

export const INITIAL_MEMORIES: MemoryInsight[] = [];

export const FAQS = [
  {
    question: "How do I switch between different LLM models?",
    answer: "Go to Model Management. All models are available through SiliconFlow (硅基流动) platform."
  },
  {
    question: "Can multiple agents debate on the same topic simultaneously?",
    answer: "Yes. In Debate Mode, assign different models (e.g. Qwen vs Kimi) to opposing sides."
  },
  {
    question: "Is my data used to train the underlying models?",
    answer: "No. AuraSynth uses enterprise-grade APIs that do not use customer data for training."
  },
  {
    question: "What is SiliconFlow (硅基流动)?",
    answer: "SiliconFlow is a unified AI model platform providing access to Qwen, Kimi, DeepSeek and more through a single API."
  },
];

export const DEBATE_TOPICS = [
  "e.g. The ethical implications of AGI in healthcare",
  "Is open-source AI safer than closed-source proprietary models?",
  "Should autonomous AI agents hold property and digital assets?",
  "The tradeoff between parameter scaling and architectural efficiency",
  "Coping with hallucination rates in legally-binding contract generators"
];

export const PRO_COMPONENTS = [
  "Qwen3.5-397B",
  "Qwen2.5-72B",
  "Kimi K2.6",
  "DeepSeek V4 Pro",
];

export const CON_COMPONENTS = [
  "DeepSeek V4 Pro",
  "Qwen3.5-397B",
  "Kimi K2.6",
  "Qwen2.5-72B",
];

export const NEUTRAL_ARBITERS = [
  "Qwen3.5-397B",
  "Kimi K2.6",
  "DeepSeek V4 Pro",
  "Human Observer (Active Intervention)"
];
