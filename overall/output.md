# Overall IOC Criteria Model Results

## Formula

```text
Overall = sum_k w_k * D_k
w_k = alpha * w_fixed + (1-alpha) * w_entropy
alpha = 0.50
w_fixed = 1/6 for each of six dimensions
```

## Final weights (hybrid, 0-1)

| Dimension | Fixed | Entropy | Hybrid final |
|---|---:|---:|---:|
| Popularity & Accessibility | 0.1667 | 0.4075 | 0.2871 |
| Inclusivity | 0.1667 | 0.0067 | 0.0867 |
| Fairness & Safety | 0.1667 | 0.0938 | 0.1302 |
| Sustainability | 0.1667 | 0.2842 | 0.2255 |
| Relevance & Innovation | 0.1667 | 0.2051 | 0.1859 |
| Gender Equity | 0.1667 | 0.0027 | 0.0847 |

## Overall ranking

| Rank | SDE | Popularity | Inclusivity | Safety | Sustainability | Innovation | Gender | Overall | Equal rank | Entropy rank |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 田径 (Athletics) | 0.8608 | 0.9815 | 0.8765 | 0.2500 | 0.5254 | 0.9971 | 0.6848 | 1 | 1 |
| 2 | 腰旗橄榄球 (Flag Football) | 0.2461 | 0.8210 | 0.8616 | 0.6097 | 0.7678 | 1.0000 | 0.6189 | 2 | 5 |
| 3 | 游泳 (Swimming) | 0.7273 | 0.9905 | 0.9850 | 0.0563 | 0.5203 | 0.9524 | 0.6130 | 4 | 4 |
| 4 | 篮球 (Basketball) | 0.7258 | 0.9722 | 0.6334 | 0.1730 | 0.6016 | 0.9953 | 0.6102 | 5 | 2 |
| 5 | 足球 (Football) | 0.7498 | 0.9570 | 0.6670 | 0.2543 | 0.4099 | 0.9077 | 0.5955 | 7 | 3 |
| 6 | 六人制长曲棍球 (Lacrosse Sixes) | 0.1043 | 0.8374 | 0.8803 | 0.5595 | 0.8858 | 1.0000 | 0.5926 | 3 | 7 |
| 7 | 网球 (Tennis) | 0.6065 | 0.9817 | 0.8242 | 0.2688 | 0.3642 | 0.9980 | 0.5794 | 6 | 6 |
| 8 | 羽毛球 (Badminton) | 0.3790 | 0.9698 | 0.8129 | 0.2212 | 0.5305 | 0.9780 | 0.5300 | 8 | 9 |
| 9 | 霹雳舞 (Breaking) | 0.1939 | 0.7048 | 0.3509 | 0.5075 | 0.8008 | 0.9798 | 0.5087 | 14 | 8 |
| 10 | 板球 (Cricket T20) | 0.4716 | 0.8963 | 0.5511 | 0.4259 | 0.1726 | 1.0000 | 0.4976 | 17 | 10 |
| 11 | 拳击 (Boxing) | 0.4256 | 0.9886 | 0.7045 | 0.2378 | 0.3693 | 0.8112 | 0.4906 | 15 | 11 |
| 12 | 射击 (Shooting) | 0.1478 | 0.9361 | 1.0000 | 0.3361 | 0.4289 | 0.9374 | 0.4887 | 9 | 14 |
| 13 | 场馆自行车 (Cycling track) | 0.4387 | 0.9721 | 0.9327 | 0.1000 | 0.3084 | 0.8787 | 0.4859 | 12 | 12 |
| 14 | 空手道 (Karate) | 0.2639 | 0.9724 | 0.7606 | 0.2106 | 0.4873 | 0.9753 | 0.4797 | 10 | 13 |
| 15 | 柔道 (Judo) | 0.3654 | 0.9927 | 0.7494 | 0.1960 | 0.2982 | 0.9652 | 0.4699 | 13 | 15 |
| 16 | 击剑 (Fencing) | 0.1844 | 0.9301 | 0.9476 | 0.2922 | 0.2932 | 0.9967 | 0.4617 | 11 | 17 |
| 17 | 场地曲棍球 (Field Hockey) | 0.2040 | 0.9137 | 0.7231 | 0.3737 | 0.2830 | 0.9867 | 0.4523 | 18 | 16 |
| 18 | 现代五项 (Modern Pentathlon) | 0.0475 | 0.8740 | 0.8541 | 0.3030 | 0.4492 | 1.0000 | 0.4371 | 16 | 19 |
| 19 | 跳水 (Diving) | 0.4175 | 0.9703 | 0.4153 | 0.0583 | 0.3135 | 0.9760 | 0.4121 | 20 | 18 |
| 20 | 壁球 (Squash) | 0.1574 | 0.8878 | 0.7344 | 0.3406 | 0.1016 | 1.0000 | 0.3981 | 19 | 21 |
| 21 | 举重 (Weightlifting) | 0.2263 | 0.9883 | 0.2320 | 0.2482 | 0.4365 | 0.9403 | 0.3976 | 21 | 20 |

## Interpretation notes

- The overall score is a weighted multi-criteria ranking, not a direct measurement of popularity.
- The hybrid weights use an equal prior because IOC does not specify official weights for the six criteria.
- The entropy component adjusts weights according to dispersion in the available 21-SDE sample.
- Popularity & Accessibility is based on the attached image's popularity score; Accessibility is not separately measured in the input data.
- Sustainability uses the latest Sustainability submodel score S.
- The result should be accompanied by weight sensitivity analysis in the paper.
