# Publication and cloud preflight

The standalone public repository is
<https://github.com/CogniPilot/rumoca-workshop>. It is independent of the main
Rumoca repository, with explicit pinned release dependencies. Participants can
download the ZIP without a GitHub account. The supplied internal handoff brief
is ignored and has not been published.

Links ready for sharing (no message has been sent on your behalf):

- Participant entry: <https://github.com/CogniPilot/rumoca-workshop/blob/main/WORKSHOP.md>
- Repository: <https://github.com/CogniPilot/rumoca-workshop>
- ZIP: <https://github.com/CogniPilot/rumoca-workshop/archive/refs/heads/main.zip>
- Codespace: <https://codespaces.new/CogniPilot/rumoca-workshop?quickstart=1>
- Browser: <https://rumoca.cognipilot.org/playground/>

Suggested preflight text: “Before Monday, choose browser-only or full Python
participation. Browser needs no account. For full work, download the workshop,
install uv and run `uv sync --frozen` followed by the smoke-test command in the
README, or use an account with Codespaces allowance. Bring a charged laptop.
If setup fails, you can pair up and continue with browser/reference figures.”

## Codespaces: required personal preflight

Container build and postCreate commands are exercised in CI. A **fresh cloud
Codespace** was not created: the authenticated automation token returned HTTP
403 because it lacks `codespace` scope. No billing/policy changes were made.

Before describing Codespaces as the preferred full route, the instructor must:

1. Create a new Codespace from `main` with the actual account and desired region.
   Measure first start; check postCreate says WORKSHOP PASS.
2. Open `.mo` and confirm the Rumoca extension runs remotely; test hover,
   completion and an intentionally broken line followed by undo. Confirm the
   Python interpreter points into `.venv` and the terminal runs all three tasks.
3. Check account remaining usage, organization policies, authorized billing and
   supported machine sizes. Fifty attendees do not share one guaranteed free
   allowance. Public repository access does not supply cloud compute.
4. If authorized and supported, configure repository **Settings → Codespaces →
   Prebuilds**, region and branch; wait for “ready” and test creating from it.
   Record which region and account were tested. No ready prebuild exists on the
   basis of the container workflow alone.
5. Check capacity/concurrent-account restrictions with the venue/organization;
   plan local and pair fallbacks. Do not create fifty billed environments as a
   synthetic capacity test without explicit budget authorization.

[GitHub’s billing documentation](https://docs.github.com/en/billing/concepts/product-billing/github-codespaces)
and [included usage](https://docs.github.com/en/billing/reference/product-usage-included)
describe account-dependent allowances; organization-paid usage differs from
personal included usage. Do not promise “free for everyone.”
[Prebuild documentation](https://docs.github.com/en/codespaces/prebuilding-your-codespaces/about-github-codespaces-prebuilds)
explains plan/budget requirements and that `onCreateCommand`/`updateContentCommand`
run during prebuilds, while `postCreateCommand` runs at individual creation.
This configuration caches dependencies in the image and runs `uv sync`/smoke
at postCreate; it does not falsely claim to prebuild all extension activation.

If fresh-cloud qualification is unavailable, use the **tested browser + local
uv** route on stage and label Codespaces as an optional configured route.

## Qualified macOS wheel release

The workshop owns release
[workshop-wheels-2026](https://github.com/CogniPilot/rumoca-workshop/releases/tag/workshop-wheels-2026).
Upstream macOS 0.10.2 wheels contained a nonportable libiconv load reference.
The maintainer repair script changes that reference to the operating system’s
libiconv, signs the library and regenerates wheel RECORD. It does not alter
compiler code. Frozen hashes select these two tested artifacts automatically.
Linux/Windows retain upstream release wheels. See [NOTICE.md](NOTICE.md).

No Nix, Rust compiler or manual binary repair is required for attendees. Python
OS qualification does not imply macOS/Windows VS Code extension qualification.
