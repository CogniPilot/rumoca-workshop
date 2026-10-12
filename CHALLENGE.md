# Open app challenge

**Announced at the opening · build throughout the workshop · demos and vote at 12:50**

Apply **Rumoca to a problem you care about**. Build an app with coding agents,
publish it on **your GitHub**, and show a working interaction.
The audience favorite wins a **free CogniPilot stocking cap**.
[App gallery and entry comments](https://github.com/CogniPilot/rumoca_workshop_amc2026/issues/1).

**Any subject, your own idea.** Choose the interface and supporting tools that
fit your problem. The fixed-wing example prompt is optional inspiration.

This is optional. The core Modelica → Rumoca → JAX → CasADi exercises need no
agent account, GitHub account or competition entry. Experienced participants
can start as soon as their environment is ready and use downtime and independent
work time to develop their app. Keep the core walkthrough available when needed.

## Inspiration and a small starting point

Copy an [example agent prompt](APP_PROMPT.md): invent an Artemis-inspired
launch experience with Three.js visuals, or extend the working fixed-wing app
into a “Tune the autopilot” flight lab. Both are optional starting ideas.
AD-based MPC is the **ambitious optional extension**.

Our lead example is
[rumoca_fixed_wing](https://cognipilot.github.io/rumoca_fixed_wing/): an
agent-built browser workbench with flight simulation, Modelica editing and an
autopilot. [Source](https://github.com/CogniPilot/rumoca_fixed_wing).

[slam_web](https://cognipilot.github.io/slam_web/) is another example **in
development**; its inertial demonstrations run, while full visual SLAM remains
work in progress. [mocap_sysid](https://cognipilot.github.io/mocap_sysid/) shows
another useful app pattern: exploring stored data and benchmark results.
[BROWSER_APPS.md](BROWSER_APPS.md) has short, rehearsed interactions for each.

You may build a new app or extend an existing one. Explain your contribution
and credit the starting project. A small interactive result is enough: for
example, expose one parameter, compare two runs, or add a useful view. You can
also choose a completely different subject.

## What to show at the end

- Your GitHub repository and what you contributed.
- One working interaction: change something and show the result.
- One result you checked and how you checked it.
- The coding agent/tool used, model/version when available, and elapsed build
  time. List multiple tools if used; label an estimated time as an estimate.

Enter by **12:40**: give the instructor your GitHub link, a one-sentence problem
description, agent/tool and elapsed build time, and a ready working interaction.
Post these in the [app gallery](https://github.com/CogniPilot/rumoca_workshop_amc2026/issues/1)
and tell the instructor you are ready.
Record wall time from starting the app to the demo-ready version, including
debugging and deployment; record active work separately if useful. Show where Rumoca is used and
explain what you contributed during the workshop. Individual and team entries
are welcome. Each participant may enter once, individually or as a member of
one team; a team has one entry. Choose one app for that entry. You may share
additional projects in the gallery without adding extra chances in the draw.
Keep all submitted links in a shared
gallery so everyone can explore the work, including apps not drawn to present.
Use your own available agent tools; keep credentials out of the published repo.

## Selecting presenters

The readiness check asks only whether the app uses Rumoca, has a GitHub link
and has a working interaction to show. It does not score visual polish,
technical complexity, aerospace relevance or the participant's experience.

If five or fewer entries are ready, all present. Otherwise, draw **five entries
at random**, plus one backup, from the ready entries. Draw the presentation
order too. Announce the selection by **12:45**. Give each entry the same chance;
selection is not a judgment of its quality. An unavailable presenter is replaced
by the backup. These rules are announced at the opening.

## Demos and audience vote

The showcase runs **12:50–12:55**. Each presenter gets **45 seconds**: the problem,
one working interaction, one checked result, and “built with [agent] in [time].”
Five demos take 3 minutes
45 seconds, leaving 75 seconds for the vote and stocking-cap award. Open tabs
in advance and stop each demo at the same time limit.

After the demos, the instructor names each entry and counts a **show of hands**.
Each attendee votes for one entry. The entry with the most votes wins one
stocking cap. A tie gets a quick vote among the tied entries; if the tie remains,
we draw among them. A winning team chooses who receives the cap.

## Prefer to stay with the core exercise?

Use [WORKSHOP.md](WORKSHOP.md). Optional extensions include trying another fit
starting guess, inspecting the generated backend source, or running the
rehearsed `--target-x 3` trajectory variant. Detailed mathematics and proof
scope are available in [MATH_REVIEW.md](MATH_REVIEW.md).
