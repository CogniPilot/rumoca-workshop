"""Release maintenance: repair v0.10.2's nonportable libiconv install name.

Run on macOS with Apple's install_name_tool, otool and codesign. This edits only
dynamic-link metadata in a workshop-owned wheel; it does not change Rumoca code.
Participants use the resulting pinned artifact through uv, never this script.
"""
import argparse
import base64
import csv
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("wheel", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        with zipfile.ZipFile(args.wheel) as z:
            z.extractall(root)
        binary = next((root / "rumoca").glob("_native*.so"))
        before = subprocess.check_output(["otool", "-L", str(binary)], text=True)
        dependencies = [line.strip().split(" ")[0] for line in before.splitlines()[1:]]
        bad = [name for name in dependencies if name.startswith("/nix/store/")]
        if len(bad) != 1 or not bad[0].endswith("/lib/libiconv.2.dylib"):
            raise RuntimeError(f"Unexpected upstream dynamic links; refusing repair: {dependencies}")
        subprocess.run(["install_name_tool", "-change", bad[0], "/usr/lib/libiconv.2.dylib", str(binary)], check=True)
        subprocess.run(["codesign", "--force", "--sign", "-", str(binary)], check=True)
        after = subprocess.check_output(["otool", "-L", str(binary)], text=True)
        if "/nix/store/" in after:
            raise RuntimeError("Nonportable dependency remains")
        record = next(root.glob("*.dist-info/RECORD"))
        rows = []
        for file in sorted(root.rglob("*")):
            if file.is_file() and file != record:
                content = file.read_bytes()
                digest = base64.urlsafe_b64encode(hashlib.sha256(content).digest()).decode().rstrip("=")
                rows.append([file.relative_to(root).as_posix(), "sha256="+digest, str(len(content))])
        rows.append([record.relative_to(root).as_posix(), "", ""])
        buffer = io.StringIO(newline="")
        csv.writer(buffer).writerows(rows)
        record.write_text(buffer.getvalue())
        output = args.output / args.wheel.name
        with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as z:
            for file in sorted(root.rglob("*")):
                if file.is_file():
                    z.write(file, file.relative_to(root).as_posix())
        evidence = {"upstream_sha256": hashlib.sha256(args.wheel.read_bytes()).hexdigest(),
                    "repaired_sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
                    "change": "libiconv dynamic library install name -> /usr/lib/libiconv.2.dylib; ad-hoc codesign; regenerated wheel RECORD",
                    "otool_before": before, "otool_after": after}
        (args.output / (args.wheel.stem+"-repair.json")).write_text(json.dumps(evidence, indent=2)+"\n")
        print(output)


if __name__ == "__main__":
    main()
