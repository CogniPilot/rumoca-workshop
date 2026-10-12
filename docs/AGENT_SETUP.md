# Optional coding agents

The core workshop needs no AI account. The containers include Codex, Claude and Copilot
CLIs, Node/npm, GitHub CLI and tmux, plus Codex, Claude Code and GitHub Copilot
Chat extensions. Versions are recorded in [the tool manifest](../scripts/agent_tools.json);
these are the latest releases checked when this workshop image was prepared.
A running Codespace keeps its installed versions until you update or rebuild it.
If your Codespace predates this rehearsal's image update, pull the repository
and run **Codespaces: Rebuild Container** once before class. The complete Codex
package is required for its interactive background server. In an older container,
`codex --no-daemon` is a temporary terminal fallback.

## Sign in with your own account

Open the Codex, Claude or Copilot panel in VS Code and follow its sign-in flow.
Alternatively, run `codex`, `claude` or `copilot` in the terminal and follow the login
instructions. Subscription access and usage limits belong to your account.
Your GitHub Codespace login does not automatically sign you into either AI
provider. The first terminal launch may ask you to choose a theme or trust the
workspace before showing the login options.

| Agent | Terminal login in Codespaces |
|---|---|
| Codex | `codex login --device-auth`, open its browser link, enter the displayed code, then run `codex`. Device login must be enabled in your ChatGPT security settings or workspace permissions. |
| Claude Code | Run `claude`, choose a theme and follow its sign-in instructions; use `/login` to sign in again. |
| Copilot | Run `copilot login` and follow its browser/device-code instructions, then run `copilot`. |

Official instructions: [Codex authentication](https://learn.chatgpt.com/docs/auth),
[Claude authentication](https://code.claude.com/docs/en/authentication),
[Copilot authentication](https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/authenticate-copilot-cli).

## First experiment: edit, run and inspect

Paste this after signing in:

```text
Read docs/WORKSHOP.md and examples/simulate.py. Use the existing Rumoca Python
Session API, importing rumoca as rum, to compare the planar quadrotor at three
quadratic drag coefficients. Keep the workshop model and original examples
unchanged. Put your script in examples/agent_experiment/ and your results in
results/live/agent_experiment/ so I can see them in the VS Code Explorer.
Run with uv run --frozen python, plot the response with units, and check that
increasing positive drag reduces travel in the same coast experiment. Explain
the actual measured result. Do not install packages or publish anything.
```

Review its changes in **Source Control**, open the generated plot, and ask for
one improvement at a time. Keep normal permission prompts and check the agent's
reported result against its terminal output.

Do not paste credentials into a model, prompt, slide or tracked file. For API
billing, use your own account-level [Codespaces secrets](https://docs.github.com/en/codespaces/managing-your-codespaces/managing-your-account-specific-secrets-for-github-codespaces)
restricted to this repository. Account login files under the container home
may need to be recreated after a rebuild.

## Keep an experiment running while presenting

Choose **Terminal → Run Task → Workshop: Codex terminal (tmux)** or
**Workshop: Claude terminal (tmux)** or **Workshop: Copilot terminal (tmux)**. Authenticate, paste your experiment prompt,
and allow the initial workspace permissions. Keep normal permission prompts;
return to the terminal if the agent needs an answer. Ask it to work in
`examples/agent_experiment/` and save plots under `results/live/agent_experiment/`
so the experiment stays visible beside the core examples.

Detach with **Ctrl+B**, then **D**. Return with:

```sh
tmux attach -t workshop-codex
# or
tmux attach -t workshop-claude
# or
tmux attach -t workshop-copilot
```

This survives closing a terminal tab while the container runs. A stopped or
rebuilt Codespace ends running agents and tmux sessions. Save outputs under the
workspace and commit useful work. See [example prompts](APP_PROMPT.md).

## Updates and your work

Pulling repository updates does not rebuild an existing Codespace. Save your
work, inspect **Source Control**, commit useful changes, then pull when ready.
To apply `.devcontainer` changes, use **Codespaces: Rebuild Container**. It uses
your current working tree's configuration, including your local changes.

Files under `/workspaces` survive a stop/start and rebuild, including uncommitted
edits. Programs installed manually and files elsewhere in the container are
recreated on rebuild. Declare tool installations in the Dockerfile/features,
and commit configuration changes you want to share. A full rebuild also clears
cached Docker images and volumes. Processes do not survive either rebuild.
See [GitHub's rebuild documentation](https://docs.github.com/en/codespaces/developing-in-a-codespace/rebuilding-the-container-in-a-codespace).

Deleting a Codespace is different: push your work or download it first.
Each participant creates their own Codespace and uses their own credentials;
the workshop image contains no presenter login or API keys. GitHub supplies
repository-scoped access in Codespaces; publishing a new repository can require
additional GitHub authorization. Copilot CLI may also require its own login.
