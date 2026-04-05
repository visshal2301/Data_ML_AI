

Here's a comprehensive overview of the key LangChain topics you need to know:Here's a breakdown of the key topic areas:

**Foundation (top row)** — LLMs/Chat Models, Prompt Templates, and Output Parsers are the three primitives everything else builds on.

**LCEL (LangChain Expression Language)** — the modern way to compose everything. The `|` pipe operator chains runnables together declaratively. This replaces older chain classes.

**Chains** — pre-built pipelines for common patterns (QA, summarization, sequential tasks). Retrieval Chains specifically power RAG (retrieval-augmented generation).

**RAG components** — the four building blocks for RAG: loaders (ingest data), splitters (chunk it), embeddings (vectorize it), and vector stores (index and search it).

**Memory** — gives chains conversational context across turns. Buffer, summary, and windowed are the main variants.

**Agents + Tools** — agents dynamically choose which tools to call at runtime. Tools can be search engines, Python REPLs, APIs, or anything custom.

**LangGraph** — the newer, more powerful framework for building stateful, multi-step agents with cycles and branching logic. Essential for complex agentic workflows.

**LangSmith** — the observability layer for logging, debugging, and evaluating your chains and agents.

Click any box in the diagram to go deeper on any topic!