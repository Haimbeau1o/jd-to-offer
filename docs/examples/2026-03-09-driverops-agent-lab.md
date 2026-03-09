# DriverOps Agent Lab Scaffold

## 目标

给滴滴司机智能助手相关岗位准备一个可运行、可讲解、可扩展的最小项目骨架。当前版本重点覆盖：

- 意图识别
- 工具调用
- 短期记忆
- 策略推荐
- FastAPI 服务化
- 面向司机经营问题的场景化回答

## 当前代码位置

- `src/driverops_agent_lab/agent.py`
- `src/driverops_agent_lab/tools.py`
- `src/driverops_agent_lab/memory.py`
- `src/driverops_agent_lab/app.py`

## 已实现能力

1. 收入解释：读取司机画像与行程统计，解释收入波动
2. 活动推荐：按城市、司机分层和标签匹配活动
3. 热区建议：给出高收益热区与时段建议
4. 规则问答：从轻量规则库返回依据
5. Memory：记录最近查询，支持后续扩展为长期记忆

## 运行方式

```bash
PYTHONPATH=src python -m driverops_agent_lab.app
```

服务启动后可调用：

```bash
curl -X POST http://127.0.0.1:8001/chat \
  -H 'Content-Type: application/json' \
  -d '{"driver_id":"driver-001","city":"beijing","query":"今天有什么活动适合我"}'
```

## 下一步扩展

- 接入真实 LLM planner / function calling
- 接入长期记忆存储
- 增加离线评测与失败案例回放
- 用检索或向量库替代当前规则数组
- 把策略推荐升级为可配置 reward / ranking 模块
