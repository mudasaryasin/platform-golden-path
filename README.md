# Platform Golden Path

A small, inspectable reference for taking a Python HTTP service through tests,
container building, vulnerability scanning and a reviewed Kubernetes deployment.
Maintainer: Mudasar Yasin. Status: initial implementation (0.1.0).

## Problem

Small teams repeatedly assemble the same delivery steps. This repository offers
one understandable path with visible safety gates and explicit operational limits.
It is a demonstration, not evidence of production adoption or measured savings.

## Run locally (Python 3.12+)

```bash
python -m unittest discover -s tests -v
python -m app.server
# In a second terminal:
curl http://localhost:8080/healthz
curl http://localhost:8080/readyz
```

## Container and local Kubernetes

Requires Docker, kind and kubectl, installed separately.

```bash
docker build -t golden-path:dev .
docker run --rm -p 8080:8080 golden-path:dev
# Stop the container before continuing if you need the same local port.
kind create cluster --name golden-path
kind load docker-image golden-path:dev --name golden-path
kubectl apply -f deploy/kubernetes.yaml
kubectl rollout status deployment/golden-path --timeout=120s
kubectl port-forward service/golden-path 8080:80
# Cleanup when finished:
# kind delete cluster --name golden-path
```

## CI, publishing and GitOps

`ci.yml` runs HTTP integration tests, builds the container and rejects fixable
HIGH/CRITICAL vulnerabilities. Unfixed vulnerabilities remain visible but do not
block this example; review that policy before production use.
`publish.yml` is manually triggered and repeats tests and scanning before pushing
a commit-SHA-tagged image to GHCR. Configure GitHub Packages access as needed.

For Argo CD, first replace `REPLACE_OWNER` in its Application and replace the local
image in `deploy/kubernetes.yaml` with your published SHA tag or immutable digest.
Install Argo CD separately; then apply `deploy/argocd/application.yaml`.
Sync is manual. CI does not mutate a live cluster or update image references.
Private GHCR images require separately configured pull credentials.

## Architecture and decisions

HTTP service → tests → container → scan → registry → reviewed manifest → Argo CD.
The service has no database, authentication or model dependencies; readiness only
means this stateless example can answer requests. Containers run without root,
with a read-only root filesystem and bounded CPU/memory. No public ingress is
created. This starter omits TLS termination, external secrets, network policies,
autoscaling, alerting and a rollback exercise. Add them for your actual environment.

## Validate the security example

The companion `ai-platform-readiness` repository can inspect
`deploy/kubernetes.yaml`. Its insecure fixture demonstrates policy failures.
The CI image scanner and manifest checks address different risks.

## Roadmap and measurement

1. Run container, kind and Argo CD validation on a real development machine.
2. Record setup time, CI duration and manual steps with environment and date.
3. Add manifest policy checks, telemetry, a rollback drill and independent review.

No performance improvement or adoption figures are claimed yet. See
[docs/validation.md](docs/validation.md) for the verification boundary.
