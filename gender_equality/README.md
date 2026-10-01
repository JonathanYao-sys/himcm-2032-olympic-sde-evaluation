# Gender Equality Submodel

本目录对应 IOC 标准中的 `Gender Equity`。模型使用三个因子：

1. `X1`：当前男女运动员比例平衡；
2. `X2`：当前男女可参加项目比例；
3. `X3`：历史女子参与比例到 2032 年的线性趋势预测。

最终输出：

```text
Score ∈ [0,1]
```

分数越高，表示该 SDE 的性别平等程度越好。

## 文件结构

每个体育项目有自己独立的 CSV，文件名使用中文项目名：

```text
拳击.csv
霹雳舞.csv
空手道.csv
板球.csv
腰旗橄榄球.csv
壁球.csv
六人制长曲棍球.csv
场馆自行车.csv
田径.csv
击剑.csv
游泳.csv
柔道.csv
现代五项.csv
射击.csv
羽毛球.csv
举重.csv
网球.csv
足球.csv
篮球.csv
跳水.csv
场地曲棍球.csv
```

`gender_equality_model.py` 会自动读取目录中的所有项目 CSV，计算后生成：

```text
output.md
```

旧版的三个汇总 CSV 已移动到 `archive_aggregate/`，模型不再使用。

## 每个 CSV 的字段

每个 CSV 使用长表格式，一行表示该 SDE 的一个年份：

| 字段 | 说明 |
|---|---|
| `sde_id` | SDE 编号 |
| `sport` | SDE 名称 |
| `year` | 年份 |
| `male_athletes` | 男性运动员数 |
| `female_athletes` | 女性运动员数 |
| `male_events` | 男子项目数；只有当前期行填写 |
| `female_events` | 女子项目数；只有当前期行填写 |
| `is_current` | 1 表示当前观测期 |
| `source` | 数据来源 |
| `notes` | 数据口径和限制 |

## 因子 1：当前运动员比例平衡 X1

```text
P_i = Female_Athletes / (Male_Athletes + Female_Athletes)
X1 = 1 - 2 × |P_i - 0.5|
X1 = clip(X1, 0, 1)
```

当女性比例为 `0.5` 时，`X1 = 1`。

## 因子 2：男女项目比例 X2

```text
X2 = min(Male_Events, Female_Events)
     / max(Male_Events, Female_Events)
```

若两个项目数都为 0，则 `X2 = 0`。  
混合项目或公开项目按男子 `0.5`、女子 `0.5` 折算。

## 因子 3：历史趋势预测 X3

对每个 SDE 建立女性运动员比例与年份的线性回归：

```text
Female_Ratio = a + b × Year
```

预测 2032 年：

```text
P_2032 = clip(a + b × 2032, 0, 1)
X3 = 1 - 2 × |P_2032 - 0.5|
```

如果该项目只有一个可用年份，则使用当前 `X1` 作为 `X3`。

## 综合得分

三个因子等权：

```text
Score = (X1 + X2 + X3) / 3
```

## 数据来源

### 现有奥运项目

历史和当前数据来自 Olympedia 历届奥运会项目页：

- 2008：`https://www.olympedia.org/editions/53`
- 2012：`https://www.olympedia.org/editions/54`
- 2016：`https://www.olympedia.org/editions/59`
- 2020：`https://www.olympedia.org/editions/61`
- 2024：`https://www.olympedia.org/editions/63`

程序统计状态为 Olympic 的男子、女子和混合项目，并把每个项目的参赛人数作为运动员人数代理。

### 2028 新增项目

Cricket、Flag Football、Squash、Lacrosse Sixes 使用 LA28 项目计划中的男女平等项目和运动员配额作为代理数据：

- `https://en.wikipedia.org/wiki/2028_Summer_Olympics`
- `https://en.wikipedia.org/wiki/Cricket_at_the_2028_Summer_Olympics`
- `https://en.wikipedia.org/wiki/Flag_football_at_the_2028_Summer_Olympics`
- `https://en.wikipedia.org/wiki/Squash_at_the_2028_Summer_Olympics`

## 运行方法

```bash
cd gender_equality
python3 gender_equality_model.py
```

运行后终端会输出每个 SDE 的 `X1`、`X2`、`X3`、`Score` 和排名，并写入 `output.md`。

## 模型限制

1. Olympedia 的参赛人数按项目事件汇总，参加多个项目的运动员可能被重复计数。
2. 2028 新增项目的历史趋势使用计划性的男女配额作为代理，不是实际历史参赛数据。
3. 线性外推到 2032 年基于有限年份，不能代表未来规则变化。
4. 项目数平衡不一定等于参赛机会完全平等，还需要考虑每个项目的队伍人数和资格规则。
5. 本模型是 Gender Equality 子模型，不能单独决定 SDE 是否加入或退出奥运会。
