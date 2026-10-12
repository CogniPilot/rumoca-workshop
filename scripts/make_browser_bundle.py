"""Package the canonical physics and its experiment into one pasteable file."""
from pathlib import Path
import hashlib

root = Path(__file__).resolve().parents[1]
source = (root / "models/Quadrotor.mo").read_text(encoding="utf-8")
wrapper = (root / "models/BrowserFlight.mo").read_text(encoding="utf-8")
dest = root / "browser/Quadrotor_browser.mo"
dest.parent.mkdir(exist_ok=True)
dest.write_text("// GENERATED bundle; physics source: models/Quadrotor.mo\n"
                "// Source SHA256: " + hashlib.sha256(source.encode()).hexdigest() + "\n"
                "// Paste all text in the playground. Create Scenario; set Model name BrowserFlight, end time 8 s; Run Simulation.\n"
                + source + "\n" + wrapper, encoding="utf-8", newline="\n")
print(dest)
