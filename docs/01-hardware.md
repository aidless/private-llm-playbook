# 硬件矩阵（全部引用实测，不产生新数字）

| 档位 | 实测载体 | 关键数字 | 证据 |
|---|---|---|---|
| 6GB 消费卡（RTX 3060 Laptop） | vllm-serving-card | 权重 2.5 GiB（Qwen3-4B-AWQ）、KV cache 2.09 GiB / 15,232 tokens、2048-len 请求理论最大并发 7.44× | `vllm-serving-card/README.md` 环境表（2026-11-09） |
| 微调显存边界 | paper_agent | QLoRA 4bit NF4 SFT 跑通；DPO 6GB 卡四次 OOM 后封存 | `paper_agent/README.md`（诚实自声明） |
| 云端通道 | amd-radeon-cloud | 中国站 launch 失败四条官方原因 + 30 秒只读自检脚本 | `amd-radeon-cloud/README.md`（2026-10-21 核实） |

选型读法：私有化部署的瓶颈不是参数量而是 **KV cache 预算**（15,232 tokens 是 6GB 卡
在 2048-len 下的天花板）；微调的瓶颈是优化器态显存（DPO 双模型驻留直接 OOM）。
