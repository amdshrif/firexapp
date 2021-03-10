import os
import sys
import logging
from collections import OrderedDict

TASKS_DIRECTORY = "firex_tasks_directory"

logger = logging.getLogger(__name__)

_loaded_firex_bundles = None


def _get_paths_without_cwd():
    # This is needed because Celery temporarily adds the cwd into the sys.path via a context switcher,
    # and our discovery takes place inside that context.
    # Having cwd in the sys.path can slow down the discovery significantly without any benefit.
    paths = list(sys.path)
    try:
        paths.remove(os.getcwd())
    except ValueError:  # pragma: no cover
        pass
    return paths


#
# In case there are duplicate modules found, only keep one for each
#   (name, module_name, object_name) tuple. This prevents duplicate
#   arg registration failures when the sys.path causes the same service
#   to be found twice.
#
def prune_duplicate_module_entry_points(entry_points):
    id_to_entry_points = OrderedDict()

    for e in entry_points:
        key = (e.name, e.module_name, e.object_name)
        if key not in id_to_entry_points:
            id_to_entry_points[key] = e
        # Replace the currently stored entry point for this key if the distro is None.
        elif id_to_entry_points[key].distro is None and e.distro is not None:
            id_to_entry_points[key] = e

    return list(id_to_entry_points.values())


def _get_entrypoints(name, prune_duplicates=True) -> []:
    import entrypoints
    eps = [ep for ep in entrypoints.get_group_all(name)]
    if prune_duplicates:
        eps = prune_duplicate_module_entry_points(eps)
    return eps


def get_firex_bundles_entry_points():
    return _get_entrypoints('firex.bundles')


def loaded_firex_bundles_entry_points() -> {}:
    global _loaded_firex_bundles
    if _loaded_firex_bundles is None:
        _loaded_firex_bundles = {ep: ep.load() for ep in get_firex_bundles_entry_points()}
    return _loaded_firex_bundles


def get_firex_tracking_services_entry_points():
    return _get_entrypoints('firex_tracking_service')


def _get_firex_dependant_package_versions() -> {}:
    versions = dict()
    for ep, loaded_pkg in loaded_firex_bundles_entry_points().items():
        try:
            version = loaded_pkg.__version__
        except AttributeError:
            version = 'Unknown'
        versions[ep.name] = version
    return versions


def _get_firex_dependant_package_locations() -> []:
    return [p.__path__ for p in loaded_firex_bundles_entry_points.values()]


def discover_package_modules(current_path, root_path=None) -> []:
    if root_path is None:
        root_path = os.path.dirname(current_path)

    services = []
    if os.path.isfile(current_path):
        basename, ext = os.path.splitext(current_path)
        if ext.lower() == ".py" and not os.path.basename(current_path).startswith('_'):
            basename = basename.replace(root_path, "")
            return [basename.replace(os.path.sep, ".").strip(".")]
        else:
            return []
    elif os.path.isdir(current_path):
        base = os.path.basename(current_path)
        if "__pycache__" in base or base.startswith("."):
            return []
        for child_name in os.listdir(current_path):
            full_child = os.path.join(current_path, child_name)
            services += discover_package_modules(full_child, root_path)
        return services
    else:
        # either a symlink or a path that doesn't exist
        return []


def find_firex_task_bundles()->[]:
    # look for task modules in dependant packages
    bundles = []
    for location in _get_firex_dependant_package_locations():
        bundles += discover_package_modules(location)
    # look for task modules in env defined location
    if TASKS_DIRECTORY in os.environ:
        include_location = os.environ[TASKS_DIRECTORY]
        if os.path.isdir(include_location):
            if include_location not in sys.path:
                sys.path.append(include_location)
            include_tasks = discover_package_modules(include_location, root_path=include_location)
            bundles += include_tasks

    return bundles
