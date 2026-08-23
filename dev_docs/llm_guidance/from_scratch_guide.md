# SHAPR From Scratch — A Plain-English Guide

A step-by-step, jargon-free walkthrough for starting a brand-new project with SHAPR. Read this first when setting up a fresh repository; the other files in `llm_guidance/` cover the individual components in detail.

## The one idea behind it

Don't document everything as you go — that burns you out and you quit. Instead: **do the work, jot tiny notes as you go, and spend a few minutes "tidying" at the end of each chunk of work (a cycle).** The notes you keep are the reason you (or an examiner, or a teammate) can later see *why* you built things the way you did.

Three rules that stay with you the whole time:
1. **Work → Learn → Update → Repeat.** Never "work → document everything → burn out."
2. **If the paperwork is slowing you down, you're doing too much.**
3. **The human is the boss; the AI is the helper.** The AI can draft, tidy, and summarise — the human decides what is true.

## Step 0 — Create the folder skeleton

Make a `docs/` folder (on this project: `dev_docs/`) with a `current/` folder holding all the role folders, plus `snapshots/` and an instruction folder beside it:

```
docs/
├── current/              ← the only place you edit during a cycle
│   ├── 01_system/        design notes — what the app *is* (architecture, modules)
│   ├── 02_contracts/     interface rules — the fixed promises between parts
│   ├── 03_control/       process notes — decision log, snapshot rules
│   ├── 04_working/       live notes — where things stand, the to-do list, the boss document
│   └── 05_knowledge/     learning notes — what you learned and want to keep
├── cycle_record_notes/   one file per chunk of work, plus a review per chunk (the historical record)
├── snapshots/             frozen copies of current/ at each chunk boundary
└── llm_guidance/          instruction files for the AI (not snapshotted)
```

You don't need all seven on day one. Even `03_control` + `04_working` + `cycle_record_notes` gives 80% of the benefit.

## Step 1 — Write the boss document first

Before anything else, write `source_of_truth.md` in `04_working`. It answers one question: **"if two notes disagree, which one wins?"**

A minimal version for a fresh project:
- The **code** is the truth about what exists.
- `current_state.md` is the truth about where the project is now.
- `tasks.md` is the truth about what's being worked on.
- `decisions.md` is the truth about *why* things were chosen.
- The **current task** overrides everything while it is being done.

This one file is the single biggest defence against notes drifting apart. Refine it later; start minimal.

## Step 2 — The tiny capture habit (during work)

While working, keep **three small notes** and append a line whenever something notable happens:
- `tasks.md` — what's being done and what's left (tick boxes).
- `decisions.md` — each time a choice is made on purpose ("we use X instead of Y because …"), add one line.
- `reflection.md` — each time something worth remembering surfaces ("widgets die with their parent window").

Append short lines. Do not tidy them yet — tidying happens at the cycle close.

## Step 3 — Run one cycle

A cycle is "a chunk of work with a clear goal." For each one:

1. **Set the goal** in `cycle_plan.md` (here: `ROADMAP.md`): goal, what "done" looks like, success check. Keep it small enough to finish in days, not months.
2. **Open a fresh chat with the AI** and hand it the handoff set: the code, `current_state.md`, `source_of_truth.md`, and only the notes relevant to this task. Not everything.
3. **Work** — code, test, append tiny notes.
4. **Close the cycle**:
   - Update `current_state.md` (where are we now?).
   - Write `cycle_record_notes/cycle_N.md`: what it set out to do, what got built, what was used, what went wrong, what was learned.
   - Write `cycle_record_notes/cycle_N_review.md` from a fresh, skeptical eye: what worked, what's still broken, verdict.
5. **Snapshot** — copy the whole `current/` folder into `snapshots/cycle_N_close/` (one command: `cp -r current snapshots/cycle_N_close/`). Frozen; never edit it. It is the time capsule and the next chunk's handoff.
6. Start the next chunk from that snapshot.

## Step 4 — Write a knowledge card for the learning that mattered

On a real discovery — a bug with a surprising cause, an architectural choice with real trade-offs, a mistake the AI made — write a small card with **exactly four lines**:

1. **Context** — the problem or situation.
2. **Decision** — what was actually done.
3. **Observation** — what happened when it ran.
4. **Learning** — *why* it happened and why future-you should care.

Give each card a number (`SKU-001`, `SKU-002`, …) that **never restarts** across the whole project, so a commit message or the final write-up can point to "card #7".

**The important bit: don't write a card for everything.** Cards are for decisions or lessons with a reason. Changing a slider's thickness, adding an ignore file, bumping a version — trivial; those go on `tasks.md`, not the knowledge cards. If it wouldn't change how you'd do things later, it's not a card.

## Step 5 — Write the "from the outside" reflection

Right after each cycle, add a short "what did this chunk teach me about *doing projects*" in `current/05_knowledge/reflection.md` — not about the code. This layer is what eventually becomes the write-up, which is what makes the whole thing worthwhile.

## Step 6 — Repeat

Each cycle takes the last snapshot, sets a new goal, works, closes, snapshots. That is the entire system.

## Minimum viable version

Create the folders + `source_of_truth.md` + `tasks.md` + `current_state.md` + `decisions.md`; do tiny capture during the work; at the end of each chunk write `cycle_N.md` + `cycle_N_review.md` and copy `current/` to `snapshots/cycle_N_close/`. Everything else is polish.

## Related
- `README.md` — the component index; load the right file per task.
- `sku_instruction.md` — the knowledge-card rules in detail.
- `cycle_record_instruction.md` — the exact cycle record and review templates.
- `working_docs_instruction.md` — the live notes and the boss document.
- `conventions_instruction.md` — tags, IDs, evidence, the anti-burnout rules.
