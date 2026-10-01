# Sustainability 模型 21 个项目验证结果

## 结果口径

- 本结果使用 `resource_consumption_index` 和 `carbon_emissions_index` 两个 `0–1` 的高影响代理指数；指数越高，表示资源和碳排放影响越大。
- 资源指数依据体育项目的场馆/设施类型进行 0–1 代理编码：室外开放场地较低，室内场馆和涉水项目较高。
- 碳指数使用全球参与国家数 `N` 作为旅行与赛事规模代理：`C = min(1, 0.10 + 0.90 × N/215)`。
- 所有结果均为 `coverage_status=partial`，不是场馆水表和电表实测值；应作为模型验证的代理数据，而不是 IOC 最终事实判断。
- 两个因子权重默认各为 `0.50`；由于每个 CSV 只有一个 SDE，逐项运行时熵权无法独立估计，最终权重为固定权重。
- 最终 `S = 0.50 × (1 − resource_index) + 0.50 × (1 − carbon_index)`，阈值 `S ≥ 0.60`。
- 用户清单中的 Fencing 重复一次，已合并为一个项目，因此共 21 个唯一项目、21 个 CSV。

## 汇总表

| 项目 | N代理 | Resource index | Carbon index | S_resource | S_carbon | S | Final |
|---|---:|---:|---:|---:|---:|---:|---|
| 腰旗橄榄球 | 79 | 0.3500 | 0.4307 | 0.6500 | 0.5693 | 0.6097 | True |
| 六人制长曲棍球 | 91 | 0.4000 | 0.4809 | 0.6000 | 0.5191 | 0.5595 | False |
| 霹雳舞 | 80 | 0.5500 | 0.4349 | 0.4500 | 0.5651 | 0.5075 | False |
| 板球 | 119 | 0.5500 | 0.5981 | 0.4500 | 0.4019 | 0.4259 | False |
| 场地曲棍球 | 132 | 0.6000 | 0.6526 | 0.4000 | 0.3474 | 0.3737 | False |
| 壁球 | 112 | 0.7500 | 0.5688 | 0.2500 | 0.4312 | 0.3406 | False |
| 射击 | 150 | 0.6000 | 0.7279 | 0.4000 | 0.2721 | 0.3361 | False |
| 现代五项 | 118 | 0.8000 | 0.5940 | 0.2000 | 0.4060 | 0.3030 | False |
| 击剑 | 159 | 0.6500 | 0.7656 | 0.3500 | 0.2344 | 0.2922 | False |
| 网球 | 206 | 0.5000 | 0.9623 | 0.5000 | 0.0377 | 0.2688 | False |
| 足球 | 201 | 0.5500 | 0.9414 | 0.4500 | 0.0586 | 0.2543 | False |
| 田径 | 215 | 0.5000 | 1.0000 | 0.5000 | 0.0000 | 0.2500 | False |
| 举重 | 180 | 0.6500 | 0.8535 | 0.3500 | 0.1465 | 0.2482 | False |
| 拳击 | 185 | 0.6500 | 0.8744 | 0.3500 | 0.1256 | 0.2378 | False |
| 羽毛球 | 181 | 0.7000 | 0.8577 | 0.3000 | 0.1423 | 0.2212 | False |
| 空手道 | 198 | 0.6500 | 0.9288 | 0.3500 | 0.0712 | 0.2106 | False |
| 柔道 | 205 | 0.6500 | 0.9581 | 0.3500 | 0.0419 | 0.1960 | False |
| 篮球 | 204 | 0.7000 | 0.9540 | 0.3000 | 0.0460 | 0.1730 | False |
| 场馆自行车 | 215 | 0.8000 | 1.0000 | 0.2000 | 0.0000 | 0.1000 | False |
| 跳水 | 211 | 0.9000 | 0.9833 | 0.1000 | 0.0167 | 0.0583 | False |
| 游泳 | 212 | 0.9000 | 0.9874 | 0.1000 | 0.0126 | 0.0563 | False |

## 逐项结果

### 拳击 (BOXING)

- Resource impact index: `0.6500`；Resource factor score: `0.3500`
- Carbon impact index: `0.8744`；Carbon factor score: `0.1256`
- Sustainability score `S`: `0.2378`
- Pass at `S ≥ 0.60`: `False`

### 霹雳舞 (BREAKING)

- Resource impact index: `0.5500`；Resource factor score: `0.4500`
- Carbon impact index: `0.4349`；Carbon factor score: `0.5651`
- Sustainability score `S`: `0.5075`
- Pass at `S ≥ 0.60`: `False`

### 空手道 (KARATE)

- Resource impact index: `0.6500`；Resource factor score: `0.3500`
- Carbon impact index: `0.9288`；Carbon factor score: `0.0712`
- Sustainability score `S`: `0.2106`
- Pass at `S ≥ 0.60`: `False`

### 板球 (CRICKET)

- Resource impact index: `0.5500`；Resource factor score: `0.4500`
- Carbon impact index: `0.5981`；Carbon factor score: `0.4019`
- Sustainability score `S`: `0.4259`
- Pass at `S ≥ 0.60`: `False`

### 腰旗橄榄球 (FLAG_FOOTBALL)

- Resource impact index: `0.3500`；Resource factor score: `0.6500`
- Carbon impact index: `0.4307`；Carbon factor score: `0.5693`
- Sustainability score `S`: `0.6097`
- Pass at `S ≥ 0.60`: `True`

### 壁球 (SQUASH)

- Resource impact index: `0.7500`；Resource factor score: `0.2500`
- Carbon impact index: `0.5688`；Carbon factor score: `0.4312`
- Sustainability score `S`: `0.3406`
- Pass at `S ≥ 0.60`: `False`

### 六人制长曲棍球 (LACROSSE_SIXES)

- Resource impact index: `0.4000`；Resource factor score: `0.6000`
- Carbon impact index: `0.4809`；Carbon factor score: `0.5191`
- Sustainability score `S`: `0.5595`
- Pass at `S ≥ 0.60`: `False`

### 场馆自行车 (TRACK_CYCLING)

- Resource impact index: `0.8000`；Resource factor score: `0.2000`
- Carbon impact index: `1.0000`；Carbon factor score: `0.0000`
- Sustainability score `S`: `0.1000`
- Pass at `S ≥ 0.60`: `False`

### 田径 (ATHLETICS)

- Resource impact index: `0.5000`；Resource factor score: `0.5000`
- Carbon impact index: `1.0000`；Carbon factor score: `0.0000`
- Sustainability score `S`: `0.2500`
- Pass at `S ≥ 0.60`: `False`

### 击剑 (FENCING)

- Resource impact index: `0.6500`；Resource factor score: `0.3500`
- Carbon impact index: `0.7656`；Carbon factor score: `0.2344`
- Sustainability score `S`: `0.2922`
- Pass at `S ≥ 0.60`: `False`

### 游泳 (SWIMMING)

- Resource impact index: `0.9000`；Resource factor score: `0.1000`
- Carbon impact index: `0.9874`；Carbon factor score: `0.0126`
- Sustainability score `S`: `0.0563`
- Pass at `S ≥ 0.60`: `False`

### 柔道 (JUDO)

- Resource impact index: `0.6500`；Resource factor score: `0.3500`
- Carbon impact index: `0.9581`；Carbon factor score: `0.0419`
- Sustainability score `S`: `0.1960`
- Pass at `S ≥ 0.60`: `False`

### 现代五项 (MODERN_PENTATHLON)

- Resource impact index: `0.8000`；Resource factor score: `0.2000`
- Carbon impact index: `0.5940`；Carbon factor score: `0.4060`
- Sustainability score `S`: `0.3030`
- Pass at `S ≥ 0.60`: `False`

### 射击 (SHOOTING)

- Resource impact index: `0.6000`；Resource factor score: `0.4000`
- Carbon impact index: `0.7279`；Carbon factor score: `0.2721`
- Sustainability score `S`: `0.3361`
- Pass at `S ≥ 0.60`: `False`

### 羽毛球 (BADMINTON)

- Resource impact index: `0.7000`；Resource factor score: `0.3000`
- Carbon impact index: `0.8577`；Carbon factor score: `0.1423`
- Sustainability score `S`: `0.2212`
- Pass at `S ≥ 0.60`: `False`

### 举重 (WEIGHTLIFTING)

- Resource impact index: `0.6500`；Resource factor score: `0.3500`
- Carbon impact index: `0.8535`；Carbon factor score: `0.1465`
- Sustainability score `S`: `0.2482`
- Pass at `S ≥ 0.60`: `False`

### 网球 (TENNIS)

- Resource impact index: `0.5000`；Resource factor score: `0.5000`
- Carbon impact index: `0.9623`；Carbon factor score: `0.0377`
- Sustainability score `S`: `0.2688`
- Pass at `S ≥ 0.60`: `False`

### 足球 (FOOTBALL)

- Resource impact index: `0.5500`；Resource factor score: `0.4500`
- Carbon impact index: `0.9414`；Carbon factor score: `0.0586`
- Sustainability score `S`: `0.2543`
- Pass at `S ≥ 0.60`: `False`

### 篮球 (BASKETBALL)

- Resource impact index: `0.7000`；Resource factor score: `0.3000`
- Carbon impact index: `0.9540`；Carbon factor score: `0.0460`
- Sustainability score `S`: `0.1730`
- Pass at `S ≥ 0.60`: `False`

### 跳水 (DIVING)

- Resource impact index: `0.9000`；Resource factor score: `0.1000`
- Carbon impact index: `0.9833`；Carbon factor score: `0.0167`
- Sustainability score `S`: `0.0583`
- Pass at `S ≥ 0.60`: `False`

### 场地曲棍球 (FIELD_HOCKEY)

- Resource impact index: `0.6000`；Resource factor score: `0.4000`
- Carbon impact index: `0.6526`；Carbon factor score: `0.3474`
- Sustainability score `S`: `0.3737`
- Pass at `S ≥ 0.60`: `False`
