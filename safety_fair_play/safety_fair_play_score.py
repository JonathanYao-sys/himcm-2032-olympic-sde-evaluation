# -*- coding: utf-8 -*-
"""
Safety and Fair Play 指标得分计算程序

三个组成变量:
1. doping_screening: 兴奋剂筛查 (0/1 二值指标)
2. injury_incidence_rate: 运动损伤发生率 (0-1 连续值, 从网站获取)
3. fairness_in_enforcement: 执法公平性 (0/1 二值指标)

权重和各运动数据由用户在下方配置区填写。
"""

import re

# requests 和 BeautifulSoup 仅用于从网站抓取 injury rate
# 如果已手动填写数据, 缺少这两个库也不影响程序运行
try:
    import requests
    from bs4 import BeautifulSoup
    _WEB_SCRAPING_AVAILABLE = True
except ImportError:
    _WEB_SCRAPING_AVAILABLE = False


# ============================================================
#  ⬇⬇⬇  权重配置区 — 请在此处填写你计算好的权重  ⬇⬇⬇
# ============================================================
# 三个指标的权重, 顺序: [兴奋剂筛查, 运动损伤发生率, 执法公平性]
# 权重之和应为 1, 程序会自动归一化
WEIGHTS = [0.0, 0.4489, 0.5511]   # TODO: 替换为你计算好的权重
# ============================================================
#  ⬆⬆⬆  权重配置区结束  ⬆⬆⬆
# ============================================================


# ============================================================
#  ⬇⬇⬇  各运动数据配置区 — 请在此处填写各运动的数据  ⬇⬇⬇
# ============================================================
# 每个运动项目一行, 格式: {"name": "运动名称", "doping": 0或1, "injury_rate": 0-1的值, "fairness": 0或1}
# - doping: 兴奋剂筛查, 1 = 通过/合规, 0 = 未通过/不合规
# - injury_rate: 运动损伤发生率, 0-1 之间的小数 (如 0.25 表示 25%)
# - fairness: 执法公平性, 1 = 公平, 0 = 不公平
SPORTS_DATA = [
    {"name": "Boxing",             "doping": 1, "injury_rate": 0.6583, "fairness": 1},
    {"name": "Breaking",           "doping": 1, "injury_rate": 0.2183, "fairness": 0},
    {"name": "Karate",             "doping": 1, "injury_rate": 0.5333, "fairness": 1},
    {"name": "Cricket",            "doping": 1, "injury_rate": 1.0000, "fairness": 1},
    {"name": "Flag football",      "doping": 1, "injury_rate": 0.3083, "fairness": 1},
    {"name": "Squash",             "doping": 1, "injury_rate": 0.5917, "fairness": 1},
    {"name": "Lacrosse Sixes",     "doping": 1, "injury_rate": 0.2667, "fairness": 1},
    {"name": "Cycling track",      "doping": 1, "injury_rate": 0.1500, "fairness": 1},
    {"name": "Athletics",          "doping": 1, "injury_rate": 0.2750, "fairness": 1},
    {"name": "Fencing",            "doping": 1, "injury_rate": 0.1167, "fairness": 1},
    {"name": "Swimming",           "doping": 1, "injury_rate": 0.0333, "fairness": 1},
    {"name": "Judo",               "doping": 1, "injury_rate": 0.5583, "fairness": 1},
    {"name": "Modern Pentathlon",  "doping": 1, "injury_rate": 0.3250, "fairness": 1},
    {"name": "Shooting",           "doping": 1, "injury_rate": 0.0000, "fairness": 1},
    {"name": "Badminton",          "doping": 1, "injury_rate": 0.4167, "fairness": 1},
    {"name": "Weightlifting",      "doping": 1, "injury_rate": 0.4833, "fairness": 0},
    {"name": "Tennis",             "doping": 1, "injury_rate": 0.3917, "fairness": 1},
    {"name": "Football",           "doping": 1, "injury_rate": 0.7417, "fairness": 1},
    {"name": "Basketball",         "doping": 1, "injury_rate": 0.8167, "fairness": 1},
    {"name": "Diving",             "doping": 1, "injury_rate": 0.0750, "fairness": 0},
    {"name": "Field Hockey",       "doping": 1, "injury_rate": 0.6167, "fairness": 1},
]
# ============================================================
#  ⬆⬆⬆  各运动数据配置区结束  ⬆⬆⬆
# ============================================================


# 指标名称
INDICATOR_NAMES = [
    "doping_screening (兴奋剂筛查)",
    "injury_incidence_rate (运动损伤发生率)",
    "fairness_in_enforcement (执法公平性)"
]


def _normalize_weights(weights):
    """将权重归一化, 确保和为 1"""
    total = sum(weights)
    if total == 0:
        raise ValueError("权重之和不能为 0")
    return [w / total for w in weights]


# 程序启动时自动归一化权重
WEIGHTS = _normalize_weights(WEIGHTS)


# ============================================================
# 1. 从网站获取运动损伤发生率
# ============================================================

def fetch_injury_incidence_rate(url=None, css_selector=None, fallback_value=0.3):
    """
    从指定网站获取运动损伤发生率 (incidence rate of sports injuries)

    参数:
        url: 网站 URL, 若为 None 则使用默认示例 URL
        css_selector: 提取数值的 CSS 选择器, 若为 None 则尝试关键词匹配
        fallback_value: 网络请求失败时的默认值 (0-1)

    返回:
        rate: float, 运动损伤发生率 (0-1 之间)
    """
    if not _WEB_SCRAPING_AVAILABLE:
        print(f"[提示] 未安装 requests/beautifulsoup4, 跳过网页抓取, 使用默认值 {fallback_value}")
        print(f"       如需从网站抓取数据, 请运行: pip install requests beautifulsoup4")
        return fallback_value

    if url is None:
        url = "https://example.com/sports-injury-rate"

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        if css_selector:
            element = soup.select_one(css_selector)
            if element:
                text = element.get_text(strip=True)
                rate = _parse_rate_from_text(text)
                if rate is not None:
                    return max(0.0, min(1.0, rate))

        for keyword in ["incidence", "injury rate", "损伤发生率", "发生率"]:
            elements = soup.find_all(string=lambda t: t and keyword.lower() in t.lower())
            for elem in elements:
                rate = _parse_rate_from_text(elem)
                if rate is not None:
                    return max(0.0, min(1.0, rate))

        print(f"[警告] 未能从网页中解析出损伤发生率, 使用默认值 {fallback_value}")
        return fallback_value

    except Exception as e:
        print(f"[警告] 获取运动损伤发生率失败: {e}, 使用默认值 {fallback_value}")
        return fallback_value


def _parse_rate_from_text(text):
    """从文本中解析数值, 支持百分比 (如 35%) 和小数 (如 0.35)"""
    pct_match = re.search(r"(\d+\.?\d*)\s*%", text)
    if pct_match:
        return float(pct_match.group(1)) / 100.0

    decimal_match = re.search(r"(0\.\d+|1\.0|1\.00)", text)
    if decimal_match:
        return float(decimal_match.group(1))

    return None


# ============================================================
# 2. Safety and Fair Play 得分计算
# ============================================================

def calculate_safety_fair_play_score(doping_screening, injury_incidence_rate,
                                     fairness_in_enforcement, return_details=False):
    """
    计算 Safety and Fair Play 综合得分

    参数:
        doping_screening: int/float, 兴奋剂筛查 (0 或 1)
        injury_incidence_rate: float, 运动损伤发生率 (0-1)
        fairness_in_enforcement: int/float, 执法公平性 (0 或 1)
        return_details: bool, 是否返回详细信息

    返回:
        score: float, 综合得分 (0-100)
        details: dict (仅当 return_details=True 时)
    """
    values = [
        float(doping_screening),
        float(injury_incidence_rate),
        float(fairness_in_enforcement)
    ]

    # 正向化: 运动损伤发生率是负向指标, 转为 1 - rate
    values_forward = values.copy()
    values_forward[1] = 1.0 - values_forward[1]

    # 加权求和
    score_normalized = sum(w * v for w, v in zip(WEIGHTS, values_forward))
    score = score_normalized * 100.0

    if return_details:
        details = {
            "weights": WEIGHTS,
            "indicators": [
                {
                    "name": INDICATOR_NAMES[0],
                    "value": values[0],
                    "weight": WEIGHTS[0],
                    "weighted_score": WEIGHTS[0] * values_forward[0] * 100
                },
                {
                    "name": INDICATOR_NAMES[1],
                    "value": values[1],
                    "value_forward": values_forward[1],
                    "weight": WEIGHTS[1],
                    "weighted_score": WEIGHTS[1] * values_forward[1] * 100
                },
                {
                    "name": INDICATOR_NAMES[2],
                    "value": values[2],
                    "weight": WEIGHTS[2],
                    "weighted_score": WEIGHTS[2] * values_forward[2] * 100
                }
            ],
            "total_score": score
        }
        return score, details
    return score


# ============================================================
# 3. 批量计算各运动得分
# ============================================================

def calculate_all_sports(sports_data):
    """
    批量计算所有运动项目的 Safety and Fair Play 得分, 并按得分降序排列

    参数:
        sports_data: list of dict, 每个 dict 包含 name, doping, injury_rate, fairness

    返回:
        results: list of dict, 每个 dict 包含运动名称、各指标值、得分
    """
    results = []
    for sport in sports_data:
        score, details = calculate_safety_fair_play_score(
            doping_screening=sport["doping"],
            injury_incidence_rate=sport["injury_rate"],
            fairness_in_enforcement=sport["fairness"],
            return_details=True
        )
        results.append({
            "name": sport["name"],
            "doping": sport["doping"],
            "injury_rate": sport["injury_rate"],
            "fairness": sport["fairness"],
            "score": score,
            "details": details
        })

    # 按得分降序排列
    results.sort(key=lambda x: x["score"], reverse=True)
    return results


def print_results_table(results):
    """以表格形式打印所有运动的得分结果"""
    print("=" * 85)
    print(f"{'排名':<6}{'运动名称':<12}{'兴奋剂筛查':<12}{'损伤发生率':<14}{'执法公平性':<12}{'综合得分':<10}")
    print("-" * 85)
    for rank, r in enumerate(results, 1):
        print(f"{rank:<6}{r['name']:<12}{r['doping']:<12}"
              f"{r['injury_rate']:<14.4f}{r['fairness']:<12}{r['score']:<10.2f}")
    print("=" * 85)


# ============================================================
# 4. 主程序
# ============================================================

if __name__ == "__main__":
    print("=" * 85)
    print("Safety and Fair Play 指标得分计算程序")
    print("=" * 85)

    # 打印当前权重
    print("\n当前配置的权重:")
    for i, name in enumerate(INDICATOR_NAMES):
        print(f"  {name}: {WEIGHTS[i]:.4f} ({WEIGHTS[i]*100:.2f}%)")

    # 批量计算所有运动的得分
    results = calculate_all_sports(SPORTS_DATA)

    # 打印结果表格
    print(f"\n共 {len(SPORTS_DATA)} 个运动项目的计算结果 (按得分降序):\n")
    print_results_table(results)
