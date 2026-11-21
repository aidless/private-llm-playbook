# 部署步骤（命令逐条引用实测仓库）

启动命令与三个坑（端口占用、tokenizer 在线拉取卡住、JIT 冷启动）逐字引用
`vllm-serving-card/README.md`「环境与启动」，此处不复制正文，只给核对入口：

```bash
test -f ../vllm-serving-card/results/card.json   # 证据在位
cat ../vllm-serving-card/README.md               # 启动命令 + 坑清单
```

SLO 分档结论（2026-11-09 实测）：交互式并发上限 **4**（TTFT p99 481.2 ms），
批处理/离线吃 16 档（261.41 tok/s，13.1×）；decode 侧不变慢（TPOT p99 65.06→61.78 ms），
排队发生在首 token 之前。
