# HiMCM Inclusivity Submodel

本目录是目前用于 Inclusivity 子模型验证的干净工作区。

## 文件结构

| 文件 | 作用 |
|---|---|
| `README.md` | 建模方法、数据口径、公式和阈值 |
| `inclusivity_model.py` | 计算 P、D、B、R、T、I，并判断是否达标 |
| `inclusivity_data.csv` | 空白模板 |
| `项目中文名.csv` | 每个项目的实际填写数据，例如 `篮球.csv` |
| `output.md` | 21 个项目的运行结果汇总 |

## 模型目标

题目中的 Inclusivity 标准为：

> at least 75 countries across four continents practicing the sport

模型分开判断：

1. `Gate`：当前期是否达到 `N ≥ 75` 且 `K ≥ 4`。
2. `I`：达到基本规模后，进一步衡量国家覆盖和地理分布质量。
3. `Final_pass`：同时满足 `Gate` 和 `I ≥ 0.75`。

`P、D、B、R、T、I` 全部为 `0–1`，不使用 0–100 分制。

## 数据口径

本批数据采用可审计的混合口径：

- `t1`、`t2`：历史观测期，使用旧存档中的官方赛事参赛记录，主要是奥运会、世锦赛或世界杯参与名单。
- `t3`：当前期，使用国际单项联合会的现行国家协会/成员协会名单，作为“practicing the sport”的可核验代理。
- 当前期成员协会只能证明该国家拥有持续存在的国家组织体系，不能证明运动员注册人数或群众参与人数。
- 因为直接获取全球统一口径的注册活跃人数不可行，当前数据统一标记为 `coverage_status=partial`。
- 因此 `output.md` 的结果是**代理数据下的模型验证结果**，不应当被表述为 IOC 最终事实判断。

对于正式提交，应在论文中明确写出：

```text
Current period N = number of IF-recognised national associations
Historical period N = number of countries with official event participation evidence
```

## CSV 字段

每一行表示：

```text
SDE × 观测期 × 国家/协会
```

| 字段 | 说明 |
|---|---|
| `sde_id` | SDE 编号，例如 `BASKETBALL` |
| `sde_name` | 项目名称 |
| `period_order` | 观测期顺序，1、2、3 |
| `period_label` | 观测期标签 |
| `country_code` | 国家/NOC/协会代码 |
| `country_name` | 国家/协会名称 |
| `continent` | `Africa`、`Americas`、`Asia`、`Europe`、`Oceania` |
| `m49_subregion` | UN M49 次区域名称 |
| `unit_type` | `country`、`noc`、`if_member` 或 `special` |
| `activity_status` | `active`、`inactive`、`unknown`、`not_applicable` |
| `coverage_status` | `complete`、`partial`、`unknown`、`not_applicable` |
| `source` | 活动或成员证据链接 |
| `notes` | 口径和限制说明 |

只有 `activity_status=active` 的记录会计入 N、K 和各项地理指标。

## 变量定义

设观测期 `s` 的正活动国家集合为 `A_s`：

```text
N_s = |A_s|
```

即该时期有活动代理证据的国家/协会单位数。

设：

```text
n_c = 第 s 期位于洲 c 的活跃国家数
K_s = 活跃国家数大于 0 的洲数
```

程序将 `period_order` 最大的观测期作为当前期。

## 五个因子

### P：国家覆盖广度

```text
若 N < 75:
    P = 0.70 × N / 75

若 N ≥ 75:
    P = 0.70 + 0.30 × [1 − exp(−(N−75)/50)]
                     / [1 − exp(−(206−75)/50)]
```

`P` 衡量国家数量的绝对覆盖规模，范围为 `0–1`。

### D：五大洲覆盖深度

```text
D = (1/5) × Σ_c min(n_c / 15, 1)
```

其中 `15` 是每个洲达到“满深度”的参考国家数。

### B：五大洲分布均衡性

```text
H_B = −Σ_c p_c ln(p_c)
p_c = n_c / N
B = H_B / ln(5)
```

`B` 越大，表示活跃国家在五大洲之间越均衡。

### R：次区域代表性

```text
H_R = −Σ_r q_r ln(q_r)
q_r = n_r / N
R = H_R / ln(22)
```

其中 `22` 是 UN M49 地理次区域数量。`R` 越大，表示覆盖的地理次区域越丰富。

### T：持续全球参与

对每个可评估观测期计算：

```text
T_s = 0.5 × min(N_s / 75, 1)
    + 0.5 × min(K_s / 4, 1)
```

然后：

```text
T = average(T_s)
```

只有可评估观测期进入平均。项目尚未出现或证据完全不可用的时期不计入 T。

## 综合质量分

```text
I = 0.35P + 0.25D + 0.20B + 0.10R + 0.10T
```

`I` 范围为 `0–1`。

## 阈值

```text
Gate_pass    = N_current ≥ 75 且 K_current ≥ 4
Quality_pass = I ≥ 0.75
Final_pass   = Gate_pass 且 Quality_pass
```

`0.75` 是当前默认质量阈值，可以在 Python 文件顶部修改：

```python
QUALITY_THRESHOLD = 0.75
```

建议在论文中测试 `0.70`、`0.75`、`0.80` 三个阈值，并比较排名稳定性。

## 运行方法

直接运行：

```bash
python3 inclusivity_model.py 篮球.csv
```

也可以在 Python 文件顶部修改：

```python
CSV_FILE = "篮球.csv"
```

程序只输出到终端，不额外生成结果文件。`output.md` 是本次批量验证保存的汇总结果。
