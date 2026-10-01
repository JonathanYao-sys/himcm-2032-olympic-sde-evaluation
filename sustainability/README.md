# HiMCM Sustainability Submodel

本目录对 IOC Sustainability 标准中的两个主因子建模：

1. `Resource consumption`：资源消耗强度；
2. `Carbon emissions`：碳排放强度。

模型最终输出 `S ∈ [0,1]`。分数越高，表示资源和碳排放影响越低，可持续性越好。

## 文件

| 文件 | 作用 |
|---|---|
| `README.md` | 建模方法、数据口径、公式和阈值 |
| `sustainability_model.py` | 计算 Sustainability 分数 |
| `sustainability_data.csv` | 空白数据模板 |
| `项目中文名.csv` | 每个 SDE 的实际数据 |
| `output.md` | 21 个项目的运行结果汇总 |

用户清单中的 `Fencing（击剑）` 出现两次，本项目已合并，因此实际为 21 个唯一 SDE。

## 两种数据模式

模型支持两种输入模式。同一个 CSV 中不要混用同一因子的两种模式。

### 模式 A：原始强度模式

| 字段 | 含义 | 单位 |
|---|---|---|
| `energy_kwh_per_athlete_day` | 能源消耗强度 | kWh/athlete-day |
| `water_m3_per_athlete_day` | 水资源消耗强度 | m³/athlete-day |
| `carbon_kgco2e_per_athlete_day` | 碳排放强度 | kgCO₂e/athlete-day |

Resource 指标先分别归一化：

```text
S_energy = (max(E) − E) / (max(E) − min(E))
S_water  = (max(W) − W) / (max(W) − min(W))
S_resource = mean(available S_energy, S_water)
```

Carbon 指标：

```text
S_carbon = (max(C) − C) / (max(C) − min(C))
```

### 模式 B：0–1 高影响指数模式

当不同 SDE 的原始场馆数据不可比或不可获得时，使用：

| 字段 | 含义 |
|---|---|
| `resource_consumption_index` | 资源消耗高影响指数，0 = 很低，1 = 很高 |
| `carbon_emissions_index` | 碳排放高影响指数，0 = 很低，1 = 很高 |

指数越高表示影响越大，因此转化为正向后：

```text
S_resource = 1 − resource_consumption_index
S_carbon   = 1 − carbon_emissions_index
```

本批 21 个项目的 CSV 使用模式 B。

## CSV 字段

每一行表示：

```text
SDE × 观测期
```

| 字段 | 说明 |
|---|---|
| `sde_id` | SDE 编号 |
| `sde_name` | SDE 名称 |
| `period_order` | 观测期顺序，数字越大越新 |
| `period_label` | 观测期标签 |
| `energy_kwh_per_athlete_day` | 模式 A 使用 |
| `water_m3_per_athlete_day` | 模式 A 使用 |
| `carbon_kgco2e_per_athlete_day` | 模式 A 使用 |
| `resource_consumption_index` | 模式 B 使用，0–1 |
| `carbon_emissions_index` | 模式 B 使用，0–1 |
| `coverage_status` | `complete`、`partial` 或 `unknown` |
| `source` | 数据来源或建模依据 |
| `notes` | 口径和限制 |

缺失值可填写空、`NA` 或 `N/A`。

## 代理指数口径

### Resource consumption index

由于公开报告很少提供按 SDE 拆分的场馆水电表数据，本批采用设施类型代理编码：

- 涉水项目：较高；
- 室内恒温、照明和空调负荷高的项目：较高；
- 室外场地：中等；
- 室外开放型、小型场地项目：较低。

该指数不是场馆实测能源或用水量。

### Carbon emissions index

碳指数使用全球参与国家数作为旅行和赛事规模的代理：

```text
C = min(1, 0.10 + 0.90 × N/215)
```

其中 `N` 来自前一阶段 Inclusivity 数据的当前期覆盖国家数。

该变量是碳排放影响的代理，不是由赛事碳核算报告直接得到的 SDE 碳排放。

### 主要参考资料

- Paris 2024 Sustainable Games:
  https://www.olympics.com/ioc/paris-2024-sustainable-games
- Paris 2024 carbon emissions report:
  https://www.olympics.com/ioc/news/paris-2024-report-confirms-over-50-carbon-emissions-reduction
- OECD legacy report:
  https://www.oecd.org/en/publications/the-legacy-of-the-paris-2024-olympic-and-paralympic-games_d7938b7f-en.html

## 权重

默认使用组合赋权：

```text
w = α × w_fixed + (1 − α) × w_entropy
```

默认参数：

```python
WEIGHT_MODE = "hybrid"
FIXED_WEIGHTS = {"resource": 0.50, "carbon": 0.50}
HYBRID_ALPHA = 0.50
```

熵权定义：

```text
p_ij = x_ij / Σ_i x_ij
e_j = −(1 / ln n) × Σ_i p_ij ln p_ij
w_j = (1 − e_j) / Σ_k (1 − e_k)
```

当样本量小于 3 或熵权退化时，程序使用固定权重。

## 最终分数

```text
S = w_R × S_resource + w_C × S_carbon
```

`S ∈ [0,1]`。

默认阈值：

```python
SUSTAINABILITY_THRESHOLD = 0.60
```

```text
Sustainability_pass = S ≥ 0.60
```

`0.60` 是本模型的比较阈值，不是 IOC 官方给定阈值。论文中建议对 `0.50`、`0.60`、`0.70` 做敏感性分析。

## 运行

默认运行：

```bash
python3 sustainability_model.py
```

指定任意 CSV：

```bash
python3 sustainability_model.py 篮球.csv
```

程序只在终端输出结果，不生成额外文件。`output.md` 是本批验证结果汇总。
