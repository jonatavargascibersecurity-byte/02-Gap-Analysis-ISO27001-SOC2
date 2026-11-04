"""Guard the explicit links to real platform content.

The repository must point to the actual room/course/module, not to a platform
home page. These tests fail if a link is removed or replaced by a generic URL.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PLATFORM_URLS = [
    "https://tryhackme.com/room/cybergovernanceregulation",
    "https://tryhackme.com/room/seriskmanagement",
    "https://app.letsdefend.io/training/lessons/risk-management",
    "https://academy.hackthebox.com/course/preview/security-audit-and-testing",
    "https://academy.hackthebox.com/course/preview/information-security-guidelines",
]


def test_readme_references_real_platform_content():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for url in PLATFORM_URLS:
        assert url in readme


def test_platforms_mapping_links_content_to_artefacts():
    doc = (ROOT / "PLATFORMS.md").read_text(encoding="utf-8")
    for url in PLATFORM_URLS:
        assert url in doc
    for artefact in ("build/SoA.md", "build/remediation-plan.md", "build/framework-crosswalk.md"):
        assert artefact in doc
