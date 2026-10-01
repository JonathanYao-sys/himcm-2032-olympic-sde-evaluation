# Overall IOC Criteria Model

本目录把六个子模型的得分合成为一个总评模型：

1. `popularity_accessibility`：Popularity and Accessibility；
2. `inclusivity`：Inclusivity；
3. `safety_fair_play`：Fairness and Safety；
4. `sustainability`：Sustainability；
5. `innovation`：Relevance and Innovation；
6. `gender_equality`：Gender Equity。

所有子模型分数先统一到 `0–1`。

## 文件

| 文件 | 作用 |
|---|---|
| `README.md` | Overall 公式、权重和解释 |
| `overall_data.csv` | 六维得分输入矩阵 |
| `overall_model.py` | 计算总评、排名和敏感性分析 |
| `output.md` | 运行结果 |

## 一个重要说明

附件第一张图里的 `总分` 只是二维合成：

```text
旧总分 ≈ 0.85 × Popularity + 0.15 × Sustainability
```

这个公式只使用了 2 个维度，不能直接用于本题的 6 个 IOC 标准。因此 `overall` 使用六维模型重新合成。

另外，图 1 的 `Sustainability` 列与 `sustainability/output.md` 的 `S` 不一致；本模型采用最新的详细 Sustainabaility 子模型结果 `S`。图 1 只用于提取 `Popularity` 分数。

## 统一公式

设六个维度的得分为：

```text
D = (D_1, ..., D_6)
```

总评定义为：

```text
Overall = Σ_{k=1}^{6} w_k D_k
```

其中：

```text
Σ w_k = 1
```

## 权重方法

由于 IOC 没有给出六个标准的官方权重，本模型使用“等权先验 + 熵权修正”的混合权重：

```text
w_k = α × w_k^fixed + (1 − α) × w_k^entropy
```

默认：

```python
HYBRID_ALPHA = 0.50
FIXED_WEIGHTS = {
    "popularity_accessibility": 1/6,
    "inclusivity": 1/6,
    "safety_fair_play": 1/6,
    "sustainability": 1/6,
    "innovation": 1/6,
    "gender_equality": 1/6,
}
```

### 熵权计算

对第 `k` 个维度：

```text
p_ik = D_ik / Σ_i D_ik
e_k = −(1 / ln n) × Σ_i p_ik ln(p_ik)
d_k = 1 − e_k
w_k^entropy = d_k / Σ_j d_j
```

其中 `n` 是 SDE 数量。

等权先验避免模型完全由样本方差决定；熵权修正让区分度较高的维度获得适当更高权重。

## 输出

`overall_model.py` 会输出：

- 六个维度的最终权重；
- 每个 SDE 的 Overall；
- 等权、熵权、混合权三种排名；
- 敏感性分析结果；
- `output.md`。

## 运行

```bash
cd overall
python3 overall_model.py
```

也可以修改 `overall_model.py` 顶部的：

```python
CSV_FILE = "overall_data.csv"
HYBRID_ALPHA = 0.50
```

## 解释

- `Overall` 是六项 IOC 标准的综合得分，不是单一运动普及度。
- `popularity_accessibility` 当前主要使用附件图的 Popularity 分数，Accessibility 没有单独字段，因此仍属于代理评分。
- `sustainability` 使用最新 Sustainability 子模型的 `S`，不是图 1 的旧 Sustainability 列。
- 由于六个子模型的数据质量不同，`Overall` 应用于排序和敏感性分析，不应当被解释为绝对真实的世界排名。

## 六个子模型的内部公式

### D1：Popularity and Accessibility

当前使用附件图中的 Popularity 分数作为该维度得分：

```text
D1 = Popularity_score
```

其中 Accessibility 尚未单独建模，因此 `D1` 在当前版本中是 Popularity & Accessibility 的代理分数。

### D2：Inclusivity

```text
D2 = I = 0.35P + 0.25D + 0.20B + 0.10R + 0.10T
```

其中：

```text
P = 国家覆盖广度
D = 五大洲覆盖深度
B = 五大洲分布均衡性
R = 次区域代表性
T = 持续全球参与
```

### D3：Fairness and Safety

先进行正负向指标的 Min–Max 归一化：

```text
正向指标：x' = (x − min(x)) / (max(x) − min(x))
负向指标：x' = (max(x) − x) / (max(x) − min(x))
```

使用熵权法：

```text
p_ij = x'_ij / Σ_i x'_ij
e_j = −(1 / ln n) × Σ_i p_ij ln(p_ij)
d_j = 1 − e_j
w_j = d_j / Σ_j d_j
```

最终得分：

```text
D3 = w_doping × x'_doping
   + w_injury × x'_injury
   + w_fairness × x'_fairness
```

### D4：Sustainability

资源与碳排放均先正向化为 `0–1` 得分：

```text
S_resource = 1 − resource_consumption_index
S_carbon   = 1 − carbon_emissions_index
```

组合权重：

```text
w = α × w_fixed + (1 − α) × w_entropy
```

最终得分：

```text
D4 = S = w_R × S_resource + w_C × S_carbon
```

### D5：Relevance and Innovation

使用两个指标 `R1`（年轻人吸引力）和 `R2`（年份/新近程度）：

```text
p_ij = x_ij / Σ_i x_ij
e_j = −(1 / ln n) × Σ_i p_ij ln(p_ij)
d_j = 1 − e_j
w_j = d_j / Σ_j d_j
```

最终得分：

```text
D5 = w_R1 × R1 + w_R2 × R2
```

### D6：Gender Equity

```text
X1 = 1 − 2 × |P_female − 0.5|
X2 = min(Male_Events, Female_Events) / max(Male_Events, Female_Events)
X3 = 1 − 2 × |P_2032 − 0.5|
```

最终得分：

```text
D6 = (X1 + X2 + X3) / 3
```

## 最终合成公式

```text
Overall = w1 × D1
        + w2 × D2
        + w3 × D3
        + w4 × D4
        + w5 × D5
        + w6 × D6
```

其中权重采用：

```text
w_k = α × w_k^fixed + (1 − α) × w_k^entropy
α = 0.50
```

最终输出一个 `0–1` 的 Overall 分数和 SDE 排名。
