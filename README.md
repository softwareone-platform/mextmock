# mextmock

## Description

This project is a mock of an extension for the Marketplace platform.

This mock only subscribes to platform events related to the **Order** business object. It provides a filter to only receive events when the attribute status of the order is `Processing`.
It just acknowledges the event and dumps the event data to stdout.


## Deployment

This project can be deployed to Kubernetes using the provided `deploy-mextmock.sh` script, which manages Helm deployments with environment-specific configurations.

### Prerequisites

- Helm 3.x installed
- Access to a Kubernetes cluster
- Valid extension ID in format `EXT-NNNN-NNNN` (case insensitive)

### Usage

```bash
# Install a new extension
./deploy-mextmock.sh install <extension_id> <api_key> [options]

# Upgrade an existing extension
./deploy-mextmock.sh upgrade <extension_id> [options]
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--environment <env>` | Target environment (dev, test, stage, prod) | `dev` |
| `--namespace <ns>` or `-n <ns>` | Kubernetes namespace | `mpt-extensions` |
| `--replicas <count>` | Number of pod replicas | `1` |
| `--dry-run` | Show commands and templates without executing | - |
