"""playbook-check 命令行：校验 playbook checklist 的完成度与证据链。

退出码与校验器一致：0=全完成且证据齐；1=有剩余步骤/断链证据；2=结构畸形。
"""
from __future__ import annotations

import argparse
import json
import sys

from .checklist import validate


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="playbook-check",
                                     description="校验 playbook checklist（fail-closed）")
    parser.add_argument("checklist", help="checklist YAML 路径")
    parser.add_argument("--json", action="store_true", help="输出结构化 JSON")
    args = parser.parse_args(argv)
    result = validate(args.checklist)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"{result['done']}/{result['total']} 步骤完成（exit {result['exit_code']}）")
        for reason in result["reasons"]:
            print(f"  - {reason}")
    return result["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
