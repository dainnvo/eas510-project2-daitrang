"""Download the official pinned ESConv release with integrity verification."""
from datetime import datetime, timezone
import hashlib
from pathlib import Path
import sys
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import config
from src.data import save_json


def main():
    files = []
    for name, expected in config.SOURCE_SHA256.items():
        url = f"https://raw.githubusercontent.com/thu-coai/Emotional-Support-Conversation/{config.SOURCE_COMMIT}/{name}"
        destination = ROOT / "data" / ("raw" if name == "ESConv.json" else "source") / name
        if destination.exists() and hashlib.sha256(destination.read_bytes()).hexdigest() == expected:
            print(f"Already verified: {name}")
        else:
            request = urllib.request.Request(url, headers={"User-Agent": "EAS510-academic-project"})
            content = urllib.request.urlopen(request, timeout=120).read()
            if hashlib.sha256(content).hexdigest() != expected:
                raise ValueError(f"Checksum mismatch: {name}")
            destination.parent.mkdir(parents=True, exist_ok=True)
            temporary = destination.with_suffix(destination.suffix + ".tmp")
            temporary.write_bytes(content)
            temporary.replace(destination)
            print(f"Downloaded and verified: {name}")
        files.append({"name": name, "url": url, "sha256": expected})
    save_json(ROOT / "data/source/acquisition.json", {
        "verified_at_utc": datetime.now(timezone.utc).isoformat(),
        "repository": config.SOURCE_REPOSITORY, "commit": config.SOURCE_COMMIT, "files": files,
        "note": "Timestamp is last local verification; immutable commit and hashes identify the data."})


if __name__ == "__main__":
    main()
