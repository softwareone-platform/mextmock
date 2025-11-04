#!/usr/bin/env bash
set -euo pipefail

# Determine the script directory and helm chart directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HELM_CHART_DIR="${SCRIPT_DIR}/helm"

# Validate helm chart directory exists
if [[ ! -d "$HELM_CHART_DIR" ]]; then
    echo "Error: Helm chart directory not found at: $HELM_CHART_DIR"
    echo "Expected to find Chart.yaml and templates/ directory"
    exit 1
fi

# Function to validate extension ID format
validate_extension_id() {
    local extension_id="$1"
    # Pattern: EXT-\d{4}-\d{4} (case insensitive)
    if [[ ! "$extension_id" =~ ^[Ee][Xx][Tt]-[0-9]{4}-[0-9]{4}$ ]]; then
        echo "Error: Invalid extension ID format: $extension_id"
        echo "Expected format: EXT-NNNN-NNNN (where N is a digit)"
        echo "Example: EXT-1234-5678"
        exit 1
    fi
}

# Function to validate replicas count
validate_replicas() {
    local replicas="$1"
    if [[ ! "$replicas" =~ ^[1-9][0-9]*$ ]]; then
        echo "Error: Invalid replicas count: $replicas"
        echo "Expected: positive integer (1, 2, 3, ...)"
        exit 1
    fi
}

usage() {
    echo ""
    echo "Usage:"
    echo "  $0 install <extension_id> <api_key> [--environment <env>] [--namespace <ns>|-n <ns>] [--replicas <count>] [--app-version <version>] [--dry-run]"
    echo "  $0 upgrade <extension_id> <api_key> [--environment <env>] [--namespace <ns>|-n <ns>] [--replicas <count>] [--app-version <version>] [--dry-run]"
    echo "  $0 template <extension_id> [<api_key>] [--environment <env>] [--namespace <ns>|-n <ns>] [--replicas <count>] [--app-version <version>]"
    echo
    echo "Notes and defaults:" 
    echo "  <extension_id>  : must follow format EXT-NNNN-NNNN (case-insensitive). Example: EXT-1234-5678"
    echo "  <env>           : dev, test, stage, prod (default: dev)"
    echo "  <ns>            : Kubernetes namespace (default: mpt-extensions). Short alias: -n"
    echo "  <count>         : positive integer replicas (default: 1)"
    echo "  --dry-run       : Show commands and rendered templates without executing"
    echo "  --app-version   : Override the image tag. If not provided, the script will try to use the latest git tag in the script's repo (or fail if none found)."
    echo "  template        : Only render and display the Helm templates (api_key optional; defaults to 'default-api-key')"
    echo ""
    exit 1
}


# Resolve the app version (image tag) to use.
# If --app-version is not provided, attempt to use the latest git tag from the script's repo.
resolve_app_version() {
    if [[ -n "${app_version:-}" ]]; then
        echo "Using app version (from flag): ${app_version}"
        return 0
    fi

    if [[ -d "${SCRIPT_DIR}/.git" ]]; then
        app_version="$(git -C "${SCRIPT_DIR}" describe --tags --abbrev=0 2>/dev/null || true)"
        if [[ -z "${app_version}" ]]; then
            echo "Error: no git tags found in ${SCRIPT_DIR}. Please provide --app-version." >&2
            exit 1
        fi
        echo "Using app version (from git tag): ${app_version}"
    else
        echo "Error: .git folder not found in ${SCRIPT_DIR}. --app-version is required." >&2
        exit 1
    fi
}

if [[ $# -lt 2 ]]; then
    usage
fi

command=$1
shift

environment="dev"
namespace="mpt-extensions"
replicas=1
dry_run=false
app_version=""
args=()

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --environment)
            environment="$2"
            shift 2
            ;;
        --namespace|-n)
            namespace="$2"
            shift 2
            ;;
        --replicas)
            replicas="$2"
            shift 2
            ;;
        --dry-run)
            dry_run=true
            shift
            ;;
        --app-version)
            app_version="$2"
            shift 2
            ;;
        *)
            args+=("$1")
            shift
            ;;
    esac
done

# Map environment to domain
case "$environment" in
    dev) domain="s1.today" ;;
    test) domain="s1.show" ;;
    stage) domain="s1.live" ;;
    prod) domain="platform.softwareone.com" ;;
    *)
        echo "Error: invalid environment '$environment'. Must be one of: dev, test, stage, prod."
        exit 1
        ;;
esac

if [[ "$command" == "install" ]]; then
    if [[ ${#args[@]} -lt 2 ]]; then
        echo "Error: install requires <extension_id> and <api_key>"
        usage
    fi
    extension_id="${args[0]}"
    api_key="${args[1]}"

    # Validate extension ID format
    validate_extension_id "$extension_id"
    
    # Validate replicas count
    validate_replicas "$replicas"

    # Convert extension_id to lowercase and replace underscores with hyphens for release name
    release_name="mextmock-$(echo "${extension_id}" | tr '[:upper:]' '[:lower:]' | sed 's/_/-/g')"

    # Resolve the app version (image tag) to use (may exit if resolution fails)
    resolve_app_version

    helm_command="helm install \"${release_name}\" \"${HELM_CHART_DIR}\" \
        --namespace \"${namespace}\" \
        --set extensionId=\"${extension_id}\" \
        --set extensionApiKey=\"${api_key}\" \
        --set replicaCount=\"${replicas}\" \
        --set envDomain=\"${domain}\" \
        --set image.tag=\"${app_version}\""


    if [[ "$dry_run" == "true" ]]; then
        echo "=== DRY RUN MODE ==="
        echo "Command that would be executed:"
        echo "$helm_command"
        echo
        echo "=== RENDERED TEMPLATES ==="
        helm template "${release_name}" "${HELM_CHART_DIR}" \
            --namespace "${namespace}" \
            --set extensionId="${extension_id}" \
            --set extensionApiKey="${api_key}" \
            --set replicaCount="${replicas}" \
            --set envDomain="${domain}" \
            --set image.tag="${app_version}"
    else
        echo "Installing Helm release: ${release_name} (env: ${environment}, domain: ${domain})"
        eval "$helm_command"
    fi

elif [[ "$command" == "upgrade" ]]; then
    if [[ ${#args[@]} -lt 2 ]]; then
        echo "Error: upgrade requires <extension_id> and <api_key>"
        usage
    fi
    extension_id="${args[0]}"
    api_key="${args[1]}"
    
    # Validate extension ID format
    validate_extension_id "$extension_id"
    
    # Validate replicas count
    validate_replicas "$replicas"
    
    # Convert extension_id to lowercase and replace underscores with hyphens for release name
    release_name="mextmock-$(echo "${extension_id}" | tr '[:upper:]' '[:lower:]' | sed 's/_/-/g')"

    # Resolve the app version (image tag) to use (may exit if resolution fails)
    resolve_app_version

    # extensionApiKey is required for upgrade: always pass it to Helm
    helm_command="helm upgrade \"${release_name}\" \"${HELM_CHART_DIR}\" \
        --namespace \"${namespace}\" \
        --set extensionId=\"${extension_id}\" \
        --set extensionApiKey=\"${api_key}\" \
        --set replicaCount=\"${replicas}\" \
        --set envDomain=\"${domain}\" \
        --set image.tag=\"${app_version}\" \
        --install"

    if [[ "$dry_run" == "true" ]]; then
        echo "=== DRY RUN MODE ==="
        echo "Command that would be executed:"
        echo "$helm_command"
        echo
        echo "=== RENDERED TEMPLATES ==="
        # For template mode, pass extensionApiKey (required for upgrade)
        helm template "${release_name}" "${HELM_CHART_DIR}" \
            --namespace "${namespace}" \
            --set extensionId="${extension_id}" \
            --set extensionApiKey="${api_key}" \
            --set replicaCount="${replicas}" \
            --set envDomain="${domain}" \
            --set image.tag="${app_version}"
    else
        echo "Upgrading Helm release: ${release_name} (env: ${environment}, domain: ${domain})"
        eval "$helm_command"
    fi

elif [[ "$command" == "template" ]]; then
    if [[ ${#args[@]} -lt 1 ]]; then
        echo "Error: template requires <extension_id>"
        usage
    fi
    extension_id="${args[0]}"
    api_key="${args[1]:-default-api-key}"
    
    # Validate extension ID format
    validate_extension_id "$extension_id"
    
    # Validate replicas count
    validate_replicas "$replicas"
    
    # Convert extension_id to lowercase and replace underscores with hyphens for release name
    release_name="mextmock-$(echo "${extension_id}" | tr '[:upper:]' '[:lower:]' | sed 's/_/-/g')"
    # Resolve app version (image tag)
    resolve_app_version
    echo "=== RENDERING TEMPLATES ==="
    echo "Extension ID: ${extension_id}"
    echo "Environment: ${environment}"
    echo "Domain: ${domain}"
    echo "Namespace: ${namespace}"
    echo "Replicas: ${replicas}"
    echo "Helm Chart Dir: ${HELM_CHART_DIR}"
    echo
    helm template "${release_name}" "${HELM_CHART_DIR}" \
        --namespace "${namespace}" \
        --set extensionId="${extension_id}" \
        --set extensionApiKey="${api_key}" \
        --set replicaCount="${replicas}" \
        --set envDomain="${domain}" \
        --set image.tag="${app_version}"

else
    echo "Error: unknown command '${command}'"
    usage
fi
