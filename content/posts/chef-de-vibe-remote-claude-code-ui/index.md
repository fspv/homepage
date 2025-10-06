---
title: "Chef de Vibe - Remote Claude Code UI"
date: 2025-10-06T10:00:00-07:00
draft: false
slug: "chef-de-vibe-remote-claude-code-ui"
tags:
  [
    "claude",
    "claude-code",
    "AI",
    "development",
    "tools",
    "remote-development",
    "vibe-coding",
    "UI",
  ]
---

# How I Built a Mobile Coding Interface in Two Weeks Without Writing a Single Line of Code

## The Eureka Moment

I had a brilliant coding idea while sitting on the toilet. Two hours later, I had a working prototype that let me code from my phone. Two weeks after that, I had a fully functioning system - and I didn't write a single line of code myself.

Let me back up a bit.

## The Problem: Losing the Coding Momentum

Like many developers, my best ideas often strike at the worst times - during my commute, morning coffee runs, or in other moments far from my laptop. In these moments, I'm bursting with enthusiasm and ready to prototype immediately. But I can't, because coding requires my IDE to be open.

Best case scenario? I jot the idea down somewhere and revisit it later. More often, I forget about it entirely. By the time I'm back at my laptop, either the moment has passed or I'm swamped with other tasks.

Over the past year, I've been really enjoying "vibe coding" - quick, enthusiasm-driven development sessions that have produced several useful pet projects. But for this to work, the stars need to align:

- I need an idea and enthusiasm right now
- I need to be near my laptop
- I need several hours of uninterrupted time

The problem? This rarely happens.

## The Solution: Claude Code Goes Mobile

Since most of my recent coding was through Claude Code (Anthropic's agentic coding tool), the solution seemed obvious: why not build a UI for it? I was impressed by Google's Jules and wanted to create something similar on top of Claude Code. After all, I was already paying for a subscription and had extensive experience with it. If I could access Claude Code from any device, anywhere, I'd never lose coding momentum again.

Initially, I considered using existing UIs. Several were available, but they lacked critical features I needed:

- Approval requests from Claude
- Session persistence (every request started a new chat in some implementations)
- Running Claude instances in Docker containers

This led me to the question I find myself asking more frequently these days: Why use a third-party tool when I can "vibe code" exactly what I need in a couple of hours?

Decision made. Let's build our own UI.

## Attempt 1: Overengineering the Solution

My first approach tried to copy Jules' architecture: connect a GitHub repo, spawn a Docker container, make code changes, and submit a PR to GitHub. I had a prototype running in about two hours.

But I quickly realized this approach was overly complex and inflexible. I couldn't just drop into a directory and start coding - I needed a GitHub repo. Setup required configuring GitHub OAuth with correct URLs, placing keys in specific locations, and more. End-to-end testing was nearly impossible.

**This was my first "aha" moment about agentic coding.** I'd spent just a few hours from idea to working prototype, quickly discovered it wasn't the right approach, and could immediately pivot. Without AI, I would have invested weeks before realizing the approach was flawed. At that point, sunk cost fallacy might have kept me pushing forward with a dead idea. With AI, I could fail fast and move on.

## Attempt 2: Learning from Others

After the first failure, I researched existing solutions. Surely I wasn't the first with this idea. I tried several similar projects but encountered the issues described earlier. I spent a couple of evenings testing alternatives and even posted on discussion boards asking for help with my specific requirements. As often happens in open source - no response.

## Attempt 3: Serious Vibe Coding

Armed with experience from my failed attempts, I started fresh with a proper design phase. Even for greenfield projects built with AI, following standard engineering processes pays dividends.

### The Design Phase

I used two AI models for the design: Gemini 2.5 Pro and Claude Opus 4. I had them extract all my requirements through questioning, validate there were no logical or functional gaps, and cross-validate each other's work. The result was a detailed backend service design (available at https://github.com/fspv/chef-de-vibe/blob/master/src/README.md ).

I kept the frontend design minimal - the hard part there would be visual representation, which I'd tackle later.

### Backend Development

Key decisions for the backend:

- **README as source of truth**: All logic was documented in the README first. Any changes required updating the README before the code. This README also drove the e2e test generation, ensuring the service behaved as intended without manual code review.
- **Language choice: Rust**: A language I would never have chosen for this project otherwise due to my limited expertise. But it's perfect for AI coding - the strict compiler and configurable Clippy linters constrain the LLM from producing nonsense. Despite my concerns about debugging complex borrowing issues, none materialized during two weeks of development.

The first backend version was running in exactly two hours. Code generation took 20 minutes; the rest was spent figuring out Claude Code CLI options (the documentation is surprisingly poor and sometimes incorrect, requiring trial and error).

The orchestrator service could now:

- Start new Claude Code instances with existing sessions from disk or create new ones
- Keep Claude Code processes running as long as needed
- Connect users (frontend) to Claude Code stdio via WebSocket

### Frontend Development

With a complete backend specification, frontend generation was straightforward - up and running within an hour. I could now send my first "Hello World" requests to Claude Code from a browser and receive responses.

## Productionizing: Where AI Productivity Slows

The prototype was running in hours. Making it production-ready should be quick too, right?

Wrong.

AI excels at building MVPs but becomes less efficient during productionization. Don't misunderstand - it's still MUCH faster than manual coding, but there are countless details: bug fixes, CI/CD, visual polish, missing features, edge cases.

I also invested time in first-class container support for Claude Code instances - my secondary dream was running each instance in an isolated environment. I implemented a generic solution allowing users to provide their own scripts for container management (Docker, Podman, or even libvirt).

Timeline:

- Backend stabilization: ~1 week of evening work
- Frontend completion: Another week (developed using Chef de Vibe itself, pointing to the stable backend)

## The Result

After two weeks, it was done. Chef de Vibe serves all my immediate needs perfectly. I've coded from trains, airports, conferences, and yes, bathrooms. It works beautifully, and I'm thrilled to maintain coding momentum regardless of location.

The entire codebase is 100% AI-generated - a testament to AI's maturity as a tool in the software engineering arsenal.

## Reflections on the Future

I strongly believe that mobile coding (in some form) is the future. Returning to a laptop feels like visiting a computer lab to write Turbo Pascal. We should be able to tell computers what to do (ideally by voice) and come back to check results later. Typing code or even prompts on a keyboard at home feels increasingly inefficient.

What I've built is just a shy validation of this concept. We're scratching the surface of what's possible. Future tools will be exponentially more powerful. But even this clumsy MVP solves real problems and taught me valuable lessons about AI-assisted development.

## Key Takeaways

1. **AI changes the economics of experimentation**: Failing fast is now measured in hours, not weeks
2. **Language choices change with AI**: Strongly-typed languages with strict compilers become more attractive
3. **Process still matters**: Even with AI, proper design and documentation pay dividends
4. **The last 20% is still hard**: AI accelerates MVP development dramatically but productionization remains detail-oriented
5. **We're living in the future**: Coding from anywhere is not just possible - it's practical

## What's Next?

Chef de Vibe is open source and available at [GitHub](https://github.com/fspv/chef-de-vibe). I'm excited to see how others use and extend it. The future of development is collaborative - between humans and AI, between developers across time zones, and between ideas and implementation, regardless of physical location.

Welcome to the age of truly mobile development.
