# Relevance and Innovation Submodel

本目录用于 IOC 标准中的 `Relevance and Innovation` 子模型。

模型使用两个指标：

1. `R1_YoungAppeal`：对年轻人的吸引力；
2. `R2_YearScore`：年份变量/新近程度。

两个指标均为 `0–1`，其中数值越高表示该项目在对应维度上越强。

最终输出：

```text
Score ∈ [0,1]
```

## 文件

| 文件 | 作用 |
|---|---|
| `README.md` | 模型方法、公式和数据口径 |
| `innovation_data.csv` | 各 SDE 的 R1、R2 数据 |
| `innovation_model.py` | 计算熵权、综合得分和排名 |

## CSV 数据格式

`innovation_data.csv` 每行表示一个 SDE：

| 字段 | 说明 |
|---|---|
| `sde_id` | SDE 编号 |
| `sde_name` | SDE 名称 |
| `R1_YoungAppeal` | 年轻人吸引力，0–1 |
| `R2_YearScore` | 年份变量/新近程度，0–1 |
| `source` | 数据来源或数据说明 |
| `notes` | 口径和限制 |

当前数据来自用户提供的 Relevance and Innovation 计算代码。原代码没有附带 R1、R2 的正式来源链接，因此当前来源字段记录为历史输入数据。

## 熵权法

设第 `j` 个指标在第 `i` 个 SDE 上的取值为 `x_ij`。

### 1. 比重矩阵

```text
p_ij = x_ij / Σ_i x_ij
```

### 2. 信息熵

```text
e_j = -(1 / ln n) × Σ_i p_ij ln(p_ij)
```

其中 `n` 是 SDE 数量。若 `p_ij = 0`，则按 `p_ij ln(p_ij) = 0` 处理。

### 3. 差异系数

```text
d_j = 1 - e_j
```

### 4. 权重

```text
w_j = d_j / Σ_j d_j
```

`w_R1 + w_R2 = 1`。

## 综合得分

两个指标已经是 `0–1`，因此不再做额外 Min–Max 归一化：

```text
Score = w_R1 × R1_YoungAppeal
      + w_R2 × R2_YearScore
```

`Score` 的范围为 `0–1`，分数越高表示 Relevance and Innovation 表现越好。

## 运行方法

直接运行：

```bash
python3 innovation_model.py
```

也可以指定 CSV：

```bash
python3 innovation_model.py /path/to/innovation_data.csv
```

或者修改 Python 文件顶部：

```python
CSV_FILE = "innovation_data.csv"
```

程序只输出到终端，不额外生成结果文件。

## 输出内容

程序会输出：

1. R1 和 R2 的熵值；
2. R1 和 R2 的差异系数；
3. 熵权法得到的权重；
4. 每个 SDE 的 R1、R2 和最终 `Score`；
5. 按 `Score` 降序排列的排名。

## 模型限制

1. `R1_YoungAppeal`、`R2_YearScore` 当前是 0–1 代理评分，不是直接从统一官方数据库获取的连续变量。
2. R1 的原始调查口径、样本对象和年份需要补充。
3. R2 的具体定义需要固定，例如是项目首次进入奥运会的时间、最近一次新增时间，还是项目更新速度。
4. 熵权法反映当前样本中的指标差异，不代表 IOC 政策重要性。
5. 本模型是 Relevance and Innovation 子模型，不能单独决定 SDE 是否加入或移除奥运会。
