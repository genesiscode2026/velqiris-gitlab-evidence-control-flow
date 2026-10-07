# VELQIRIS Evidence-Control Flow for GitLab Duo

A Bring Your Own project for the GitLab Transcend **Life After Code** hackathon. It combines a deterministic CI invariant auditor with a GitLab Duo custom-flow configuration that reviews changes for unsupported deployment, testing, commercial and settlement claims.

## What is new in the submission window

- GitLab Duo flow configuration under `.gitlab/duo/flows/`.
- Project-level `AGENTS.md` context for fail-closed evidence handling.
- CI artifact production and downstream artifact validation.
- Real CI base/head requirement; the auditor does not substitute a sample diff.

## Local verification

```bash
python3 -m unittest -v test_agentic_flow.py
```

The local auditor and CI pipeline are deterministic. A real Duo run and public pipeline URL must be captured after GitLab contributor provisioning; this README does not claim they already exist.

## License

MIT.
