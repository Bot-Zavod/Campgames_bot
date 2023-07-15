from typing import Dict
from typing import List
from typing import Tuple

import tomli
import yaml


def read_poetry() -> Dict[str, str]:
    with open("pyproject.toml", "rb") as fp:
        pyproject = tomli.load(fp)

    dependencies: dict = pyproject["tool"]["poetry"]["dependencies"]
    # {
    #     'loguru': '^0.7.0',
    #     'poetry': '^1.5.1',
    #     'pydantic': '^1.10.9',
    #     'python': '^3.10',
    #     'python-dotenv': '^1.0.0',
    #     'python-telegram-bot': {'extras': ['rate-limiter'], 'version': '^20.3'}
    # }

    # filters keys
    for key in dependencies.keys():
        if isinstance(dependencies[key], dict):
            dependencies[key] = dependencies[key]["version"].replace("^", "")
        else:
            dependencies[key] = dependencies[key].replace("^", "")

    dependencies.pop("python")

    return dependencies


def read_pre_commit() -> Tuple[int, dict]:
    with open(".pre-commit-config.yaml") as fp:
        pre_commit: dict = yaml.full_load(fp)

    for index_m, hook in enumerate(pre_commit["repos"]):
        if "additional_dependencies" not in hook["hooks"][0]:
            continue
        if hook["hooks"][0]["id"] != "mypy":
            continue
        return index_m, hook
    else:
        raise Exception("Not found mypy in pre-commit")
    # {'hooks': [{'additional_dependencies': ['python-telegram-bot==20.3',
    #                                     'html5lib==1.1',
    #                                     'pytz==2022.5',
    #                                     'aiolimiter==1.0.0',
    #                                     'poetry==1.5.1',
    #                                     'pydantic==1.10.9',
    #                                     'python-dotenv==1.0.0',
    #                                     'loguru==0.7.0'],
    #         'args': ['--no-strict-optional'],
    #         'files': '^bot/.*\\.py$',
    #         'id': 'mypy',
    #         'language': 'python',
    #         'name': 'mypy',
    #         'require_serial': True,
    #         'types': ['python'],
    #         'verbose': True}],
    # 'repo': 'https://github.com/pre-commit/mirrors-mypy',
    # 'rev': 'v1.4.1'}


def design_pre_commit(pre_commit: dict) -> dict:
    hook_change = {}
    order = ["repo", "rev", "hooks"]
    for index, hook in enumerate(pre_commit["repos"]):
        # make dict in order standart mypy
        for reverse_hook in order:
            if hook.get(reverse_hook):
                hook_change[reverse_hook] = hook[reverse_hook]

            if reverse_hook != "hooks":
                continue
            # checking hooks only with "additional_dependencies"
            if not hook[reverse_hook][0].get("additional_dependencies"):
                continue

            reverse_dependencies = {}
            # change dependencies in reverse function
            for dependency in reversed(hook[reverse_hook][0]):
                reverse_dependencies[dependency] = hook[reverse_hook][0][dependency]

            hook[reverse_hook][0] = reverse_dependencies
            hook_change[reverse_hook] = hook[reverse_hook]
        # put change in file
        pre_commit["repos"][index] = hook_change
        hook_change = {}

    return pre_commit


def write_new_mypy(index_mypy: int, hook: list) -> None:
    with open(".pre-commit-config.yaml") as fp:
        pre_commit: dict = yaml.safe_load(fp)

    pre_commit["repos"][index_mypy] = hook

    pre_commit = design_pre_commit(pre_commit)

    with open(".pre-commit-config.yaml", "w") as fp:
        yaml.safe_dump(pre_commit, fp, sort_keys=False)


def change_mypy_versions(
    poetry_deps: Dict[str, str],
    dependencies_mypy: List[str],
    bad_packages: List[int],
    hook: dict,
) -> None:
    """deleted wrong versions mypy"""

    for i in reversed(bad_packages):
        dependencies_mypy.pop(i)
    # add dependencies from poetry
    for key, value in poetry_deps.items():
        dependencies_mypy.append(f"{key}=={value}")
        print(f"- add {key}=={value}")

    hook["hooks"][0]["additional_dependencies"] = dependencies_mypy


def compare_versions() -> bool:
    poetry_deps = read_poetry()
    index_mypy, hook = read_pre_commit()

    bad_packages = []
    dependencies_mypy = hook["hooks"][0]["additional_dependencies"]
    # checking versions from poetry to mypy
    for index, library in enumerate(dependencies_mypy):
        values: list = library.split("==")
        if package := poetry_deps.get(values[0]):
            if values[1] == package:
                poetry_deps.pop(values[0])
            else:
                bad_packages.append(index)

    if poetry_deps:
        change_mypy_versions(poetry_deps, dependencies_mypy, bad_packages, hook)
        write_new_mypy(index_mypy, hook)
        return False
    return True


if __name__ == "__main__":
    compare_versions()
