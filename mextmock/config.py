from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="MPT",
    root_path="../.",
    settings_files=["settings.yaml", ".secrets.yaml"],
)
