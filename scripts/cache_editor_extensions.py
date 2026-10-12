"""Cache qualified public VSIX files in the image before participant startup."""
from pathlib import Path
import argparse
import hashlib
import gzip
import json
import platform
import shutil
import time
import urllib.request
import zipfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('/opt/workshop-vsix'))
    args = parser.parse_args()
    pins = json.loads(Path(__file__).with_name('agent_tools.json').read_text())['extensions']
    extensions = {name: version for name, version in pins.items() if version}
    extensions.update({'mathematic.vscode-pdf': '0.1.11', 'leanprover.lean4': '0.0.240',
        'samuelcolvin.jinjahtml': '0.20.0', 'bierner.markdown-preview-github-styles': '2.2.0',
        'JamesGoppert.rumoca-modelica': '0.10.2'})
    arch = {'x86_64': 'x64', 'aarch64': 'arm64'}[platform.machine()]
    args.output.mkdir(parents=True, exist_ok=True)
    records = {}
    for identifier, version in extensions.items():
        publisher, name = identifier.split('.', 1)
        if identifier == 'JamesGoppert.rumoca-modelica':
            url = f'https://github.com/CogniPilot/rumoca/releases/download/v{version}/rumoca-modelica-linux-{arch}-{version}.vsix'
        else:
            url = f'https://marketplace.visualstudio.com/_apis/public/gallery/publishers/{publisher}/vsextensions/{name}/{version}/vspackage'
            if identifier.startswith(('openai.', 'anthropic.')):
                url += f'?targetPlatform=linux-{arch}'
        file = args.output/f'{identifier.lower()}-{version}.vsix'
        for attempt in range(3):
            try:
                with urllib.request.urlopen(url, timeout=120) as source, file.open('wb') as output:
                    stream = gzip.GzipFile(fileobj=source) if source.headers.get('Content-Encoding') == 'gzip' else source
                    shutil.copyfileobj(stream, output)
                with zipfile.ZipFile(file) as archive:
                    package = json.loads(archive.read('extension/package.json'))
                    assert package['version'] == version
                    assert (package['publisher']+'.'+package['name']).lower() == identifier.lower()
                break
            except Exception:
                if attempt == 2:
                    raise
                time.sleep(2*(attempt+1))
        records[identifier.lower()] = {'version':version, 'file':file.name,
            'sha256':hashlib.sha256(file.read_bytes()).hexdigest(), 'source':url}
        print(f'Cached {identifier} {version}', flush=True)
    (args.output/'index.json').write_text(json.dumps(records, indent=2)+'\n')


if __name__ == '__main__':
    main()
