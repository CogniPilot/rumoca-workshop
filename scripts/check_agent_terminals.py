"""Rehearse agent terminal startup without credentials or model requests (Linux)."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import fcntl
import json
import os
import pty
import select
import signal
import struct
import subprocess
import sys
import tempfile
import termios
import time

ROOT = Path(__file__).resolve().parents[1]
MARKERS = {
    "codex": ["OpenAI Codex", "Welcome to Codex", "Sign in with ChatGPT"],
    "claude": ["Welcome to Claude Code", "Choose the text style"],
    "copilot": ["Confirm folder trust", "Copilot v", "Sign in to GitHub"],
}


def check(name):
    scratch = Path.home() / "scratch/rumoca-workshop/agent-terminal-checks"
    scratch.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=name + "-", dir=scratch) as tmp:
        # A fresh private home keeps existing accounts and running agents untouched.
        env = os.environ.copy()
        for key in ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN",
                    "CLAUDE_CODE_OAUTH_TOKEN", "GH_TOKEN", "GITHUB_TOKEN", "COPILOT_GITHUB_TOKEN"]:
            env.pop(key, None)
        env.update(HOME=tmp, CODEX_HOME=tmp + "/.codex", CLAUDE_CONFIG_DIR=tmp + "/.claude",
                   XDG_CONFIG_HOME=tmp + "/.config", XDG_CACHE_HOME=tmp + "/.cache",
                   TERM="xterm-256color", COLORTERM="truecolor")
        for key in ["CODEX_HOME", "CLAUDE_CONFIG_DIR", "XDG_CONFIG_HOME", "XDG_CACHE_HOME"]:
            Path(env[key]).mkdir()
        master, slave = pty.openpty()
        fcntl.ioctl(slave, termios.TIOCSWINSZ, struct.pack("HHHH", 35, 120, 0, 0))
        socket = f"workshop-terminal-{os.getpid()}-{name}"
        command = ["tmux", "-L", socket, "new-session", "-A", "-s", "check", name]
        # Establish a controlling terminal in a fresh process; avoid preexec_fn
        # in this threaded runner because it can deadlock after fork.
        launcher = [sys.executable, "-c",
                    "import fcntl,os,sys,termios; fcntl.ioctl(0,termios.TIOCSCTTY,0); "
                    "os.execvpe(sys.argv[1],sys.argv[1:],os.environ)"]
        proc = subprocess.Popen(launcher + command, stdin=slave, stdout=slave, stderr=slave,
                                cwd=ROOT, env=env, start_new_session=True)
        os.close(slave)
        started = time.monotonic()
        screen = ""
        raw = b""
        try:
            while time.monotonic() - started < 60 and proc.poll() is None:
                if select.select([master], [], [], .2)[0]:
                    try:
                        chunk = os.read(master, 65536)
                    except OSError:
                        break
                    raw += chunk
                    # Respond as the participant's xterm frontend does. Detached tmux
                    # alone is insufficient: some TUIs wait for an attached terminal.
                    if b"\x1b[6n" in chunk:
                        os.write(master, b"\x1b[1;1R")
                    if b"\x1b[c" in chunk or b"\x1b[0c" in chunk:
                        os.write(master, b"\x1b[?1;2c")
                    if b"\x1b[>c" in chunk:
                        os.write(master, b"\x1b[>0;136;0c")
                capture = subprocess.run(["tmux", "-L", socket, "capture-pane", "-p", "-S", "-100", "-t", "check"],
                                         env=env, text=True, capture_output=True)
                screen = capture.stdout
                if any(marker in screen for marker in MARKERS[name]):
                    return {"status": "PASS", "version": subprocess.check_output([name, "--version"], env=env, text=True).strip(),
                            "initial_screen": next(m for m in MARKERS[name] if m in screen),
                            "wall_seconds": round(time.monotonic() - started, 3)}
            raise RuntimeError(f"{name} did not reach its initial screen: {screen[-1500:]} {raw[-3000:]!r}")
        finally:
            if name == "codex":
                # Stop only the daemon belonging to this temporary CODEX_HOME.
                subprocess.run([name, "app-server", "daemon", "stop"], env=env,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=20)
            pane = subprocess.run(["tmux", "-L", socket, "display-message", "-p", "-t", "check", "#{pane_pid}"],
                                  env=env, text=True, capture_output=True)
            if pane.returncode == 0:
                pid = int(pane.stdout.strip())
                try:
                    if os.getpgid(pid) == pid:
                        os.killpg(pid, signal.SIGTERM)
                        for _ in range(50):
                            time.sleep(.1)
                            try:
                                os.killpg(pid, 0)
                            except ProcessLookupError:
                                break
                        else:
                            os.killpg(pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            subprocess.run(["tmux", "-L", socket, "kill-session", "-t", "check"], env=env, capture_output=True)
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.terminate()
                proc.wait(timeout=5)
            os.close(master)


def main():
    # Launch in parallel just as independent participant terminals can be opened.
    with ThreadPoolExecutor(max_workers=3) as pool:
        results = dict(zip(MARKERS, pool.map(check, MARKERS)))
    report = {"status": "PASS", "agents": results,
              "scope": "Fresh private homes; real tmux clients attached through PTYs. Initial UI only, no authentication or model requests."}
    output = ROOT / "results/live/agent-terminals.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n")
    print("AGENT TERMINALS PASS: " + json.dumps(results))


if __name__ == "__main__":
    main()
