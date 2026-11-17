# tiny-chess-01 · 任务书

## 0. 准入自检

- [x] 需要拉真人注册？否
- [x] 需要钱包签名转账？否（仅 GitHub 登录或 API key）
- [x] 需要垫钱入场？否

## 1. 题面摘要

**目标**: 用 ≤4096 字节 Python 3.13 标准库写一个国际象棋引擎，在 make.fun 赏金中击败 8 个 house 引擎。

**House 引擎（按强度排序）**:
- depth-2 (855 Elo), depth-3 (1073), depth-4 (1199)
- nodes-100k (1392), nodes-250k (1497), nodes-500k (1596)
- nodes-1M (1667), nodes-2M (1712)

**评分**: Elo 等级分，基于 Bradley-Terry 模型，0-2112 范围。
**门槛**: 练习赛 Elo ≥1154 可进入决赛。
**基准**: Sunfish 4KB 引擎，练习赛平均 1325 Elo。

**约束**:
- main.py ≤4096 字节（已提交大小）
- 整仓 ≤8192 字节
- 每步 ≤10 秒，总限时 1800 秒
- 确定性：无墙钟、无未播种随机
- 仅标准库，无模型调用

## 2. 交付物

- `main.py` — 核心引擎（depth-2 alpha-beta + PST 评估）
- `LICENSE` — MIT
- `README.md` — 项目说明
- `.makefun/owner.json` — 钱包声明
- `.gitignore` — 排除 .makefun/

## 3. 评分方式

- Elo 等级分（越高越好）
- 需要超过 Sunfish 基准（90% 置信区间）
- 每步 ≤10 秒，总时 ≤1800 秒

## 4. 任务分解

### T1: 引擎核心 ✅
- 实现棋盘表示（64 元素列表）
- 实现走法生成（所有棋子类型）
- 实现走法应用
- 实现 UCI 协议通信

### T2: 评估函数 ✅
- 子力价值（p:100, n:320, b:330, r:500, q:900）
- 子力位置表（PST）
- 王安全（PST 惩罚）

### T3: 搜索算法 ✅
- Alpha-beta 剪枝
- 移动排序（MVV-LVA）
- 节点限制（50K）
- 深度 2

### T4: 性能优化 ✅
- 单 ply 评估 <0.5 秒
- 总 6 游戏 <60 秒
- 无超时风险

### T5: 验证 ✅
- 本地 6 游戏练习赛测试
- 文件大小检查
- 语法检查

### T6: 提交准备 ✅
- bundle --dry-run
- bountygate 全绿
- 提交

## 5. 提交前检查

- [x] `bountygate.sh tiny-chess-01-clean` 全绿
- [x] `bundle --dry-run` 确认会话日志
- [x] 文件大小: main.py 4051B, 整仓 6241B
- [x] 语法检查通过
- [x] 无 banned imports
