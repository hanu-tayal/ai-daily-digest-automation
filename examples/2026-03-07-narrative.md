# This Week in AI: A Narrative for Product Leaders

*March 7, 2026 — Synthesized from Lenny's, a16z, AI Collective, AI x Product, and Marily's newsletters*

---

## The Big Picture

This week, three threads converge: how to scale AI adoption inside large organizations, how to build agentic systems that actually work, and how to sell without a sales team. Underneath it all is a deeper question: when everyone can execute fast, what's your edge?

---

## Part One: Adoption at Scale

Chintan Turakhia is Senior Director of Engineering at Coinbase. He led a thousand-plus engineers through a rewrite of their self-custody wallet into a consumer social app—in six to nine months. The only way that was possible was AI as a force multiplier.

The numbers are stark: PR review time dropped from 150 hours to 15 hours. The cycle from user feedback to shipped features compressed dramatically. How did they do it?

First, leadership had to go hands-on. Chintan didn't delegate AI adoption to a committee. He used the tools himself. That conviction trickled down.

Second, they ran a "PR speed run": 100 engineers, 70 PRs in 15 minutes. It was a forcing function. Everyone had to try. The result wasn't just efficiency—it was proof that the system could work at scale.

Third, they used Cursor to analyze adoption patterns. Who were the power users? What did they do differently? They identified those behaviors and replicated them. The metrics that mattered: PR velocity, cycle time, and power-user identification.

The takeaway: if you're leading engineering or product, you can't outsource AI adoption. You have to be in the weeds. And you have to measure what actually moves.

---

## Part Two: The Architecture of Agency

The era of the chatbot is ending. We're moving from systems that talk to systems that do. For product managers, that's thrilling—and chaotic. We're no longer managing text generation. We're managing behavior.

How do you stop an agent from hallucinating in an infinite loop? How do you ensure it remembers a user's preference from three weeks ago? How do you make it fail gracefully when an API goes down?

The answer is design patterns. Not theory—blueprints. The same way software engineering has MVC and Singleton, agentic AI has its own scaffolding.

Start with routing. Stop trying to make one prompt do everything. Build a traffic controller that sends users to the right specialized workflow. If someone says "I want a refund," route them to finance, not tech support. That alone saves time and reduces risk.

Add reflection. Ask the model to check its own work before the user sees it. It adds latency, but it drastically increases trust. A draft that goes through a critique loop is better than a quick, sloppy response.

Then memory. Short-term for the conversation. Long-term for RAG—facts stored in a vector database, recalled weeks later. An agent without memory is just a fancy search engine.

Add self-healing: when an API fails, retry, or switch to a backup. Add human-in-the-loop for high-stakes domains: the agent drafts, the human approves.

And resource-aware routing: use cheap models for scanning, expensive models only for the hard parts. A legal doc analyzer doesn't need GPT-4 to read page numbers.

The maturity curve: Level one, routing. Level two, reflection. Level three, memory. Level four, multi-agent orchestration. Don't try to build a swarm on day one. Agency is an architecture, not a feature.

---

## Part Three: Selling Without a Sales Team

The old founder-led sales playbook: manual DMs on LinkedIn, hand-written cold emails, spreadsheets, prayer. For enterprise, multiply the pain by twelve and add procurement.

That playbook is kaput. AI-native founders are selling to banks, hospitals, law firms, and universities with zero dedicated sales hires. Processes that used to take 18 months now move much faster.

Two unlocks converged. First, computer-use agents are finally good enough. They can see your screen, click buttons, fill forms. Claude Cowork, OpenAI Operator—they run in a browser tab. Point one at Sales Navigator.

Shawn Tsao from Snapp runs Cowork on a tab pointed at Sales Navigator. It reads his ICP filters, clicks through profiles, sends connection requests on autopilot, maxing out LinkedIn's 200-per-week limit. Each lead flows into Dripify for automated sequences. His review: "A bit scuffed, but it saves a ton of time."

Second, full pipeline automation. Clay, Lemlist, Attio. Build your lead list, enrich with AI, route into outreach tools with branching logic. Message viewed, reply received, no response, objection raised—each generates its own follow-up. Silvia Chen from Bilrost built this to sell loan processing software to banks. Her LinkedIn DMs are so flooded she can't open the app.

The bottleneck in enterprise sales isn't the pitch. It's getting the customer to believe in you comically early. Every industry has "tokens of trust"—SOC 2, compliance docs, pilot results. AI can't eliminate them, but it can compress the timeline from months to days. One founder got a letter of intent from Vanta the same morning he reached out. It unblocked a stalled deal.

The goal: you only do the part of sales that requires you personally—the demo, the relationship, the close. Everything upstream runs autonomously.

---

## Part Four: Orchestration Over Ownership

Perplexity rolled out Computer—a system that coordinates many models instead of betting on one. Different jobs (research, coding, data, browsing) route to different model families. The router is the leverage point. Aravind Srinivas has been clear: the power is in orchestration, not in owning the frontier model.

Notion added Custom Agents. Always-on agents that run recurring workflows across Notion, Slack, Calendar. Define what the agent does, when it runs, which databases it touches. Free until May 2026, then Notion credits. For teams that live in Notion, it's the first version that feels like an actual teammate rather than chat in a sidebar.

The pattern: orchestration and metering are the new product levers. Not owning the model is a feature, because it lets you use every model you want, whenever it's best for the task.

---

## Part Five: The Human Layer

Marily Nika writes about the weird, modern anxiety of building with AI. Not "AI will take my job"—the tool anxiety. The feeling that if you stop paying attention for a week, you'll fall behind forever.

Fast eats slow. But if you chase speed the way most people do—more tools, more tabs, more hacks—you don't get faster. You get noisier. And the noise is what's making everyone anxious.

She uses a Greek word: eudaimonia. Not happiness—a life well lived. Living in alignment with your values. Building with purpose. Making choices that compound your capability and your calm.

The framework: pick a north star outcome, not a tool. "Ship one prototype per week." Build toolchains, not tool collections. Set a hard budget for optimization—if it's not worth the time, ship the messy version and move on. Replace "keep up" with one concrete weekly ship. Momentum beats mastery.

The future is won by the people with the calmest inner system. Fast isn't clicking faster. Fast is the ability to move with clarity, again and again, without burning out.

Jenny Wen, head of design at Claude, says the classic design process—discovery, mock, iterate—is becoming obsolete. Engineers are forcing the role to evolve. Designers have to stay relevant in the age of AI. The question isn't whether AI will surpass humans in taste. It's how to build systems where human judgment and AI throughput coexist.

---

## What This Means for You

If you're building product in AI: adoption starts with you. Go hands-on. Measure what moves. Use power users as your signal.

If you're architecting agents: start with routing. Add reflection. Add memory. Don't jump to multi-agent swarms.

If you're selling: browser agents plus Clay plus trust artifacts. Founder-led sales is now agent-orchestrated. Compress the trust timeline.

If you're feeling the anxiety: build a system. One north star. One weekly ship. Toolchains, not tool collections. The calmest inner system wins.

---

*Sources: Lenny's How I AI (Coinbase), AI x Product (Agentic Design Patterns), a16z speedrun (GTM), The AI Collective (Perplexity, Notion), Marily's AI Product Academy (Eudaimonia), Lenny's (Design Process).*
