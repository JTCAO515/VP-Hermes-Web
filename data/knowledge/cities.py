"""中国热门旅行城市知识库"""
CITIES = {
    "beijing": {
        "name_en": "Beijing",
        "name_zh": "北京",
        "province": "北京",
        "best_season": "春秋（3-5月, 9-11月）",
        "days_min": 3,
        "days_max": 7,
        "budget_tip": "住宿偏贵，建议选胡同民宿或三环外酒店",
        "vibe": "历史厚重 + 现代首都",
        "keywords": ["故宫", "长城", "胡同", "烤鸭", "京剧", "798", "天安门"]
    },
    "shanghai": {
        "name_en": "Shanghai",
        "name_zh": "上海",
        "province": "上海",
        "best_season": "春秋（3-5月, 10-11月）",
        "days_min": 2,
        "days_max": 5,
        "budget_tip": "外滩/陆家嘴住宿贵，法租界民宿性价比高",
        "vibe": "摩登都市 + 海派文化",
        "keywords": ["外滩", "迪士尼", "法租界", "小笼包", "豫园", "陆家嘴"]
    },
    "chengdu": {
        "name_en": "Chengdu",
        "name_zh": "成都",
        "province": "四川",
        "best_season": "春秋（3-6月, 9-11月）",
        "days_min": 3,
        "days_max": 6,
        "budget_tip": "美食超便宜，住宿也很实惠",
        "vibe": "美食之都 + 悠闲慢生活",
        "keywords": ["火锅", "熊猫", "宽窄巷子", "都江堰", "串串", "茶馆"]
    },
    "xian": {
        "name_en": "Xi'an",
        "name_zh": "西安",
        "province": "陕西",
        "best_season": "春秋（3-5月, 9-10月）",
        "days_min": 2,
        "days_max": 4,
        "budget_tip": "整体消费不高，兵马俑门票稍贵",
        "vibe": "十三朝古都",
        "keywords": ["兵马俑", "古城墙", "回民街", "大雁塔", "biangbiang面"]
    },
    "guilin": {
        "name_en": "Guilin",
        "name_zh": "桂林",
        "province": "广西",
        "best_season": "4-10月（夏季注意雨季）",
        "days_min": 3,
        "days_max": 5,
        "budget_tip": "阳朔西街住宿丰俭由人",
        "vibe": "山水甲天下",
        "keywords": ["漓江", "阳朔", "象鼻山", "龙脊梯田", "十里画廊"]
    },
    "yunnan": {
        "name_en": "Yunnan",
        "name_zh": "云南",
        "province": "云南",
        "best_season": "3-10月（四季如春）",
        "days_min": 5,
        "days_max": 14,
        "budget_tip": "大理丽江民宿便宜，旺季涨价",
        "vibe": "自然风光 + 民族风情",
        "keywords": ["大理", "丽江", "香格里拉", "洱海", "玉龙雪山", "泸沽湖"]
    },
    "hangzhou": {
        "name_en": "Hangzhou",
        "name_zh": "杭州",
        "province": "浙江",
        "best_season": "3-5月, 9-11月",
        "days_min": 2,
        "days_max": 4,
        "budget_tip": "西湖附近住宿较贵，地铁沿线方便",
        "vibe": "江南水乡 + 诗意",
        "keywords": ["西湖", "断桥", "灵隐寺", "龙井茶", "宋城"]
    },
    "guangzhou": {
        "name_en": "Guangzhou",
        "name_zh": "广州",
        "province": "广东",
        "best_season": "10-12月, 2-4月",
        "days_min": 2,
        "days_max": 4,
        "budget_tip": "早茶人均50-150，住宿中等",
        "vibe": "美食之都 + 千年商都",
        "keywords": ["早茶", "小蛮腰", "沙面", "白云山", "陈家祠"]
    },
    "shenzhen": {
        "name_en": "Shenzhen",
        "name_zh": "深圳",
        "province": "广东",
        "best_season": "10-12月, 2-4月",
        "days_min": 2,
        "days_max": 4,
        "budget_tip": "住宿偏贵，餐饮选择丰富",
        "vibe": "创新之都 + 年轻城市",
        "keywords": ["世界之窗", "欢乐谷", "大梅沙", "华侨城", "华强北"]
    },
    "chongqing": {
        "name_en": "Chongqing",
        "name_zh": "重庆",
        "province": "重庆",
        "best_season": "春秋（3-5月, 9-11月）",
        "days_min": 3,
        "days_max": 5,
        "budget_tip": "性价比超高，火锅人均60-120",
        "vibe": "8D魔幻山城",
        "keywords": ["洪崖洞", "火锅", "轻轨穿楼", "磁器口", "长江索道"]
    },
    "changsha": {
        "name_en": "Changsha",
        "name_zh": "长沙",
        "province": "湖南",
        "best_season": "春秋（3-5月, 9-11月）",
        "days_min": 2,
        "days_max": 3,
        "budget_tip": "消费低，茶颜悦色必喝",
        "vibe": "娱乐之都 + 美食",
        "keywords": ["橘子洲", "岳麓山", "茶颜悦色", "臭豆腐", "文和友"]
    },
    "nanjing": {
        "name_en": "Nanjing",
        "name_zh": "南京",
        "province": "江苏",
        "best_season": "春秋（3-5月, 9-11月）",
        "days_min": 2,
        "days_max": 4,
        "budget_tip": "住宿适中，景区密集步行可达",
        "vibe": "六朝古都",
        "keywords": ["夫子庙", "中山陵", "明孝陵", "玄武湖", "鸭血粉丝汤"]
    },
    "suzhou": {
        "name_en": "Suzhou",
        "name_zh": "苏州",
        "province": "江苏",
        "best_season": "3-5月, 9-11月",
        "days_min": 2,
        "days_max": 3,
        "budget_tip": "园林附近民宿有特色",
        "vibe": "江南园林甲天下",
        "keywords": ["拙政园", "虎丘", "周庄", "山塘街", "松鼠桂鱼"]
    },
    "harbin": {
        "name_en": "Harbin",
        "name_zh": "哈尔滨",
        "province": "黑龙江",
        "best_season": "冬季12-2月（冰雪节）",
        "days_min": 2,
        "days_max": 4,
        "budget_tip": "冬季装备要准备充足",
        "vibe": "冰雪之城 + 俄式风情",
        "keywords": ["冰雪大世界", "中央大街", "索菲亚教堂", "松花江", "锅包肉"]
    },
    "zhangjiajie": {
        "name_en": "Zhangjiajie",
        "name_zh": "张家界",
        "province": "湖南",
        "best_season": "4-6月, 9-10月",
        "days_min": 3,
        "days_max": 5,
        "budget_tip": "景区内住宿贵，建议住武陵源",
        "vibe": "阿凡达悬浮山原型",
        "keywords": ["天门山", "玻璃栈道", "武陵源", "天子山", "百龙天梯"]
    },
    "tibet": {
        "name_en": "Tibet",
        "name_zh": "西藏",
        "province": "西藏",
        "best_season": "5-10月",
        "days_min": 7,
        "days_max": 14,
        "budget_tip": "高反准备+边防证，跟团省心",
        "vibe": "雪域高原 + 信仰之地",
        "keywords": ["布达拉宫", "大昭寺", "纳木错", "珠峰", "羊卓雍措"]
    },
    "sanya": {
        "name_en": "Sanya",
        "name_zh": "三亚",
        "province": "海南",
        "best_season": "10-4月（冬季温暖）",
        "days_min": 3,
        "days_max": 7,
        "budget_tip": "旺季（春节）价格翻倍",
        "vibe": "热带海滨度假",
        "keywords": ["亚龙湾", "天涯海角", "蜈支洲岛", "椰梦长廊", "海鲜"]
    },
    "dunhuang": {
        "name_en": "Dunhuang",
        "name_zh": "敦煌",
        "province": "甘肃",
        "best_season": "5-10月",
        "days_min": 2,
        "days_max": 4,
        "budget_tip": "沙漠防晒做好，鸣沙山月牙泉必去",
        "vibe": "丝绸之路 + 大漠风情",
        "keywords": ["莫高窟", "鸣沙山", "月牙泉", "玉门关", "雅丹"]
    }
}
