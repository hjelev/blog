---
title: "Vibe Coding vs Spec-Driven Development"
date: 2026-10-21
categories: [ai, cli]
---

# Vibe Coding vs Spec-Driven Development

![Vibe coding vs spec-driven development](/static/img/vibe-vs-spec-header.svg)

AI coding agents have made writing code cheap. Knowing *what* code to write, and whether the result is right, hasn't gotten any cheaper. Two very different ways of working with AI have grown out of that: **vibe coding**, where you chat with the agent and react to what it builds, and **spec-driven development (SDD)**, where you write down what you want first and let the agent build from that document.

Neither one is "correct". They solve different problems, and knowing when to switch between them is the useful skill.

## What is vibe coding?

The term comes from Andrej Karpathy, who described it in early 2025 as fully giving in to the vibes and "forgetting that the code even exists". It caught on so quickly that Collins Dictionary made it their word of the year for 2025.

In practice, vibe coding looks like this:

1. Describe what you want in plain language.
2. Let the AI write the code.
3. Run it and see what happens.
4. If something is off, describe the problem and repeat. You rarely read the diff.

It's fast, fun, and great for getting from zero to *something*. The weak spots show up later: nobody really knows how the code works, each "fix" can quietly break something else, and once the project no longer fits in the model's context, the agent starts forgetting decisions it made earlier.

## What is spec-driven development?

Spec-driven development flips the order. Before any code exists, you write a **specification**: what the feature should do, why it exists, the edge cases, and how you'll know it works. The AI then turns that spec into a technical plan, the plan into small tasks, and the tasks into code. The spec stays in the repo as the source of truth.

A typical SDD flow:

1. **Specify**: what you're building and why, plus acceptance criteria.
2. **Plan**: architecture, stack, data model, and constraints.
3. **Tasks**: the plan split into small steps you can review and test.
4. **Implement**: the agent works through the tasks.
5. **Verify**: check the result against the spec, not against your gut feeling.

The key idea is that when requirements change, you **update the spec** and regenerate from there, instead of piling on more chat prompts.

## The two workflows side by side

![Vibe coding loop vs spec-driven pipeline](/static/img/vibe-vs-spec-workflow.svg)

Vibe coding is one tight loop with a single checkpoint at the end: "does it look right?". Spec-driven development is a pipeline with a review gate between each step. You catch a wrong assumption in a one-page spec instead of in 2,000 lines of generated code.

## Comparison table

| | Vibe coding | Spec-driven development |
|---|---|---|
| **Starting point** | A prompt or an idea | A written specification |
| **Source of truth** | The code (and the chat history) | The spec, versioned in the repo |
| **Speed to first result** | ⚡ Minutes | 🐢 Slower: you write the spec first |
| **Speed over weeks** | Slows down as the codebase grows | Stays steady, since each change starts from the spec |
| **Who reviews the code** | Often nobody: "it runs, ship it" | Humans review the spec, plan, and tasks |
| **Handling changes** | New prompt on top of old ones | Edit the spec, then regenerate the plan and tasks |
| **Testing** | Manual: click around and see | Acceptance criteria come from the spec |
| **Context for the AI** | Whatever is left in the chat | Spec, plan, and project rules loaded every time |
| **Onboarding others** | Hard: decisions live in old chats | Easy: read the spec |
| **Typical failure** | "It worked yesterday" regressions, security holes | Over-planning a tiny change, specs that drift from the code |
| **Skill needed** | Describing what you want | Describing it *precisely*, plus knowing what to review |
| **Best for** | Prototypes, scripts, side projects, learning | Production code, teams, long-lived projects |

## When to use which

![When each approach fits](/static/img/vibe-vs-spec-when.svg)

A simple way to decide is to ask two questions: **how long will this code live**, and **how bad is it if it breaks**?

- **Short-lived and low-stakes** (a weekend project, a one-off script, a quick UI prototype): vibe code it. Writing a spec would take longer than the project.
- **Long-lived and high-stakes** (payments, auth, a shared API, anything a team maintains): use a spec. It's the cheapest place to catch mistakes.
- **Somewhere in between**: a "light spec" of five bullet points in a markdown file goes a long way. You don't need the full ceremony to get most of the benefit.

A common pattern is to **vibe code the prototype, then spec the real thing**. Use vibe coding to find out what you actually want, and once you know, write it down and rebuild it properly.

## Tools for spec-driven development

You can do SDD with nothing more than a markdown file and an agent, but some tools add structure:

- **[GitHub Spec Kit](https://github.com/github/spec-kit)**: an open-source CLI that adds slash commands to your agent (`/speckit-constitution`, `/speckit-specify`, `/speckit-plan`, `/speckit-tasks`, `/speckit-implement`). It works with Copilot, Claude Code, Gemini CLI, Cursor, and others.

  ```bash
  uv tool install specify-cli
  specify init my-project --integration copilot
  ```

- **[Kiro](https://kiro.dev/)**: an IDE from AWS built around specs. It generates `requirements.md`, `design.md`, and `tasks.md` for each feature, and has hooks that run agents when files change.
- **Claude Code / OpenCode plan modes**: both agents have a read-only planning mode (`Shift+Tab` in Claude Code, `Tab` in OpenCode) that's a lightweight way to agree on a plan before any code changes. Combine that with a `CLAUDE.md` or `AGENTS.md` file for project rules. See my [OpenCode vs Claude Code comparison](/linux/macos/cli/ai/opencode-vs-claude-code/) for more on both.

## A minimal spec template

If you want to try spec-driven development without new tools, drop something like this into `specs/feature-name.md` and ask your agent to plan from it:

```markdown
# Feature: Export notes as Markdown

## Why
Users want to back up their notes outside the app.

## What
- "Export" button on the notes page downloads a .zip of .md files
- One file per note, named after the note title
- Images are included in an /images folder

## Out of scope
- Importing notes back
- PDF export

## Acceptance criteria
- [ ] Exporting 0 notes shows a message instead of an empty zip
- [ ] Titles with / or : produce valid file names
- [ ] Export of 1,000 notes finishes in under 10 seconds
```

The "out of scope" section and the acceptance criteria do most of the work. They stop the agent from wandering off, and they give you a checklist for reviewing the result.

## Conclusion

Vibe coding and spec-driven development aren't rivals so much as two ends of a dial. Vibe coding is perfect for exploring and for code you'll throw away. Spec-driven development is what keeps AI-written code maintainable once other people, real users, or real money depend on it. Pick the setting based on what's at stake, and don't be afraid to move along the dial as a project grows up.
