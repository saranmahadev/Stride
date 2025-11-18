"""
Tests for the enhanced SprintManager.
"""
import shutil
import tempfile
from pathlib import Path
import pytest

from stride.core.folder_manager import FolderManager, SprintStatus
from stride.core.sprint_manager import SprintManager


@pytest.fixture
def temp_project():
    tmp = Path(tempfile.mkdtemp())
    yield tmp
    shutil.rmtree(tmp)


def test_create_and_get_metadata(temp_project: Path):
    fm = FolderManager(temp_project)
    fm.ensure_structure()
    sm = SprintManager(folder_manager=fm)

    sprint_id = "SPRINT-TST1"
    sprint_path = sm.create_sprint(
        sprint_id=sprint_id,
        title="Test Sprint",
        description="A test sprint",
        author="tester@example.com",
        status=SprintStatus.PROPOSED,
    )

    assert sprint_path.exists()
    proposal = sprint_path / "proposal.md"
    assert proposal.exists()

    meta = sm.get_sprint_metadata(sprint_id)
    assert isinstance(meta, dict)
    assert meta.get("id") == sprint_id
    assert meta.get("title") == "Test Sprint"
    assert meta.get("status") == SprintStatus.PROPOSED.value


def test_move_sprint_status(temp_project: Path):
    fm = FolderManager(temp_project)
    fm.ensure_structure()
    sm = SprintManager(folder_manager=fm)

    sprint_id = "SPRINT-MOVE1"
    sm.create_sprint(sprint_id=sprint_id, title="Move", description="move test", author="a@x.com")

    # move to active
    ok = sm.move_sprint_status(sprint_id, SprintStatus.ACTIVE)
    assert ok is True
    assert fm.get_sprint_path(sprint_id, SprintStatus.ACTIVE).exists()
    assert not fm.get_sprint_path(sprint_id, SprintStatus.PROPOSED).exists()


def test_update_sprint_metadata(temp_project: Path):
    fm = FolderManager(temp_project)
    fm.ensure_structure()
    sm = SprintManager(folder_manager=fm)

    sprint_id = "SPRINT-META1"
    sm.create_sprint(sprint_id=sprint_id, title="Meta", description="meta test", author="meta@x.com")

    updated = sm.update_sprint_metadata(sprint_id, {"assignee": "alice@example.com"})
    assert updated is True

    meta = sm.get_sprint_metadata(sprint_id)
    assert meta.get("assignee") == "alice@example.com"


def test_list_all_sprints(temp_project: Path):
    fm = FolderManager(temp_project)
    fm.ensure_structure()
    sm = SprintManager(folder_manager=fm)

    s1 = "SPRINT-LST1"
    s2 = "SPRINT-LST2"
    sm.create_sprint(sprint_id=s1, title="One", description="one", author="a@x.com")
    sm.create_sprint(sprint_id=s2, title="Two", description="two", author="b@x.com")

    # move one to active
    sm.move_sprint_status(s1, SprintStatus.ACTIVE)

    all_sprints = sm.list_all_sprints()
    ids = {s["id"] for s in all_sprints}
    assert s1 in ids and s2 in ids


def test_validate_sprint_detects_missing_proposal(temp_project: Path):
    fm = FolderManager(temp_project)
    fm.ensure_structure()
    sm = SprintManager(folder_manager=fm)

    sprint_id = "SPRINT-VAL1"
    sm.create_sprint(sprint_id=sprint_id, title="Val", description="val", author="v@x.com")

    sprint_path = fm.get_sprint_path(sprint_id, SprintStatus.PROPOSED)
    proposal = sprint_path / "proposal.md"
    # remove proposal to simulate corruption
    proposal.unlink()

    ok, errors = sm.validate_sprint(sprint_id)
    assert ok is False
    assert any("proposal" in e.lower() or "missing" in e.lower() for e in errors)
