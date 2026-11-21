"""playbook checklist 校验器：验收口径是 fail-closed 的。

一个 playbook 步骤「做过了」的唯一凭证是字节：evidence_path 指向的文件存在，
或 evidence_cite 里登记了外部仓库的路径与日期。口头声明、空串、指向不存在文件的
证据一律不算数——这与 ttftkit invariance 闸的「缺 outputs ≠ 通过」同一纪律。
"""
from __future__ import annotations

import pathlib

import yaml

REQUIRED_STEP_FIELDS = ("id", "title")


def _config_error(reasons: list[str], msg: str) -> dict:
    reasons.append(msg)
    return {"exit_code": 2, "reasons": reasons, "total": 0, "done": 0, "steps": []}


def validate(path: str) -> dict:
    """校验一份 checklist YAML，返回 {exit_code, reasons, total, done, steps}。

    退出码：0=全部完成且证据齐全；1=有步骤未做或证据缺失；2=结构畸形/文件不存在。
    """
    reasons: list[str] = []
    p = pathlib.Path(path)
    if not p.is_file():
        return _config_error(reasons, f"checklist file not found: {path}")
    try:
        doc = yaml.safe_load(p.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        return _config_error(reasons, f"invalid YAML: {exc}")
    if not isinstance(doc, dict):
        return _config_error(reasons, "checklist must be a mapping")
    steps = doc.get("steps")
    if not isinstance(steps, list) or not steps:
        return _config_error(reasons, "steps must be a non-empty list")

    seen_ids: set[str] = set()
    parsed: list[dict] = []
    for raw in steps:
        if not isinstance(raw, dict):
            return _config_error(reasons, f"step must be a mapping: {raw!r}")
        for field in REQUIRED_STEP_FIELDS:
            if not raw.get(field):
                return _config_error(reasons, f"step missing required field {field!r}: {raw!r}")
        sid = str(raw["id"])
        if sid in seen_ids:
            return _config_error(reasons, f"duplicate step id: {sid}")
        seen_ids.add(sid)

        evidence_path = raw.get("evidence_path")
        evidence_cite = raw.get("evidence_cite")
        if evidence_path is None and evidence_cite is None:
            return _config_error(
                reasons,
                f"step {sid} has no evidence (need evidence_path or evidence_cite)",
            )
        parsed.append({
            "id": sid,
            "title": str(raw["title"]),
            "done": bool(raw.get("done", False)),
            "evidence_path": evidence_path,
            "evidence_cite": evidence_cite,
        })

    out_steps: list[dict] = []
    for step in parsed:
        if step["evidence_path"] is not None:
            if not pathlib.Path(step["evidence_path"]).is_file():
                # 登记了证据路径但文件不在：这不是通过，是断了的证据链
                reasons.append(f"step {step['id']}: evidence file missing: {step['evidence_path']}")
                out_steps.append({**step, "status": "BROKEN_EVIDENCE"})
                continue
            status = "DONE" if step["done"] else "EVIDENCE_READY"
        elif isinstance(step["evidence_cite"], str) and step["evidence_cite"].strip():
            status = "DONE" if step["done"] else "EVIDENCE_READY"
        else:
            return _config_error(reasons, f"step {step['id']}: evidence_cite is empty")
        out_steps.append({**step, "status": status})

    done = sum(1 for s in out_steps if s["status"] == "DONE")
    if done < len(out_steps):
        remaining = [s["id"] for s in out_steps if s["status"] != "DONE"]
        reasons.append(f"remaining steps: {', '.join(remaining)}")
        exit_code = 1
    else:
        exit_code = 0
    return {"exit_code": exit_code, "reasons": reasons,
            "total": len(out_steps), "done": done, "steps": out_steps}
