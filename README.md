# private-llm-playbook

小模型私有化部署 playbook：**硬件矩阵 + 部署步骤 + 验收指标 + 成本账**，
全部实测数字引用现有资产（vllm-serving-card / paper_agent / amd-radeon-cloud / ttftkit），
本仓库零新实测——它是「登记与组织」，不是「再测一遍」。

## 两条路线

| playbook | 覆盖 | 状态 |
|---|---|---|
| `playbooks/single-card-vllm.yaml` | 6GB 消费卡 vLLM 部署全链（硬件→启动→SLO→成本→验收） | 6/6 步骤有证据（exit 0） |
| `playbooks/cloud-qlora-finetune.yaml` | 云端 QLoRA 微调 → 回本地部署 | 3/4（adapter 合并部署未实测，诚实标 false） |

## 校验器

```bash
pip install -e .
playbook-check playbooks/single-card-vllm.yaml   # exit 0=全完成且证据齐 / 1=有剩余或断链 / 2=畸形
```

纪律：`done: true` 的唯一凭证是字节（`evidence_path` 文件存在，或 `evidence_cite`
登记了外部仓库路径与日期）。缺证据 = 没测，与 ttftkit invariance 闸同一口径。

## 为什么是 playbook 不是实验

2026-11-10 存在性普查（`portfolio/second-half-census-2026-11-10.json` P3）判定：
实测字节已在四个姊妹仓库，缺的是登记与组织。本仓库补的就是这一格。
