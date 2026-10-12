# Join the Rumoca research community

Help us make declared mathematics reusable and checkable across simulation,
identification, optimization and verification. Your Modelica knowledge and
experience in your own domain are valuable here.

**Start with a problem, a model and one result we can check together.**

Email **[jgoppert@purdue.edu](mailto:jgoppert@purdue.edu)**, or speak with
**James Goppert or Micah Condie** at the workshop. Tell us your problem, the
model you would like to use, and one result we could check together. A small
example and a clear question are enough to begin; no aerospace background is
required.

## Choose a first contribution

| Your interest | A useful first step |
|---|---|
| Modeling | Bring a small Modelica example with units, assumptions and expected behavior. Models from your own discipline help broaden the test cases. |
| Experiments and identification | Share a model/data question and a measurable validation target. Distinguish fitted data from held-out evidence. |
| Geometry and control | Propose a Lie-group modeling or control question with explicit frame conventions and a checkable baseline. |
| Reachability and verification | State a property and its assumptions: initial set, disturbances, chart domain, or software semantics. Help connect models with proof obligations. |
| Compiler and tools | Report a minimal reproduction, add a regression case, improve a backend or make the editor workflow easier. |
| Browser apps | Share your Rumoca app and its source, one checked result, the agent/tool used and elapsed build time. |

## Where the work lives

- [Rumoca](https://github.com/CogniPilot/rumoca): the open Modelica compiler;
  [compiler issues](https://github.com/CogniPilot/rumoca/issues) welcome concrete reproductions.
- [CogniPilot Modelica models](https://github.com/CogniPilot/modelica_models):
  reusable physics, Lie groups, estimation, planning and control building blocks.
- [This workshop](../README.md): a small shared-model workflow with synthetic data,
  numerical checks and [scoped Lean proofs](MATH_REVIEW.md).
- [Browser workbenches](BROWSER_APPS.md): fixed-wing experiments, a SLAM example
  in development and a motion-capture results viewer.
- [PURT pylon racing](https://pylon-racing.geddes.rcac.purdue.edu/): the next
  competition will leverage Rumoca. Follow the site for announcements and details.

## Research questions we can investigate together

Can we carry the same declared equations into estimation and control? How do
we preserve geometric structure when representing motion? What assumptions
make a reachable-set or software-verification claim valid? Which experiment
would expose the biggest gap between a digital twin and the physical system?

These questions need models, mathematics, software and experiments. Today's
workshop is one tested starting point; bring the next example and help define
the evidence it needs.
