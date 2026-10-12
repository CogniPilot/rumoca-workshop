"""Check packaged workshop links, deck freshness and shared-model provenance."""
from pathlib import Path
from urllib.parse import unquote
import csv
import hashlib
import json
import re
import zipfile
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
def read(name):
    return json.loads((ROOT/name).read_text(encoding="utf-8"))
def digest(name):
    return hashlib.sha256((ROOT/name).read_bytes()).hexdigest()

def main():
    documents = list(ROOT.glob("*.md")) + list((ROOT/"data").glob("*.md")) + [ROOT/"slides/workshop.md"]
    documents = [p for p in documents if p.name != "Rumoca_Workshop_Handoff.md"]
    links = 0
    for doc in documents:
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", doc.read_text(encoding="utf-8")):
            if re.match(r"[a-zA-Z][\w+.-]*:", target) or target.startswith("#"):
                continue
            target = unquote(target.split("#")[0].split(' "')[0]).strip("<>")
            assert (doc.parent/target).exists(), f"Broken link: {doc.relative_to(ROOT)} → {target}"
            links += 1
    source = digest("models/Quadrotor.mo")
    for name in ["data/truth.json", "results/reference/simulation.json", "results/reference/fit_drag.json",
                 "results/reference/optimization.json", "results/reference/smoke.json", "results/reference/math_audit.json"]:
        assert read(name)["source_sha256"] == source, f"Stale model provenance: {name}"
    fit = read("results/reference/fit_drag.json")
    control = read("results/reference/optimization.json")
    assert fit["data_sha256"] == digest("data/noisy_flight.csv")
    assert control["fit_sha256"] == digest("results/reference/fit_drag.json")
    proof = read("formal/provenance.json")
    assert proof["model_sha256"] == source
    assert proof["solve_program_sha256"] == digest("formal/solve_program.json")
    assert proof["lean_sha256"] == digest("formal/Generated.lean")
    bundle = (ROOT/"browser/Quadrotor_browser.mo").read_text(encoding="utf-8")
    assert source in bundle and (ROOT/"models/Quadrotor.mo").read_text(encoding="utf-8").strip() in bundle
    with (ROOT/"data/noisy_flight.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 644 and len({r["flight"] for r in rows}) == 4
    assert {r["split"] for r in rows} == {"train", "validation"}
    build = read("slides/build-report.json")
    from build_slides import parse
    parse()  # Validate actual slide times and breaks, rather than only the report.
    assert build["schedule_minutes"] == 180 and build["break_minutes"] == 20
    for name, expected in {**build["input_sha256"], **build["artifact_sha256"]}.items():
        assert digest(name) == expected, f"Deck needs rebuilding: {name}"
    presentation_report = read("verification/presentation.json")
    assert presentation_report["status"] == "PASS"
    assert presentation_report["pptx_sha256"] == digest("slides/workshop.pptx")
    ns = {"p":"http://schemas.openxmlformats.org/presentationml/2006/main"}
    with zipfile.ZipFile(ROOT/"slides/workshop.pptx") as deck:
        slides = [n for n in deck.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)]
        notes = [n for n in deck.namelist() if re.fullmatch(r"ppt/notesSlides/notesSlide\d+\.xml", n)]
        assert len(slides) == build["slides"] == len(notes) == 28
        presentation = ET.fromstring(deck.read("ppt/presentation.xml"))
        assert len(presentation.find("p:sldIdLst", ns)) == 28
    for name in ["rumoca_fixed_wing", "slam_web", "mocap_sysid"]:
        assert read(f"verification/app-{name}.json")["status"] == "PASS"
        assert (ROOT/f"slides/assets/app-{name}.png").is_file()
    for name, script in [("torch_backend", "check_torch_backend"), ("torch_policy", "learn_hover_torch")]:
        receipt = read(f"results/reference/{name}.json")
        assert receipt["status"] == "PASS" and receipt["source_sha256"] == source
        assert receipt["script_sha256"] == digest(f"scripts/{script}.py")
        for target, expected in receipt["target_sha256"].items():
            assert digest(f"templates/torch-ode/{target}") == expected
    assert read("verification/user-guide.json")["status"] == "PASS"
    report = {"status":"PASS", "local_markdown_links":links, "slides":28, "schedule_minutes":180,
              "break_minutes":20, "model_sha256":source,
              "checks":["local links", "shared model/result/CSV/formal/browser provenance", "deck input/artifact hashes",
                        "PPTX slides, speaker notes and office-renderer provenance", "app rehearsal receipts",
                        "Torch target and policy source/template provenance", "embedded user-guide rehearsal receipt"],
              "scope":"Packaging consistency. Mathematical, numerical and UI checks have separate receipts."}
    (ROOT/"verification/materials.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8", newline="\n")
    print(f"MATERIALS PASS: {links} local links, 28 slides with notes, 180 minutes, matching provenance")

if __name__ == "__main__":
    main()
