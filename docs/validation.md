# Validation record

The initial implementation is checked with real local HTTP integration tests.
Docker builds, Trivy scans, Kubernetes rollout, GHCR publishing and Argo CD sync
must be verified in environments with those runtimes and access. Workflow files
are configuration, not proof of a successful hosted run. Record links to actual
runs and commands here after execution; do not replace missing results with claims.

## Suggested first demonstration

Run the service, show health/readiness, run tests, inspect container security
settings, run CI on GitHub, then deploy to kind. Capture observed timings and
failures. Use a dedicated sandbox and synthetic data.
