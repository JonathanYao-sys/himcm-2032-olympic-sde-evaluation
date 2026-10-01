# Inclusivity 模型 21 个项目验证结果

## 数据口径与限制

- 当前期 `t3` 使用国际单项联合会现行国家协会/成员协会名单，作为“practicing the sport”的可核验代理。
- `t1`、`t2` 使用旧存档中的官方赛事参与记录；因此不同项目的赛事阶段并不完全同质。
- 所有记录均标记为 `coverage_status=partial`，结果应理解为代理数据下的模型验证，而非 IOC 最终事实裁定。
- `I` 与五个因子均采用 `0–1`。默认质量阈值为 `I ≥ 0.75`。
- 用户清单中的 `Fencing（击剑）` 出现两次；本批将其合并为一个项目，因此共 21 个唯一项目、21 个 CSV。
- `Final_pass = Gate_pass 且 Quality_pass`，其中 `Gate_pass` 要求当前期 `N ≥ 75` 且 `K ≥ 4`。

## 汇总表

| 组别 | 项目 | t3 N | t3 K | P | D | B | R | T | I | Gate | Quality | Final |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|
| 第一组 | 拳击 | 185 | 5 | 0.9877 | 1.0000 | 0.9683 | 0.9929 | 1.0000 | 0.9886 | True | True | True |
| 第一组 | 霹雳舞 | 80 | 5 | 0.7308 | 0.5733 | 0.7086 | 0.8611 | 0.7783 | 0.7048 | True | False | False |
| 第一组 | 空手道 | 198 | 5 | 0.9959 | 0.9733 | 0.9527 | 0.9859 | 0.9133 | 0.9724 | True | True | True |
| 第二组 | 板球 | 119 | 5 | 0.8893 | 0.9067 | 0.9418 | 0.9664 | 0.7333 | 0.8963 | True | True | True |
| 第二组 | 腰旗橄榄球 | 79 | 5 | 0.7249 | 0.8400 | 0.9423 | 0.9806 | 0.7072 | 0.8210 | True | True | True |
| 第二组 | 壁球 | 112 | 5 | 0.8692 | 0.9067 | 0.9296 | 0.9479 | 0.7622 | 0.8878 | True | True | True |
| 第二组 | 六人制长曲棍球 | 91 | 5 | 0.7886 | 0.8400 | 0.9030 | 0.9283 | 0.7800 | 0.8374 | True | True | True |
| 第三组 | 场馆自行车 | 215 | 5 | 1.0000 | 1.0000 | 0.9610 | 0.9791 | 0.8200 | 0.9721 | True | True | True |
| 第三组 | 田径 | 215 | 5 | 1.0000 | 1.0000 | 0.9757 | 0.9838 | 0.8800 | 0.9815 | True | True | True |
| 第三组 | 击剑 | 159 | 5 | 0.9633 | 0.8933 | 0.9296 | 0.9769 | 0.8600 | 0.9301 | True | True | True |
| 第三组 | 游泳 | 212 | 5 | 1.0000 | 1.0000 | 0.9617 | 0.9814 | 1.0000 | 0.9905 | True | True | True |
| 第三组 | 柔道 | 205 | 5 | 0.9995 | 1.0000 | 0.9690 | 0.9908 | 1.0000 | 0.9927 | True | True | True |
| 第三组 | 现代五项 | 118 | 5 | 0.8866 | 0.8400 | 0.8899 | 0.9596 | 0.7978 | 0.8740 | True | True | True |
| 第三组 | 射击 | 150 | 5 | 0.9514 | 0.9067 | 0.9002 | 0.9645 | 1.0000 | 0.9361 | True | True | True |
| 第三组 | 羽毛球 | 181 | 5 | 0.9847 | 0.9867 | 0.9595 | 0.9947 | 0.8711 | 0.9698 | True | True | True |
| 第三组 | 举重 | 180 | 5 | 0.9839 | 1.0000 | 0.9756 | 0.9930 | 0.9956 | 0.9883 | True | True | True |
| 第三组 | 网球 | 206 | 5 | 1.0000 | 1.0000 | 0.9715 | 0.9853 | 0.8889 | 0.9817 | True | True | True |
| 第三组 | 足球 | 201 | 5 | 0.9975 | 0.9600 | 0.9480 | 0.9738 | 0.8089 | 0.9570 | True | True | True |
| 第三组 | 篮球 | 204 | 5 | 0.9990 | 1.0000 | 0.9712 | 0.9917 | 0.7911 | 0.9722 | True | True | True |
| 第三组 | 跳水 | 211 | 5 | 1.0000 | 1.0000 | 0.9617 | 0.9817 | 0.7978 | 0.9703 | True | True | True |
| 第三组 | 场地曲棍球 | 132 | 5 | 0.9201 | 0.9200 | 0.9486 | 0.9859 | 0.7333 | 0.9137 | True | True | True |

## 逐项观测期结果

### 拳击

- 当前期：N=185，K=5，coverage=partial
- 第1期：2016 Olympic/World activity evidence；N=76，K=5，coverage=partial，计入T=True
- 第2期：2020 Olympic/World activity evidence；N=80，K=5，coverage=partial，计入T=True
- 第3期：2024-2025 IF membership/practice proxy；N=185，K=5，coverage=partial，计入T=True
- 因子：P=0.9877，D=1.0000，B=0.9683，R=0.9929，T=1.0000
- I=0.9886；Gate=True；Quality=True；Final=True

### 霹雳舞

- 当前期：N=80，K=5，coverage=partial
- 第1期：2019 WDSF World Championship；N=58，K=5，coverage=partial，计入T=True
- 第2期：2021 WDSF World Championship；N=11，K=3，coverage=partial，计入T=True
- 第3期：2024-2025 WDSF membership/practice proxy；N=80，K=5，coverage=partial，计入T=True
- 因子：P=0.7308，D=0.5733，B=0.7086，R=0.8611，T=0.7783
- I=0.7048；Gate=True；Quality=False；Final=False

### 空手道

- 当前期：N=198，K=5，coverage=partial
- 第1期：2016 WKF World Championships；N=107，K=5，coverage=partial，计入T=True
- 第2期：2020 Olympic Karate；N=36，K=5，coverage=partial，计入T=True
- 第3期：2024-2025 WKF membership/practice proxy；N=198，K=5，coverage=partial，计入T=True
- 因子：P=0.9959，D=0.9733，B=0.9527，R=0.9859，T=0.9133
- I=0.9724；Gate=True；Quality=True；Final=True

### 板球

- 当前期：N=119，K=5，coverage=partial
- 第1期：2016 ICC World Twenty20；N=15，K=5，coverage=partial，计入T=True
- 第2期：2021 ICC Men’s T20 World Cup；N=15，K=5，coverage=partial，计入T=True
- 第3期：2024 ICC membership/practice proxy；N=119，K=5，coverage=partial，计入T=True
- 因子：P=0.8893，D=0.9067，B=0.9418，R=0.9664，T=0.7333
- I=0.8963；Gate=True；Quality=True；Final=True

### 腰旗橄榄球

- 当前期：N=79，K=5，coverage=partial
- 第1期：2016 IFAF World Championship；N=15，K=4，coverage=partial，计入T=True
- 第2期：2021 IFAF World Championship；N=22，K=3，coverage=partial，计入T=True
- 第3期：2024-2025 IFAF membership/practice proxy；N=79，K=5，coverage=partial，计入T=True
- 因子：P=0.7249，D=0.8400，B=0.9423，R=0.9806，T=0.7072
- I=0.8210；Gate=True；Quality=True；Final=True

### 壁球

- 当前期：N=112，K=5，coverage=partial
- 第1期：2017 World Team Squash Championship；N=22，K=5，coverage=partial，计入T=True
- 第2期：2019 World Team Squash Championship；N=21，K=5，coverage=partial，计入T=True
- 第3期：2024-2025 WSF membership/practice proxy；N=112，K=5，coverage=partial，计入T=True
- 因子：P=0.8692，D=0.9067，B=0.9296，R=0.9479，T=0.7622
- I=0.8878；Gate=True；Quality=True；Final=True

### 六人制长曲棍球

- 当前期：N=91，K=5，coverage=partial
- 第2期：2022 World Games Lacrosse Sixes；N=9，K=4，coverage=partial，计入T=True
- 第3期：2024-2025 World Lacrosse membership/practice proxy；N=91，K=5，coverage=partial，计入T=True
- 因子：P=0.7886，D=0.8400，B=0.9030，R=0.9283，T=0.7800
- I=0.8374；Gate=True；Quality=True；Final=True

### 场馆自行车

- 当前期：N=215，K=5，coverage=partial
- 第1期：2016 Olympic track cycling；N=34，K=5，coverage=partial，计入T=True
- 第2期：2020 Olympic track cycling；N=35，K=5，coverage=partial，计入T=True
- 第3期：2024-2025 UCI membership/practice proxy；N=215，K=5，coverage=partial，计入T=True
- 因子：P=1.0000，D=1.0000，B=0.9610，R=0.9791，T=0.8200
- I=0.9721；Gate=True；Quality=True；Final=True

### 田径

- 当前期：N=215，K=5，coverage=partial
- 第1期：2016 Olympic athletics；N=48，K=5，coverage=partial，计入T=True
- 第2期：2020 Olympic athletics；N=48，K=5，coverage=partial，计入T=True
- 第3期：2024-2025 World Athletics membership/practice proxy；N=215，K=5，coverage=partial，计入T=True
- 因子：P=1.0000，D=1.0000，B=0.9757，R=0.9838，T=0.8800
- I=0.9815；Gate=True；Quality=True；Final=True

### 击剑

- 当前期：N=159，K=5，coverage=partial
- 第1期：2016 Olympic fencing；N=45，K=4，coverage=partial，计入T=True
- 第2期：2020 Olympic fencing；N=42，K=4，coverage=partial，计入T=True
- 第3期：2024-2025 FIE membership/practice proxy；N=159，K=5，coverage=partial，计入T=True
- 因子：P=0.9633，D=0.8933，B=0.9296，R=0.9769，T=0.8600
- I=0.9301；Gate=True；Quality=True；Final=True

### 游泳

- 当前期：N=212，K=5，coverage=partial
- 第1期：2016 Olympic swimming；N=188，K=5，coverage=partial，计入T=True
- 第2期：2020 Olympic swimming；N=188，K=5，coverage=partial，计入T=True
- 第3期：2024-2025 World Aquatics membership/practice proxy；N=212，K=5，coverage=partial，计入T=True
- 因子：P=1.0000，D=1.0000，B=0.9617，R=0.9814，T=1.0000
- I=0.9905；Gate=True；Quality=True；Final=True

### 柔道

- 当前期：N=205，K=5，coverage=partial
- 第1期：2016 Olympic judo；N=136，K=5，coverage=partial，计入T=True
- 第2期：2020 Olympic judo；N=127，K=5，coverage=partial，计入T=True
- 第3期：2024-2025 IJF membership/practice proxy；N=205，K=5，coverage=partial，计入T=True
- 因子：P=0.9995，D=1.0000，B=0.9690，R=0.9908，T=1.0000
- I=0.9927；Gate=True；Quality=True；Final=True

### 现代五项

- 当前期：N=118，K=5，coverage=partial
- 第1期：2016 Olympic modern pentathlon；N=28，K=5，coverage=partial，计入T=True
- 第2期：2020 Olympic modern pentathlon；N=31，K=5，coverage=partial，计入T=True
- 第3期：2024-2025 UIPM membership/practice proxy；N=118，K=5，coverage=partial，计入T=True
- 因子：P=0.8866，D=0.8400，B=0.8899，R=0.9596，T=0.7978
- I=0.8740；Gate=True；Quality=True；Final=True

### 射击

- 当前期：N=150，K=5，coverage=partial
- 第1期：2016 Olympic shooting；N=91，K=5，coverage=partial，计入T=True
- 第2期：2020 Olympic shooting；N=90，K=5，coverage=partial，计入T=True
- 第3期：2024-2025 ISSF membership/practice proxy；N=150，K=5，coverage=partial，计入T=True
- 因子：P=0.9514，D=0.9067，B=0.9002，R=0.9645，T=1.0000
- I=0.9361；Gate=True；Quality=True；Final=True

### 羽毛球

- 当前期：N=181，K=5，coverage=partial
- 第1期：2016 Olympic badminton；N=46，K=5，coverage=partial，计入T=True
- 第2期：2020 Olympic badminton；N=46，K=5，coverage=partial，计入T=True
- 第3期：2024-2025 BWF membership/practice proxy；N=181，K=5，coverage=partial，计入T=True
- 因子：P=0.9847，D=0.9867，B=0.9595，R=0.9947，T=0.8711
- I=0.9698；Gate=True；Quality=True；Final=True

### 举重

- 当前期：N=180，K=5，coverage=partial
- 第1期：2016 Olympic weightlifting；N=96，K=5，coverage=partial，计入T=True
- 第2期：2020 Olympic weightlifting；N=73，K=5，coverage=partial，计入T=True
- 第3期：2024-2025 IWF membership/practice proxy；N=180，K=5，coverage=partial，计入T=True
- 因子：P=0.9839，D=1.0000，B=0.9756，R=0.9930，T=0.9956
- I=0.9883；Gate=True；Quality=True；Final=True

### 网球

- 当前期：N=206，K=5，coverage=partial
- 第1期：2016 Olympic tennis；N=55，K=5，coverage=partial，计入T=True
- 第2期：2020 Olympic tennis；N=45，K=5，coverage=partial，计入T=True
- 第3期：2024-2025 ITF membership/practice proxy；N=206，K=5，coverage=partial，计入T=True
- 因子：P=1.0000，D=1.0000，B=0.9715，R=0.9853，T=0.8889
- I=0.9817；Gate=True；Quality=True；Final=True

### 足球

- 当前期：N=201，K=5，coverage=partial
- 第1期：2014 FIFA World Cup；N=32，K=5，coverage=partial，计入T=True
- 第2期：2018 FIFA World Cup；N=32，K=5，coverage=partial，计入T=True
- 第3期：2024 FIFA membership/practice proxy；N=201，K=5，coverage=partial，计入T=True
- 因子：P=0.9975，D=0.9600，B=0.9480，R=0.9738，T=0.8089
- I=0.9570；Gate=True；Quality=True；Final=True

### 篮球

- 当前期：N=204，K=5，coverage=partial
- 第1期：2014 FIBA World Cup；N=24，K=5，coverage=partial，计入T=True
- 第2期：2019 FIBA World Cup；N=32，K=5，coverage=partial，计入T=True
- 第3期：2024-2025 FIBA membership/practice proxy；N=204，K=5，coverage=partial，计入T=True
- 因子：P=0.9990，D=1.0000，B=0.9712，R=0.9917，T=0.7911
- I=0.9722；Gate=True；Quality=True；Final=True

### 跳水

- 当前期：N=211，K=5，coverage=partial
- 第1期：2016 Olympic diving；N=29，K=5，coverage=partial，计入T=True
- 第2期：2020 Olympic diving；N=30，K=5，coverage=partial，计入T=True
- 第3期：2024-2025 World Aquatics membership/practice proxy；N=211，K=5，coverage=partial，计入T=True
- 因子：P=1.0000，D=1.0000，B=0.9617，R=0.9817，T=0.7978
- I=0.9703；Gate=True；Quality=True；Final=True

### 场地曲棍球

- 当前期：N=132，K=5，coverage=partial
- 第1期：2016 Olympic hockey；N=16，K=4，coverage=partial，计入T=True
- 第2期：2020 Olympic hockey；N=14，K=5，coverage=partial，计入T=True
- 第3期：2024-2025 FIH membership/practice proxy；N=132，K=5，coverage=partial，计入T=True
- 因子：P=0.9201，D=0.9200，B=0.9486，R=0.9859，T=0.7333
- I=0.9137；Gate=True；Quality=True；Final=True
