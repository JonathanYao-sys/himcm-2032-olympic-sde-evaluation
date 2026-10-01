# Unified Olympic SDE Evaluation Results

## Overall formula

```text
Overall_7 = w1*Popularity + w2*Inclusivity + w3*Safety
          + w4*Sustainability + w5*Innovation + w6*Gender
          + w7*ProgrammeContinuity
```

## AHP weights

| Dimension | Weight |
|---|---:|
| popularity_accessibility | 0.273341 |
| inclusivity | 0.092063 |
| safety_fair_play | 0.156795 |
| sustainability | 0.092063 |
| innovation | 0.049191 |
| gender_equality | 0.049191 |
| programme_continuity | 0.287357 |

## Ranking

| Rank | SDE | Popularity | Inclusivity | Safety | Sustainability | Innovation | Gender | Overall_6 | Overall_7 | Decision | Reality group |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| 1 | 田径 (Athletics) | 0.8608 | 0.9815 | 0.8765 | 0.2500 | 0.5254 | 0.9971 | 0.7875 | 0.8484 | RETAIN | continuous |
| 2 | 游泳 (Swimming) | 0.7273 | 0.9905 | 0.9851 | 0.0563 | 0.5203 | 0.9524 | 0.7337 | 0.8094 | RETAIN | continuous |
| 3 | 足球 (Football) | 0.7498 | 0.9570 | 0.6670 | 0.2543 | 0.4099 | 0.9077 | 0.6817 | 0.7732 | RETAIN | continuous |
| 4 | 篮球 (Basketball) | 0.7258 | 0.9722 | 0.6334 | 0.1730 | 0.6016 | 0.9953 | 0.6759 | 0.7690 | RETAIN | continuous |
| 5 | 网球 (Tennis) | 0.6065 | 0.9817 | 0.8242 | 0.2688 | 0.3642 | 0.9980 | 0.6703 | 0.7645 | RETAIN | continuous |
| 6 | 场馆自行车 (Cycling Track) | 0.4387 | 0.9721 | 0.9327 | 0.1000 | 0.3084 | 0.8787 | 0.5955 | 0.7106 | RETAIN | continuous |
| 7 | 羽毛球 (Badminton) | 0.3790 | 0.9698 | 0.8129 | 0.2212 | 0.5305 | 0.9780 | 0.5836 | 0.7022 | RETAIN | continuous |
| 8 | 柔道 (Judo) | 0.3654 | 0.9927 | 0.7494 | 0.1960 | 0.2982 | 0.9652 | 0.5470 | 0.6763 | RETAIN | continuous |
| 9 | 射击 (Shooting) | 0.1478 | 0.9362 | 1.0000 | 0.3361 | 0.4289 | 0.9374 | 0.5379 | 0.6689 | RETAIN | continuous |
| 10 | 击剑 (Fencing) | 0.1844 | 0.9301 | 0.9476 | 0.2922 | 0.2932 | 0.9967 | 0.5284 | 0.6623 | RETAIN | continuous |
| 11 | 场地曲棍球 (Field Hockey) | 0.2040 | 0.9137 | 0.7231 | 0.3737 | 0.2830 | 0.9867 | 0.4927 | 0.6375 | RETAIN | continuous |
| 12 | 跳水 (Diving) | 0.4175 | 0.9703 | 0.4153 | 0.0584 | 0.3135 | 0.9760 | 0.4734 | 0.6247 | RETAIN | continuous |
| 13 | 现代五项 (Modern Pentathlon) | 0.0475 | 0.8740 | 0.8541 | 0.3030 | 0.4492 | 1.0000 | 0.4607 | 0.6139 | RETAIN | continuous |
| 14 | 举重 (Weightlifting) | 0.2263 | 0.9883 | 0.2320 | 0.2482 | 0.4365 | 0.9403 | 0.3925 | 0.5672 | RETAIN | continuous |
| 15 | 腰旗橄榄球 (Flag Football) | 0.2461 | 0.8210 | 0.8616 | 0.6097 | 0.7678 | 1.0000 | 0.5927 | 0.5216 | CONDITIONAL_RETAIN | new |
| 16 | 板球 (Cricket T20) | 0.4716 | 0.8963 | 0.5511 | 0.4259 | 0.1726 | 1.0000 | 0.5540 | 0.4953 | CONDITIONAL_RETAIN | new |
| 17 | 六人制长曲棍球 (Lacrosse Sixes) | 0.1043 | 0.8374 | 0.8803 | 0.5595 | 0.8858 | 1.0000 | 0.5467 | 0.4885 | CONDITIONAL_RETAIN | new |
| 18 | 壁球 (Squash) | 0.1574 | 0.8878 | 0.7344 | 0.3406 | 0.1016 | 1.0000 | 0.4583 | 0.4260 | CONDITIONAL_RETAIN | new |
| 19 | 拳击 (Boxing) | 0.4256 | 0.9886 | 0.7045 | 0.2378 | 0.3693 | 0.8112 | 0.5590 | 0.3978 | REMOVE_CANDIDATE | removed |
| 20 | 空手道 (Karate) | 0.2639 | 0.9724 | 0.7606 | 0.2106 | 0.4873 | 0.9753 | 0.5239 | 0.3722 | REMOVE_CANDIDATE | removed |
| 21 | 霹雳舞 (Breaking) | 0.1939 | 0.7048 | 0.3509 | 0.5075 | 0.8008 | 0.9798 | 0.4316 | 0.3072 | REMOVE_CANDIDATE | removed |

## Notes

- Programme continuity is a policy/history prior used to align the model with the requested reality-based grouping.
- Overall_6 excludes programme continuity; Overall_7 includes it.
- Popularity uses C1-C5. The cost proxy is kept in the input but not added again to Sustainability.
- Inclusivity and gender inputs are precomputed intermediate factors to keep the consolidated input one-row-per-SDE.