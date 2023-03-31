# -*- coding: utf-8 -*-
"""
    2020-05-03
"""
# cmb(招行) email 账单
pattern_cmb = r"\d+ (?P<date>\d+) (?P<detail>.+) [￥$¥] (?P<amount>-*[\d,]+\.\d+) 7007 (.+) (-*[\d,]+\.\d+)"
# cmb(招行) pdf 账单
pattern_cmb_pdf1 = r"(?P<date>\d\d/\d\d) (?P<detail>.+) (?P<amount>[\d,]+\.\d+) 7007 \d\d/\d\d ([\d,]+\.\d+)\(CN\)"
pattern_cmb_pdf2 = r"\s*\d\d/\d\d (?P<date>\d\d/\d\d) (?P<detail>.+) (?P<amount>-*[\d,]+\.\d+) 7007 (-*[\d,]+\.\d+)\(\w+\)"
# cmbc(民生) 账单
pattern_cmbc = r"(?P<date>\d\d/\d\d) \d\d/\d\d (?P<detail>.*) (?P<amount>-*[\d,]+\.\d+) 4643"
# ccb(建行) 账单
pattern_ccb = r"(?P<date>\d\d\d\d-\d\d-\d\d)\s+(\d\d\d\d-\d\d-\d\d)\s+3885\s+(?P<detail>[\s\S]+\S)\s+CNY\s+(?P<amount>-*[\d,]+\.\d+)\s+CNY\s+(-*[\d,]+\.\d+)"

# 支出描述关键字分类, 与网站解耦
bill_category_keywords = (
    {
        'food': ['肯德基', '老盛昌', '全家', '水果', '汉堡王', '必胜客', '红宝石', '多乐之日',
                 '金拱门', '鸡排', '鲜芋仙', '四海游龙', '雪芙', '汤包', '泡芙', '餐饮', 
                 '呷哺呷哺', '玛格萝妮', '烤肉', '翠华', '美团 && amount >= 20', '集贸市场', 
                 '莉莲', '煌上煌', 'Mo-Mo牧场', '阿文大虾', '冰淇淋', '蛋糕', '咖喱',
                 '耶里夏丽', '维果部落', '巴黎贝甜', '宽窄巷', '甘兔庵', '泉盛公司(食其家)', 
                 '茶食代', '早安巴黎', '面包', '谷田稻香', '烧肉', '餐厅', '酒楼', '食堂', 
                 '果茶', '巴黎贝甜', '维果部落', '茶餐', '冰激凌', '陆祥店', 'Coffee+Belt',
                 '麦卡尤娜', '马上诺', '好德便利', '吴宝春麦方店', '7-Eleven', '阿甘锅盔', 
                 '蘇小柳', '曼游记', '杂粮煎饼', '留夫鸭', '清美绿色食品' ,'小面家人', '食云纪', 
                 'Cantina', '牛杂', '牛肉', '张亮麻辣烫', 'Wagas', '串小贱', '小杨生煎', 
                 '鲍师傅糕点', '羊肉串', '吴老幺', '汤连得', '韵秋荷', '加减橙厨', '熬八年', 
                 '佬街佬味', '西餐', '85度C', 'LAWSON', 'TimsCoffeeHouse', '北鼎BUYDEEM', 
                 '料理', '烤鱼', '追湘', '叮咚买菜', '快乐烘焙', '点都德', '葡式蛋挞', '麦金地', 
                 '歌志轩', '厨嫂当家', '家有好面', '棒棒鸡', '潮汕传人', '铜锣烧', 'Cafe', 
                 '拉扎斯#饿了么#', '春杏古早味#蛋糕店#', '开心丽果#龙湖吃饭#', '浙江优亿#留夫鸭#', 
                 '奈雪の茶', '长发冰室#粤菜#', '亚惠#华为食堂#', '优芙得#华为食堂#', 
                 '群接龙#疫情期间团购#', '东旭#华为食堂#', '晴美#华为食堂#', '东方既白', 
                 '1973继光香香鸡悦达88', '沃歌斯', '阿拉本帮', '翠园', '博多一幸舍#拉面#', 
                 'Sunflour#面包#', '哈氏食品', '百果园', '西贝莜面村', '武圣羊汤', '百年卤煮', 
                 '蘑范儿小鸡炖蘑菇', '三人行骨头王', '大朗谷雨', 'D伍KITCHEN#华为食堂#', 
                 '大食代', 'PIZZAHUT', '多乐房', '不二原麦#面包#', '剁椒鱼头', '梅龙镇快餐', 
                 '麦吉#奶茶#', '麻辣烫', '好利来', '薯语', '南门涮肉', '湘蒸味#东方万国食堂#',
                 '黑牛の店', '张记油条', '巴比馒头', '泉盛公司#食其家#', '梅龙镇酒家#华为食堂#',  
                 'Vesta', 'AJIYA', '丰茂烤串', '海南椰子鸡', '老北京涮羊肉', '中国葛洲坝集团文旅#金闵园食堂#',
                 '富春小笼', 'Munchies梦奇屋', '潮汕集市#深圳机场#', '筑岛上海金虹桥店',                 
                 '磁盛天毛血旺', '牛尖角创意烧肉', '意拾光', '来福士咬金', '渔市厂#美罗城#',
                 '立方铁铁板烧', '东北灶', '海底捞', '小邢海鲜龙虾烧烤', '蔡澜港式点心',
                 '湘阁里辣#溪村#', '两廣狠牛#灵石路牛杂#', '香吧拉#小龙虾#', 'H+Kitchen#儿童医院希腊餐厅#',
                 '鳗诚屋', 'Julies香', '哈尔滨食品厂', '伶小熙点心铺', '茱莉亚食品', '陈香贵',
                 '酥鱼坊', '糖小满', '詹记宫廷桃酥', '阿木龙虾', '陕老顺', '广佬记', '德保膳食管理#国展地下#',
                 '东北水饺', '酸小七酸汤鱼', '小码头川湘菜', '姑苏面庄', '西北合', '鹅南记',
                 '寿司沼津港', '南京大牌档', '每日优鲜', '客家厨房', '乡谷村','老碗会', '磁盛天', '粤吧小罐汤', 
                 '乐凯撒披萨', '湘稻香#国展绿地#', '侎唛食厂#青浦台湾菜#','爱碗亭#华为食堂#','秦云老太婆#华为食堂#',
                 '好这口重庆小面', '张六羊肉粉', '地锅鸡守艺', '海鲜烧烤', '小明同学卤肉饭',  
                 ],
        
        'life': ['京东', '绿地优鲜超市', '华住', '宝岛眼镜', '上蔬永辉', '迪亚天天', '窝的鲜花', 
                 '茶阁里的猫', '联华超市', '万宁', '屈臣氏', '名创优品',  '顺丰速运', 
                 '刘氏蔬菜', '德邦物流', '宜家家居', '美甲护肤', '丝芙兰', '洗衣', '喜茶', 
                 '大茉莉好物集', '永辉生活', 'sweetcolor#眼镜#', '苹果园大卖场', 
                 '流行前线#理发#','华润万家', '支付宝-周立珍#软水再生盐#', '支付宝-马宏涛#三少爷宠物#', 
                 'LOFT#日式杂货店#', 'G-Super绿地超市', '一条生活馆','万物心选', '万物心选',
                 '快递', '永辉超市', 'KKV#印象城杂货铺#', '第五季发型', '完美日记#化妆品#', 
                 'X11#印象城杂货铺#', '多特瑞#精油#', '快团团#顾村生活群#', '九木杂物社', 
                 'OCE#杂货店#', 'AlexshopStore#进口食品小超市#', '来伊份', 'FONTAINE#冰淇淋#',
                 '宏辉果品', '德克士', '喜士多便利连锁', 'APITA雅品嘉超市', '张姐蔬菜菊联路',
                 '联华快客', '时代超市', '邻家超市', '广东赛壹便利店#溪村超市#', '家乐缘#溪村超市#',
                 '苹果园批发行菊联路店#水果#', '怪兽充电', '沃尔玛(中国)', '满记甜品',
                 '京喜#京东拼多多#', '无印良品', '山姆会员商店', '光明随心订', '南京大牌档',
                 '顺丰同城','金多乐商贸#淘宝猫粮#',
                 ],

        'coffee & tea': ['星巴克', '花神咖啡馆', '歌帝梵#冰淇淋#', '上海喜创于茶', '壹加花园', 
                 '百兰谷咖啡', 'NO+COFFEE', '乐乐茶', '玛格琳尼#巧克力#', '西舍咖啡',
                 'Manner Coffee', '1+Garden', 'Tims咖啡', 'AZABUYA#麻布屋抹茶冰淇淋#',
                 'VQ鲜榨果汁', '中街1946#雪糕#', '果榛炒酸奶', '7分甜', '麦卡优娜手感烘焙',
                 '茶百道', 'SMAKA#儿童医院咖啡#', '上海民睿文化发展#万国击剑旁美术馆咖啡#',
                 '阿尔托金闽园#金闽园3号楼咖啡#', 'MURANO#玻璃博物馆餐厅#', '奈雪',  
                 'luckincoffee', '瑞幸咖啡', '茉酸奶', 'DrCheese奶酪博士', 'M Stand',
                 '阿拉比卡咖啡','NewWorldcafe#坂田咖啡厅#',
                ],
        
        'dressing': ['优衣库', 'HM', '盖璞', '热风', 'GU', '服装', '飒拉', '新天泽雅柔', 
                '海澜之家', '弥淑服饰', '永兴东润中国服饰', '茉莉屋#内衣贴身#', 
                'nikoand#衣服#', '三黄时装', '女装9', '上海乐橙贸易商行#龙之梦衣饰#',
                '全棉时代', '滔搏运动城#龙湖天街运动服饰#', 'GAP', '函亭服饰', 
                ],
        
        'taxi': ['嘀嗒', '美团 && amount < 20', '滴滴出行', '曹操出行', '申城出行#打车#', 
                '享道出行',
                 ],
        
        'traffic': [ '上海交通卡',  '钧正网络#哈罗单车#', '地铁APP', '杭州青奇',  '通驰科技#上海地铁#',
                '广州骑安#青桔单车#', '厦门地铁', '中国铁路总公司资金', '地铁快乐行#微信上海地铁押金#',
                '深高速', '哈啰普惠#哈啰单车#',  
                ],
        
        'car': ['石油化工', '十院停车场', '速泊车生活', '上海绿地东汽车销售', '停简单#小布跳舞的家乐福停车#', 
                '上海宝山天街', '迈泊停车', '高速通行费', '上海声珩建筑装潢服务#爱康国宾体检中心停车#', 
                '申隆石化双城站', '杭州景芳#车检#', '上海翼鸣#凯旋丽都停车场#', '永升生活服务#极橙停车#', 
                '上海金桥出口加工区#金闽园停车#', '上海集佳文化创意发展#玻璃博物馆停车#',
                '聚悦#万国体育击剑停车#', '金桥太茂#停车#', '长风11号地块停车场#儿童医院停车#',
                'ETCP停车#东方万国停车#', '万象城停车场', '上海交大#交大停车#', 
                '互联互通停车场#虹桥绿地停车#', '上海虹桥天街(停车场)', 
               ],
        
        'shopping': ['久光', '芮欧', 'JD', '开市客#Cosco#', 'Outland#户外用品#'],
        
        'basic': ['城投水务', '电力公司', '手机充值', '上海燃气有限公司', '保利叶语物业', 
                    '中国电信股份有限公司'
                 ],
        
        'entertain': ['幸福蓝海', '格瓦拉', '主题乐园', '顾村公园', '野生动物园', '迪士尼', 
                '中影#电影#', '香朵开心农场', '上海海洋水族馆', '上海玻璃博物馆',
                '百丽宫影城', 'GOOGLE*YOUTUBE#油管频道会员#'
                ],
        
        'health': ['复旦大学附属华山医院', '药房', '儿童医院', '第十人民医院', '望族国宾', 
                '挂号网', '华山北院', '菊泉新城社区卫生',  '叮当快药',
                '雅悦', '怡禾健康',
                ],

        'birth':    ['长宁区妇幼保健', '上海申尔科技#儿童医院罗森护理用品#', 'e护通#儿童医院护理#', 
                '上海市宝山区顾村镇菊#社区疫苗#',
                ],
        
        'raise child': ['网易考拉', '卡通尼', '麦淘亲子', '亲子','爱婴室', '玩具反斗城', 
                '贤爸科学', '奈尔宝家庭中心', '菊泉卫生服务中心', 'lollipop#粒粒堡#', 
                '易智乐', 'mideer弥鹿母婴旗舰店#玩具#', 'FIZZ+IN+BLUE#童装#', 
                '斯凯奇贸易#童鞋#', 'ROOKIE#童装#', 'OK之选#育儿团购#', '极橙',  
                '斑米文具', '凯叔讲故事', 
                ],

        'education': ['otto2',  '教育', '当当网', '少儿英语', '彩贝壳', '学而思轻课', '孩思乐', 
                '小鹅通知识助手', 'STEM', '斑马AI', '汪齐风芭蕾', '鲸鱼外教', 
                '世外云尚#幼儿园学费#', '柔持英语',  'Otto2艺术美学#画画课#', 
                '上海开剑体育发展有限公司#击剑课#', '斑马', '欧莱俱乐部', '聚芙文化艺术咨询#Otto2#',
                ],

        'holiday': ['去哪儿网', '酒店', '海昌极地海洋', '海昌公园'],
        
        'business': ['丽途国际公寓'],
        
        'security': ['相互宝', '三星财产保险#车险#'],
        
        'digital': ['华为终端有限', '华为商城', ],
        
        'collection': ['微拍堂', ]

    },

    {
        'refund': [''],         # '' is substring of any string
    }
)

# 随手记账目分类
sui_category_expense = {
        'food':         ['食品酒水', '早午晚餐'],
        'life':         ['日常生活', '日常花销'],
        'coffee & tea': ['食品酒水', '烟酒茶'],
        'dressing':     ['衣服饰品', '衣服裤子'],
        'traffic':      ['行车交通', '公共交通'],
        'taxi':         ['行车交通', '打车租车'],
        'car':          ['行车交通', '私家车费用'],
        'shopping':     ['购置物品', '生活用品'],
        'basic':        ['固定支出', '水电煤气'],
        'entertain':    ['休闲娱乐', '休闲玩乐'],
        'health':       ['医疗保健', '药品费'],
        'birth':        ['生儿育女', '生孩子'],
        'raise child':  ['生儿育女', '养孩子'],
        'education':    ['生儿育女', '教育子女'],
        'holiday':      ['休闲娱乐', '旅游度假'],
        'business':     ['其他杂项', '公费垫付'],
        'security':     ['金融保险', '购买保险'],
        'digital':      ['购置物品', '数码产品'],
        'collection':   ['购置物品', '古董收藏'],
        'unsorted':     ['未知分类', '未知子类'],
}

sui_category_income = {
    'refund': ['其他收入', '退货进账'],
}
