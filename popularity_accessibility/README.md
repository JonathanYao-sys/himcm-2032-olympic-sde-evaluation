# Popularity and Accessibility Submodel

本文件夹对应 IOC 标准中的 `Popularity and Accessibility`。

来源脚本：`olympic_evaluation.py`。

## 识别结果

该脚本并不是完全单一的 Popularity 模型。它包含两个维度：

| 维度 | 指标 | 脚本内权重 |
|---|---|---:|
| Popularity | C1–C5 | 0.85 |
| Sustainability | S 人均办赛成本 | 0.15 |

因此：

```text
Total_Score = 0.85 × Popularity_Score
            + 0.15 × Sustainability_Cost_Score
```

对于整体 Overall 模型，推荐只使用：

```text
Popularity_Score
```

作为 `Popularity and Accessibility` 维度得分。`S_PerCapitaCost_KUSD` 应交给 Sustainability 子模型处理，否则会与现有的 `sustainability` 维度重复计算。

## 指标定义

Popularity 维度包含五个正向指标：

| 指标 | 字段 | 含义 | 方向 |
|---|---|---|---|
| C1 | `C1_ViewShare_Pct` | 收视份额，% | 正向 |
| C2 | `C2_Attendance_Pct` | 上座率，% | 正向 |
| C3 | `C3_Nations` | 参与国家数 | 正向 |
| C4 | `C4_RegisteredAthletes` | 注册运动员数 | 正向 |
| C5 | `C5_Top5AvgFollowers_10k` | 前五名运动员平均粉丝数，万人 | 正向 |

Sustainability 成本指标：

| 指标 | 字段 | 含义 | 方向 |
|---|---|---|---|
| S | `S_PerCapitaCost_KUSD` | 人均办赛成本，千美元 | 负向 |

## 数据预处理

对长尾指标 C4、C5 使用：

```text
x_log = ln(1 + x)
```

然后对每个指标做 Min–Max 归一化。

正向指标：

```text
x' = (x − min(x)) / (max(x) − min(x))
```

负向指标：

```text
x' = (max(x) − x) / (max(x) − min(x))
```

如果某个指标所有项目取值相同，则该指标没有区分能力，在熵权中权重为 0。

## 熵权法

对每个维度内部分别计算熵权。

比重：

```text
p_ij = x'_ij / Σ_i x'_ij
```

信息熵：

```text
e_j = −(1 / ln n) × Σ_i p_ij ln(p_ij)
```

差异系数：

```text
d_j = 1 − e_j
```

指标权重：

```text
w_j = d_j / Σ_j d_j
```

## 维度得分

Popularity 维度：

```text
Popularity_Score =
w_C1 × C1' + w_C2 × C2' + w_C3 × C3'
+ w_C4 × C4' + w_C5 × C5'
```

Sustainability 成本维度：

```text
Sustainability_Cost_Score = S'
```

脚本最终总分：

```text
Total_Score = 0.85 × Popularity_Score
            + 0.15 × Sustainability_Cost_Score
```

## 与 Overall 模型的关系

在 `overall` 中建议使用：

```text
Overall_Popularity_Accessibility = Popularity_Score
```

不要把脚本的 `Total_Score` 直接作为 Popularity 维度得分，因为 `Total_Score` 已经包含 15% 的 Sustainability 成本。

此外，`C3_Nations` 与 Inclusivity 中的国家覆盖存在概念重叠。如果要严格避免重复计分，可以：

1. 使用脚本的 `Popularity_Score`，但在论文中说明 C3 是 Popularity 的传播规模代理；或
2. 从 Popularity 维度中移除 C3，只用 C1、C2、C4、C5，把国家覆盖完全交给 Inclusivity 处理。

## CSV 字段

`popularity_accessibility_data.csv` 包含：

| 字段 | 说明 |
|---|---|
| `sde_id` | SDE 唯一编号 |
| `sport` | 英文项目名称 |
| `sport_cn` | 中文项目名称 |
| `C1_ViewShare_Pct` | 收视份额 |
| `C2_Attendance_Pct` | 上座率 |
| `C3_Nations` | 参与国家数 |
| `C4_RegisteredAthletes` | 注册运动员数 |
| `C5_Top5AvgFollowers_10k` | 前五名运动员平均粉丝数 |
| `S_PerCapitaCost_KUSD` | 人均办赛成本 |
| `Popularity_Score` | 脚本计算出的 Popularity 得分 |
| `Sustainability_Cost_Score` | 成本指标正向化后的得分 |
| `Total_Score` | 0.85 × Popularity + 0.15 × Sustainability |
| `source` | 数据来源说明 |
| `notes` | 数据限制说明 |

## 当前限制

1. 原始脚本没有包含 C1–C5 和 S 的公开来源链接，因此 CSV 中的 `source` 只能记录为脚本输入数据。
2. `C3_Nations` 与 Inclusivity 指标存在重叠。
3. `S_PerCapitaCost_KUSD` 与 Sustainability 模型存在重叠。
4. `Popularity_Score` 不能单独代表 Accessibility；Accessibility 需要场馆、成本、参与门槛等额外数据。
5. 当前脚本使用 Python 的 `numpy` 和 `pandas`，本目录暂只保存 README 和 CSV，不包含执行脚本。
