"""酒店/餐厅数据 + 游记工具"""
HOTEL_DATA = {
    "beijing": [
        {"name": "北京王府井希尔顿", "tier": "luxury", "price": "¥1200+", "area": "王府井", "rating": 4.5},
        {"name": "北京全季酒店(前门)", "tier": "mid", "price": "¥400-600", "area": "前门", "rating": 4.3},
        {"name": "北京如家(天安门广场店)", "tier": "budget", "price": "¥200-350", "area": "前门", "rating": 4.0},
        {"name": "北京四合院客栈(南锣鼓巷)", "tier": "mid", "price": "¥500-800", "area": "南锣鼓巷", "rating": 4.4},
    ],
    "shanghai": [
        {"name": "上海外滩华尔道夫", "tier": "luxury", "price": "¥2000+", "area": "外滩", "rating": 4.7},
        {"name": "上海亚朵S(南京路)", "tier": "mid", "price": "¥500-800", "area": "南京路", "rating": 4.4},
        {"name": "上海汉庭(人民广场)", "tier": "budget", "price": "¥250-400", "area": "人民广场", "rating": 4.1},
    ],
    "chengdu": [
        {"name": "成都博舍", "tier": "luxury", "price": "¥1500+", "area": "太古里", "rating": 4.8},
        {"name": "成都亚朵(春熙路)", "tier": "mid", "price": "¥400-600", "area": "春熙路", "rating": 4.5},
        {"name": "成都背包十年青旅", "tier": "budget", "price": "¥60-100", "area": "宽窄巷子", "rating": 4.6},
    ],
    "xian": [
        {"name": "西安索菲特传奇", "tier": "luxury", "price": "¥1000+", "area": "钟楼", "rating": 4.6},
        {"name": "西安美居(钟楼)", "tier": "mid", "price": "¥300-500", "area": "钟楼", "rating": 4.3},
        {"name": "西安湘子门青旅", "tier": "budget", "price": "¥50-80", "area": "南门", "rating": 4.5},
    ],
    "guilin": [
        {"name": "桂林香格里拉", "tier": "luxury", "price": "¥800+", "area": "漓江边", "rating": 4.5},
        {"name": "阳朔芒果旅宿", "tier": "mid", "price": "¥300-500", "area": "阳朔西街", "rating": 4.4},
        {"name": "阳朔老班长青旅", "tier": "budget", "price": "¥40-70", "area": "阳朔", "rating": 4.3},
    ],
    "yunnan": [
        {"name": "大理古城安隅酒店", "tier": "luxury", "price": "¥800-1200", "area": "大理古城", "rating": 4.7},
        {"name": "丽江花间堂(四方街)", "tier": "mid", "price": "¥400-700", "area": "丽江古城", "rating": 4.5},
        {"name": "大理慢吧青旅", "tier": "budget", "price": "¥40-60", "area": "大理古城", "rating": 4.4},
    ],
}

def recommend_hotels(city: str, tier: str = "mid") -> list:
    """按城市+档次推荐酒店"""
    hotels = HOTEL_DATA.get(city, [])
    matches = [h for h in hotels if h["tier"] == tier]
    if not matches:
        matches = [h for h in hotels if h["tier"] in ["mid", "budget"]]
    return matches[:3]

def generate_travel_story(city: str, days: int, activities: list = None) -> dict:
    """生成游记模板"""
    return {
        "title": f"我在{city}的{days}天",
        "subtitle": f"一个关于{city}的旅行故事",
        "sections": [
            {"title": "出发", "content": f"坐上前往{city}的火车/飞机，心情是期待的。"},
            {"title": "探索", "content": f"在{city}的每一天都是新的发现。"},
            {"title": "美食", "content": f"当地的味道，是最深的记忆。"},
            {"title": "离开", "content": f"{days}天过得真快，{city}下次见。"},
        ]
    }
