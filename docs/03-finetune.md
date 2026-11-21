# 微调路线（QLoRA，诚实边界）

- 栈：`paper_agent/train/`（train_agent.py SFT + train_dpo.py）。
- 数据纪律：每个样本强制 `evidence_refs` + `arxiv_grounding`——模型学的是
  「写有据可查的话」，不是「写漂亮话」（`paper_agent/build_sft.py`）。
- 边界（不粉饰）：缺真 DPO（6GB 卡 OOM）、缺真人偏好标注、合成分布天花板已现。
  这是「技术报告档」的结论，部署 playbook 引用它时同样只当 SFT 档用。
