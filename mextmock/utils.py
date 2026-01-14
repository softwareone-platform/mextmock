import functools
import logging
import subprocess
import uuid
from dataclasses import dataclass
from typing import Annotated

import jwt
from fastapi import Header

logger = logging.getLogger(__name__)

ACCOUNT_ID_KEY = "https://claims.softwareone.com/accountId"
EXTENSION_ID_KEY = "https://claims.softwareone.com/extensionId"
SERVICE_ID_KEY = "https://claims.softwareone.com/serviceId"
INSTALLATION_ID_KEY = "https://claims.softwareone.com/installationId"
PARAM_PHASE_ORDERING = "ordering"
PARAM_PHASE_FULFILLMENT = "fulfillment"

@dataclass
class AuthContext:
    account_id: str
    extension_id: str
    installation_id: str
    service_id :str


def _validate_auth_context(auth_context:Annotated[str | None,
Header(alias="Authorization")] = None):
    if auth_context is None:
        return None
    try:
        scheme, token = auth_context.split()
    except ValueError:
        return None
    if scheme != "Bearer" or token is None:
        return None
    try:
        payload = jwt.decode(
            token,
            algorithms=["RS256"],
            options={"verify_signature": False},
        )
    except jwt.PyJWTError:
        # todo add logging
        return None

    return payload




def get_auth_context(auth_context: Annotated[str | None, Header(alias="Authorization")] = None):
    jwt_payload = _validate_auth_context(auth_context)
    if jwt_payload is None:
        return None

    try:
        return AuthContext(
                account_id=jwt_payload[ACCOUNT_ID_KEY],
                extension_id=jwt_payload[EXTENSION_ID_KEY],
                installation_id=jwt_payload[INSTALLATION_ID_KEY],
                service_id=jwt_payload[SERVICE_ID_KEY],
            )
    except KeyError:
        return None


def get_instance_external_id():
    result = subprocess.run(
        ['cat', '/proc/1/cpuset'],
        capture_output=True,
        stdin=subprocess.DEVNULL,
        start_new_session=True,
    )
    try:
        result.check_returncode()
    except subprocess.CalledProcessError:
        return f"{uuid.getnode():012x}"

    _, container_id = result.stdout.decode()[:-1].rsplit('/', 1)
    if len(container_id) == 64:
        return container_id

    result = subprocess.run(
        ['grep', 'overlay', '/proc/self/mountinfo'],
        capture_output=True,
        stdin=subprocess.DEVNULL,
        start_new_session=True,
    )
    try:
        result.check_returncode()
        mount = result.stdout.decode()
        start_idx = mount.index('upperdir=') + len('upperdir=')
        end_idx = mount.index(',', start_idx)
        dir_path = mount[start_idx:end_idx]
        _, container_id, _ = dir_path.rsplit('/', 2)
        if len(container_id) != 64:
            return f"{uuid.getnode():012x}"
        return container_id
    except (subprocess.CalledProcessError, ValueError):
        return f"{uuid.getnode():012x}"


def find_first(func, iterable, default=None):
    return next(filter(func, iterable), default)

def get_parameter(parameter_phase, source, param_external_id):
    """
    Returns a parameter of a given phase by its external identifier.
    Returns an empty dictionary if the parameter is not found.
    Args:
        parameter_phase (str): The phase of the parameter (ordering, fulfillment).
        source : The source business object from which the parameter
        should be extracted.
        param_external_id (str): The unique external identifier of the parameter.

    Returns:
        dict: The parameter object or an empty dictionary if not found.
    """
    logger.debug("Order Parameters %s %s",param_external_id,source['parameters'][parameter_phase])
    return find_first(
        lambda x: x.get("externalId") == param_external_id,
        source["parameters"][parameter_phase],
        default={},
    )


get_ordering_parameter = functools.partial(get_parameter, PARAM_PHASE_ORDERING)

