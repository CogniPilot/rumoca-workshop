# Open interactive experiment challenge

**Announced at the opening · experiment during downtime · demos and vote at 12:50**

Apply **Rumoca to a problem you care about**. Change an existing model,
controller or interactive simulator, show the effect, and explain one result
you checked. The audience favorite wins a **free CogniPilot stocking cap**.

**Any subject, your own idea.** A new web app, WASM build, public GitHub repo
and deployment are optional stretch goals. A model in the Rumoca playground,
a plot from your Codespace/local workflow, or a change in an existing browser
workbench is enough. Coding agents are optional; document your tool and time.

The core Modelica → Rumoca → JAX → CasADi exercises remain the main workshop.
Use downtime and independent work for the challenge, and keep the walkthrough
available when needed. No extra account is required to enter or present.

## Start with a working example

Choose one question, one change and one comparison. For example:

- Change a controller or scenario in the existing fixed-wing workbench and
  compare its response with the original.
- Modify a workshop model or optimization constraint, rerun it, and explain
  the resulting tradeoff.
- Bring a model from your own domain into the playground and expose one
  behavior someone can explore interactively.

Our lead workbench is
[rumoca_fixed_wing](https://cognipilot.github.io/rumoca_fixed_wing/), with Modelica
editing, flight simulation and an autopilot.
[Source](https://github.com/CogniPilot/rumoca_fixed_wing).
[Short tested interactions](BROWSER_APPS.md) provide a starting point.

A Falcon 9-style interactive landing experience is creative inspiration, not
a supplied or qualified rocket model. Keep any such model's simplifying
assumptions visible. A comparable small experiment in your own domain is welcome.

[APP_PROMPT.md](APP_PROMPT.md) starts with a short experiment prompt. Its public
Three.js launch app and AD-based fixed-wing MPC prompts are optional stretches;
MPC is ambitious. No Artemis or Falcon 9 app is supplied by this workshop.

## What to show

- Your question and what you changed beyond following the worksheet.
- One working interaction or before/after comparison using Rumoca.
- One result you checked and how you checked it.
- Agent/tool used, model/version when available, and elapsed work time.
  Say “manual” if no agent was used; label estimated times as estimates.

Enter by **12:40**: tell the presenters your name/team, one-sentence question,
starting model/app, tool and elapsed time, and how you will show the result.
A live tab, local file or screen share is acceptable. A repository/live link
is useful when available, but is not required. Share your starting project
and credit its authors.

Use the [gallery](https://github.com/CogniPilot/rumoca_workshop_amc2026/issues/1)
if you want to share links publicly. Otherwise give the entry to the presenters;
a GitHub login or public upload is unnecessary. Record wall time from starting
work to the demo-ready result, including debugging; active work may be recorded
separately. Individual and team entries are welcome.

Each participant may enter once, individually or as a member of one team;
a team has one entry. Additional projects can go in the gallery without adding
extra chances in the draw.

## Selecting presenters

The readiness check asks only whether the experiment uses Rumoca, includes your
own change, and has a working interaction or comparison to show. It does not
rank visual polish, complexity, aerospace relevance, tool choice or experience.

If five or fewer entries are ready, all present. Otherwise draw **five entries
at random**, plus one backup. Draw the presentation order too. Announce selection
by **12:45**. Each entry has the same chance; selection is a time limit, not a
quality judgment. An unavailable presenter is replaced by the backup.
Announce these rules at the opening.

## Demos and audience vote

The showcase runs **12:50–12:55**. Each presenter gets **45 seconds**: question,
change, result, one check, and “worked with [tool] for [time].” Five demos take
3 minutes 45 seconds, leaving 75 seconds for the vote and award. Open tabs or
files in advance; use the same time limit for everyone.

Each attendee votes for one entry by a **show of hands**. Count visibly.
The audience favorite wins one free CogniPilot stocking cap. A tie gets a quick
vote among the tied entries; if it remains, draw among them. A winning team
chooses who receives the cap. Share voluntary links from all entries, including
those not drawn to present.

## Prefer to stay with the core?

Use [WORKSHOP.md](WORKSHOP.md). Detailed mathematics and proof scope are in
[MATH_REVIEW.md](MATH_REVIEW.md). A new experiment needs its own checks; the
workshop's Lean proofs do not automatically apply to your edits.
