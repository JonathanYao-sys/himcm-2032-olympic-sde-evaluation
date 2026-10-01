# Safety and Fair Play Submodel

本模型对应 IOC 标准中的 `Safety and Fair Play`，使用三个指标：

1. `doping_screening`：兴奋剂筛查；
2. `injury_incidence_rate`：运动损伤发生率；
3. `fairness_enforcement`：执法公平性。

最终输出 `Score ∈ [0,1]`，分数越高表示 Safety and Fair Play 表现越好。

## 1. 指标方向

| 指标 | 字段 | 类型 | 方向 |
|---|---|---|---|
| 兴奋剂筛查 | `doping_screening` | 0/1 | 正向 |
| 运动损伤发生率 | `injury_incidence_rate` | 0–1 | 负向 |
| 执法公平性 | `fairness_enforcement` | 0/1 | 正向 |

负向指标先行正向化：

```text
x_injury_forward = 1 - injury_incidence_rate
```

## 2. 数据归一化

对每个指标做 Min–Max 归一化。

正向指标：

```text
x' = (x - min(x)) / (max(x) - min(x))
```

负向指标：

```text
x' = (max(x) - x) / (max(x) - min(x))
```

如果某一列所有 SDE 的取值相同，则该列统一设为 `1.0`，避免除以 0。

## 3. 熵权法

设归一化后的数据矩阵为 `X'`，共有 `m` 个指标、`n` 个 SDE。

计算指标比例：

```text
p_ij = x'_ij / Σ_i x'_ij
```

计算信息熵：

```text
e_j = -(1 / ln n) × Σ_i p_ij ln(p_ij)
```

计算差异系数：

```text
d_j = 1 - e_j
```

计算权重：

```text
w_j = d_j / Σ_j d_j
```

如果某个指标在所有 SDE 中取值完全相同，则 `e_j ≈ 1`，该指标权重接近 0。

在当前数据中，`doping_screening` 对所有 SDE 都为 1，因此该指标没有区分能力，权重为 0。

## 4. 综合得分

使用归一化后的指标计算：

```text
Score = w_doping × x'_doping
      + w_injury × x'_injury
      + w_fairness × x'_fairness
```

`Score` 的范围为 `0–1`。如果需要百分比，可在论文中额外显示：

```text
Score_percent = Score × 100
```

## 5. CSV 数据格式

`safety_fair_play_data.csv` 每行表示一个 SDE：

| 字段 | 说明 |
|---|---|
| `sde_id` | SDE 编号 |
| `sde_name` | SDE 名称 |
| `doping_screening` | 0 或 1；1 表示通过/合规 |
| `injury_incidence_rate` | 0–1 的损伤发生率 |
| `fairness_enforcement` | 0 或 1；1 表示执法公平 |
| `source` | 数据来源或当前数据说明 |
| `notes` | 数据口径和限制 |

当前 CSV 的数据来自原 `legacy_weight_calculation.py` 和 `safety_fair_play_score.py` 中的配置数据。原文件没有完整来源链接，因此当前来源字段记为历史配置数据。

## 6. Python 文件

`safety_fair_play_model.py` 只使用 Python 标准库，不依赖 pandas、requests 或 BeautifulSoup。

运行方法：

```bash
python3 safety_fair_play_model.py
```

也可以指定 CSV：

```bash
python3 safety_fair_play_model.py /path/to/data.csv
```

程序会输出：

- 三个指标的归一化值；
- 熵权法得到的权重；
- 每个 SDE 的最终 `Score`；
- 按 `Score` 降序排列的排名。

## 7. 当前模型限制

1. 损伤发生率的数据来源未在旧脚本中完整保留，需要后续用官方伤病研究补充来源链接。
2. `doping_screening` 当前所有 SDE 都为 1，因此熵权为 0；这不代表兴奋剂治理不重要，而是该列在当前样本中没有区分能力。
3. `fairness_enforcement` 是 0/1 代理变量，不是完整的公平裁判审计结果。
4. 熵权法只反映当前样本中的指标差异，不代表 IOC 政策重要性。
5. 当前模型是 Safety and Fair Play 子模型，不能单独决定 SDE 是否应被加入或移除奥运会。
