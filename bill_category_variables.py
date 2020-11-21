# -*- coding: utf-8 -*-
"""
    2020-05-03
"""
# cmb(招行) email 账单
pattern_cmb = r"(?P<date>\d+) \d+ (?P<detail>.+) [￥$](?P<amount>-* *[\d,]+\.\d+) 7007 (.+) (-* *[\d,]+\.\d+)"
# cmb(招行) pdf 账单
pattern_cmb_pdf = r"(?P<date>\d\d/\d\d) (?P<detail>.+) (?P<amount>[\d,]+\.\d+) 7007 \d\d/\d\d ([\d,]+\.\d+)\(CN\)"
# cmbc(民生) 账单
pattern_cmbc = r"(?P<date>\d\d/\d\d) \d\d/\d\d (?P<detail>.*) (?P<amount>-*[\d,]+\.\d+) 4643"
# ccb(建行) 账单
pattern_ccb = r"(?P<date>\d\d\d\d-\d\d-\d\d)\s+(\d\d\d\d-\d\d-\d\d)\s+3885\s+(?P<detail>[\s\S]+\S)\s+CNY\s+(?P<amount>-*[\d,]+\.\d+)\s+CNY\s+(-*[\d,]+\.\d+)"

# 支出描述关键字分类, 与网站解耦
bill_category_keywords = (
    {
        'food': ['肯德基', '老盛昌', '全家', '水果', '汉堡王', '必胜客', '红宝石', '多乐之日',
                 '金拱门', '鸡排', '鲜芋仙', '四海游龙', '雪芙', '汤包', '泡芙', '餐饮', '呷哺呷哺', '玛格萝妮', '烤肉',
                 '翠华', '美团 && amount >= 20', '集贸市场', '莉莲', '煌上煌', 'Mo-Mo牧场', '阿文大虾', '冰淇淋', '蛋糕', '咖喱',
                 '耶里夏丽', '维果部落', '巴黎贝甜', '宽窄巷', '甘兔庵', '泉盛公司', '茶食代', '早安巴黎', '面包', '谷田稻香', '烧肉',
                 '餐厅', '酒楼', '食堂', '果茶', '巴黎贝甜', '维果部落', '茶餐', '冰激凌', '陆祥店', 'Coffee+Belt',
                 '麦卡尤娜', '马上诺', '好德便利', '吴宝春麦方店', '7-Eleven', '阿甘锅盔', '蘇小柳', '曼游记', '杂粮煎饼', '留夫鸭', '清美绿色食品' ,
                 '小面家人', '食云纪', 'Cantina', '牛杂', '牛肉', '张亮麻辣烫', 'Wagas', '串小贱', '小杨生煎', '鲍师傅糕点', '羊肉串', '吴老幺',
                 '汤连得', '韵秋荷', '加减橙厨', '熬八年', '佬街佬味', '西餐', '85度C', 'LAWSON', 'TimsCoffeeHouse', '北鼎BUYDEEM', '料理', '烤鱼',
                 '追湘', '叮咚买菜', '快乐烘焙', '点都德', '葡式蛋挞', '麦金地', '歌志轩', '厨嫂当家', '家有好面', '棒棒鸡', '潮汕传人',
                 '铜锣烧', 'Cafe', '拉扎斯#饿了么#', '春杏古早味#蛋糕店#', '开心丽果#龙湖吃饭#', '浙江优亿#留夫鸭#', '奈雪の茶', '长发冰室#粤菜#', 
                 '亚惠#华为食堂#', '优芙得#华为食堂#', '群接龙#疫情期间订饭#', '东旭#华为食堂#', '晴美#华为食堂#', '东方既白', 
                 '1973继光香香鸡悦达88', '沃歌斯', '阿拉本帮', '翠园', '博多一幸舍#拉面#', 'Sunflour#面包#', '哈氏食品', '百果园', '西贝莜面村', '武圣羊汤', '百年卤煮', '蘑范儿小鸡炖蘑菇', 
                 '大朗谷雨', 'D伍KITCHEN#华为食堂#', '大食代', 'PIZZAHUT'],
        'life': ['绿地优鲜超市', '华住', '宝岛眼镜', '上蔬永辉', '迪亚天天', '窝的鲜花', '茶阁里的猫',
                 '联华超市', '万宁', '屈臣氏', '名创优品',  '顺丰速运', '刘氏蔬菜', '德邦物流', '宜家家居',
                 '美甲护肤', '丝芙兰', '洗衣', '喜茶', '大茉莉好物集', '永辉生活', 'sweetcolor#眼镜#', '苹果园大卖场', '流行前线#理发#',
                 '华润万家', '支付宝-周立珍#软水再生盐#', '支付宝-马宏涛#三少爷宠物#', 'LOFT#日式杂货店#', 'G-Super绿地超市', '一条生活馆','万物心选',  
                 '万物心选', '快递', '永辉超市'
                 ],
        'coffee & tea': ['星巴克', '花神咖啡馆', '歌帝梵#冰淇淋#', '上海喜创于茶', '壹加花园', '百兰谷咖啡', 'NO+COFFEE', '乐乐茶', '玛格琳尼#巧克力#', '西舍咖啡'],
        'dressing': ['优衣库', 'HM', '盖璞', '热风', 'GU', '服装', '飒拉', '新天泽雅柔', '海澜之家', '弥淑服饰', '永兴东润中国服饰', '茉莉屋#内衣贴身#'],
        'traffic': ['嘀嗒', '美团 && amount < 20', '上海交通卡', '滴滴出行', '钧正网络', '地铁APP', '杭州青奇', '曹操出行', '通驰科技#上海地铁#'],
        'car': ['石油化工', '十院停车场', '速泊车生活', '上海绿地东汽车销售', '停简单'],
        'shopping': ['京东', '久光', '芮欧', 'JD', '开市客#Cosco#',],
        'basic': ['城投水务', '电力公司', '手机充值', '上海燃气有限公司', '保利叶语物业', '中国电信股份有限公司'],
        'entertain': ['幸福蓝海', '格瓦拉', '主题乐园', '顾村公园', '野生动物园', '迪士尼'],
        'health': ['复旦大学附属华山医院', '药房', '儿童医院', '第十人民医院', '望族国宾', '挂号网', '华山北院'],
        'raise child': ['网易考拉', '卡通尼', '麦淘亲子', '亲子',
                        '爱婴室', '玩具反斗城', '贤爸科学', '奈尔宝家庭中心', '菊泉卫生服务中心', 'lollipop#粒粒堡#', '易智乐'],
        'education': ['otto2',  '教育', '当当网', '少儿英语', '彩贝壳', '学而思轻课', '孩思乐', '小鹅通知识助手', 'STEM', '斑马AI', '汪齐风芭蕾', ],
        'holiday': ['去哪儿网', '酒店'],
        'business': ['丽途国际公寓'],
        'security': ['相互宝'],
        'digital': ['华为终端有限', '华为商城', ],
        'collection': ['微拍堂']
    },

    {
        'refund': [''],         # '' is substring of any string
    }
)

# 随手记账目分类
sui_category_expense = {
    'food': ['食品酒水', '早午晚餐'],
    'life': ['日常生活', '日常花销'],
    'coffee & tea': ['食品酒水', '烟酒茶'],
    'dressing': ['衣服饰品', '衣服裤子'],
    'traffic': ['行车交通', '打车租车'],
    'car': ['行车交通', '私家车费用'],
    'shopping': ['购置物品', '生活用品'],
    'basic': ['固定支出', '水电煤气'],
    'entertain': ['休闲娱乐', '休闲玩乐'],
    'health': ['医疗保健', '药品费'],
    'raise child': ['生儿育女', '养孩子'],
    'education': ['生儿育女', '教育子女'],
    'holiday': ['休闲娱乐', '旅游度假'],
    'business': ['其他杂项', '公费垫付'],
    'security': ['金融保险', '购买保险'],
    'digital': ['购置物品', '数码产品'],
    'collection': ['购置物品', '古董收藏'],
    'unsorted': ['XXX', 'YYY'],
}

sui_category_income = {
    'refund': ['其他收入', '退货进账'],
}
