"""playbook checklist 校验器：TDD RED→GREEN。

口径（fail-closed）：
- 每步必须有唯一 id、非空标题，以及证据（evidence_path 或 evidence_cite，二选一）。
- evidence_path 指向的文件必须真实存在——「我做过」不是证据，字节才是。
- done=true 但缺证据 / 证据文件缺失 → 判 FAIL（exit 1），绝不静默通过。
- 结构畸形（缺字段、id 重复）→ 配置错误（exit 2）。
- 全部步骤 done 且证据齐全 → exit 0；有步骤未做 → exit 1 并列出剩余步骤。
"""
import textwrap

import pytest

from privatellm.checklist import validate


def _write(tmp_path, text):
    f = tmp_path / "checklist.yaml"
    f.write_text(textwrap.dedent(text), encoding="utf-8")
    return str(f)


GOOD = """
    title: 单卡 vLLM 私有化部署
    steps:
      - id: s1
        title: 环境就绪
        done: true
        evidence_cite: "vllm-serving-card/results/environment.txt (2026-11-09)"
      - id: s2
        title: 压测完成
        done: true
        evidence_path: "{{EVID}}"
"""


def test全done证据齐_exit0(tmp_path):
    evid = tmp_path / "card.json"
    evid.write_text("{}", encoding="utf-8")
    path = _write(tmp_path, GOOD.replace("{{EVID}}", str(evid)))
    r = validate(path)
    assert r["exit_code"] == 0, r["reasons"]


def test步骤未做_exit1并列出剩余(tmp_path):
    evid = tmp_path / "card.json"
    evid.write_text("{}", encoding="utf-8")
    text = GOOD.replace("{{EVID}}", str(evid)).replace("done: true\n        evidence_path", "done: false\n        evidence_path")
    r = validate(_write(tmp_path, text))
    assert r["exit_code"] == 1
    assert any("s2" in reason for reason in r["reasons"])


def testdone但证据文件不存在_不是通过(tmp_path):
    text = GOOD.replace("{{EVID}}", str(tmp_path / "不存在的文件.json"))
    r = validate(_write(tmp_path, text))
    assert r["exit_code"] == 1
    assert any("evidence" in reason.lower() or "证据" in reason for reason in r["reasons"])


def testdone但缺证据字段_配置错误(tmp_path):
    text = GOOD.replace("{{EVID}}", str(tmp_path / "x.json")).replace(
        "        evidence_path: \"" + str(tmp_path / "x.json") + "\"\n", "")
    r = validate(_write(tmp_path, text))
    assert r["exit_code"] == 2
    assert any("s2" in reason for reason in r["reasons"])


def testid重复_配置错误(tmp_path):
    text = GOOD.replace("{{EVID}}", str(tmp_path / "x.json")).replace("- id: s2", "- id: s1")
    r = validate(_write(tmp_path, text))
    assert r["exit_code"] == 2


def test缺steps或空steps_配置错误(tmp_path):
    r = validate(_write(tmp_path, "title: 空的\nsteps: []\n"))
    assert r["exit_code"] == 2


def testevidence_cite为空串_等于没证据(tmp_path):
    text = GOOD.replace("{{EVID}}", str(tmp_path / "x.json")).replace(
        'evidence_cite: "vllm-serving-card/results/environment.txt (2026-11-09)"',
        'evidence_cite: ""')
    r = validate(_write(tmp_path, text))
    assert r["exit_code"] == 2


def test文件不存在_配置错误不是崩溃(tmp_path):
    r = validate(str(tmp_path / "没有这个.yaml"))
    assert r["exit_code"] == 2


def test返回结构带步骤明细(tmp_path):
    evid = tmp_path / "card.json"
    evid.write_text("{}", encoding="utf-8")
    r = validate(_write(tmp_path, GOOD.replace("{{EVID}}", str(evid))))
    assert r["total"] == 2 and r["done"] == 2
    assert r["steps"][0]["id"] == "s1" and r["steps"][0]["status"] == "DONE"
