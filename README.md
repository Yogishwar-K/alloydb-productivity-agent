# alloydb-productivity-agent

# Multi-Agent Productivity Assistant (AlloyDB + ADK)

A high-performance, context-aware productivity assistant built for the Google GenAI APAC Labs Hackathon. This system treats intelligence as a first-class citizen of the data layer by leveraging **In-Database AI** with AlloyDB.

## The Vision
Traditional productivity apps rely on rigid keyword searches. This assistant uses **Semantic Discovery** to understand the *intent* and *context* of a user's workload, allowing for smarter task recommendations and streamlined data ingestion.

## Tech Stack & Google Cloud Integration
* **Google ADK (Agent Development Kit):** Orchestrates the `root_agent` and manages the seamless interaction between user prompts and backend tools.
* **AlloyDB AI:** Our enterprise-grade PostgreSQL-compatible database.
* **Gemini 3.1 Pro Preview:** Powers the core reasoning and orchestration within the ADK agent.
* **In-Database Intelligence:**
    * `embedding('text-embedding-005', ...)`: Generates and stores vector embeddings directly within SQL `INSERT` statements.
    * `ai.if()`: Performs real-time logic-based "vibe checks" inside the database engine to filter tasks based on contextual relevance.
* **pgvector:** Enables ultra-fast vector similarity searches ($L2$ distance) to surface the most relevant tasks.

## Core Features
1. **Smart Ingestion:** Users add tasks in natural language (e.g., "Remind me to review the firewall logs tomorrow"). The system automatically vectorizes and categorizes the intent.
2. **Semantic Retrieval:** Users can query based on goals (e.g., "What should I work on if I have 15 minutes?"). The system matches the "vibe" of the task to the user's current situation using vector proximity.

## Installation & Execution
1. **Clone & Install:**
   ```bash
   git clone [your-repo-link]
   cd productivity_agent
   pip install -r requirements.txt
## Environment Setup:
Configure your .env with your AlloyDB Public/Private IP and credentials.

## Launch:
```bash
adk web
