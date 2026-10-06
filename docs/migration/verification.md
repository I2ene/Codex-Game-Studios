# Framework validation procedure

Use Python 3.11+ with `requirements.txt` in a local environment. Run these commands
from the framework checkout, keeping any captured output outside tracked files:

```text
python tools/validate.py
python -m unittest discover -s tests -v
python tools/integration_sample.py
```

After changing reviewed managed payload, run `python tools/build_release.py`, then
validate again. Release hashes describe the current payload; they are not a signature
or proof of game quality. The integration sample prints JSON to stdout and creates
its consumer in a temporary directory; it does not publish an archived result.

The reusable counter source and acceptance cases live in `fixtures/minimal-counter/`.
The framework's regression tests live in `tests/`. Preserve these sources when
cleaning generated reports and fixture output.

## Evidence levels

- **FORMAT:** native metadata, links, source inventory and release structure checks.
- **EXECUTED:** the exact command, checkout and observed result of a helper or
  synthetic consumer exercise. A synthetic sample is a framework check.
- **NOT ASSESSED:** any required check not actually run or supported by observed data.

Optional `tools/integration_sample.py --native-discovery` uses the available Codex
CLI for read-only installed-skill and hook-API discovery. It does not prove skill
inference, custom-role launch or trusted callback delivery. Record unavailable
capabilities as unassessed; never change global configuration or trust to obtain a pass.

Actual game design, balance, visuals, accessibility, performance, playtests, engine
builds, platform certification, deployment and live operations require consumer data
and their applicable professional workflows. Missing inputs and empty scans are not
clean passes. Parent assessments and actual independent participants remain distinct.

See [architecture](architecture.md), [capabilities](capabilities.md),
[automation mapping](automation.md) and [platform references](platform-evidence.md).
