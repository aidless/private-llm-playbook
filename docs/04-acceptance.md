# 验收指标（闸，不是自评）

1. **性能闸**：ttftkit `limits`（TTFT/TPOT p95 上限、error_rate 预算）与
   `regressions`（相对基线退化百分比）。
2. **不变性闸**：同 prompt 跑 `concurrency=1` 与目标 batch 各一轮（`capture_outputs=True`），
   输出逐字节一致才算数——缺 outputs 是「没测」（exit 2），不是通过。
3. **复算命令**：所有数字必须能从原始文件重算（`vllm-serving-card/parse_results.py`）；
   重算不一致 = 阻塞，不是小事。

工作区本地核对三件证据：

```bash
test -f ../vllm-serving-card/results/card.json
test -f ../ttftkit/src/ttftkit/gate.py
test -f ../paper_agent/train/train_agent.py
```
