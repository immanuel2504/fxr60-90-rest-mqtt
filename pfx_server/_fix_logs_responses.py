#!/usr/bin/env python3
"""Replace the truncated `binary` placeholders with the real captured responses.

The log GETs return {"binary": "<base64 gzip tar>", "filename": "..."}. Earlier
these were stored with the base64 elided, which makes the capture unverifiable.
This stores:

  response body/response.json          the FULL response, verbatim as received
  response body/decoded/<member>       every file inside the archive, extracted
  response body/decoded/MANIFEST.txt   member list with sizes

so the evidence is both byte-exact and directly readable.
"""
import base64
import io
import json
import os
import shutil
import tarfile

REST = "/home/altautoadmin/pfx_server/rest"

# folder -> captured response file
CAPTURES = [
    ("cloud-logs-syslog-GET/01-retrieve-SUCCESS", "/tmp/logbase/syslog.out"),
    ("cloud-logs-RcLog-GET/01-retrieve-SUCCESS", "/tmp/logbase/RcLog.out"),
    ("cloud-logs-RgWarningLog-GET/01-retrieve-SUCCESS", "/tmp/logbase/RgWarningLog.out"),
    ("cloud-logs-RgErrorLog-GET/01-retrieve-SUCCESS", "/tmp/logbase/RgErrorLog.out"),
    ("cloud-logs-radioPacketLog-GET/01-retrieve-SUCCESS", "/tmp/logbase/radioPacketLog.out"),
    ("cloud-logs-radioPacketLog-GET/03-repopulates-after-enable", "/tmp/_p3"),
]

# extract members only when the archive is small enough to be useful in-repo.
# packet logs are 1 MiB each x4 and radio_control.log.N are ~5 MB each.
MAX_MEMBER = 200_000
MAX_TOTAL = 400_000


def main():
    for folder, cap in CAPTURES:
        d = os.path.join(REST, folder, "response body")
        if not os.path.isdir(d):
            print("skip (no folder):", folder)
            continue
        raw_text = open(cap).read()
        doc = json.loads(raw_text)

        # 1. the full response, verbatim
        with open(os.path.join(d, "response.json"), "w") as fh:
            fh.write(raw_text if raw_text.endswith("\n") else raw_text + "\n")

        # 2. decode and extract
        dec = os.path.join(d, "decoded")
        shutil.rmtree(dec, ignore_errors=True)
        os.makedirs(dec, exist_ok=True)

        blob = base64.b64decode(doc["binary"])
        open(os.path.join(dec, doc["filename"]), "wb").write(blob)

        is_gzip = "valid" if blob[:2] == b"\x1f\x8b" else "INVALID"
        lines = [
            f"Archive:  {doc['filename']}",
            f"Response: {len(raw_text)} bytes of JSON",
            f"base64:   {len(doc['binary'])} chars -> {len(blob)} bytes gzip",
            f"gzip magic: {blob[:2].hex()}  ({is_gzip})",
            "",
            "Members:",
        ]
        total = 0
        with tarfile.open(fileobj=io.BytesIO(blob), mode="r:gz") as t:
            members = t.getmembers()
            for m in members:
                lines.append(f"  {m.name}  {m.size} bytes")
            for m in members:
                if m.size <= MAX_MEMBER and total + m.size <= MAX_TOTAL:
                    data = t.extractfile(m).read()
                    safe = m.name.replace("/", "_")
                    open(os.path.join(dec, safe), "wb").write(data)
                    total += m.size
                else:
                    lines.append(f"  (not extracted: {m.name} is {m.size} bytes - "
                                 f"exceeds the {MAX_MEMBER}-byte in-repo limit; "
                                 f"extract it from {doc['filename']} above)")
        lines += [
            "",
            f"{len(members)} member(s). Files small enough to keep are extracted",
            "alongside this manifest; the .tar.gz holds all of them.",
            "",
            "Re-extract everything with:",
            f"  tar xzf {doc['filename']}",
        ]
        open(os.path.join(dec, "MANIFEST.txt"), "w").write("\n".join(lines) + "\n")
        print(f"{folder}: full response + {len(members)} members "
              f"({total} bytes extracted)")


if __name__ == "__main__":
    main()
