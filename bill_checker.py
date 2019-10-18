# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 22:36:18 2018

@author: Mac
"""
import re
from xls_writer import SuiXlsTemplate, ExpenseEntry
import datetime

# cmb email 账单
cmb_pattern = r"(?P<date>\d+) \d+ (?P<detail>.+) [￥$] (?P<amount>[\d,]+\.\d+) 7007 (.+) ([\d,]+\.\d+)"
# cmb pdf 账单
cmb_pattern_pdf = r"(?P<date>\d\d/\d\d) (?P<detail>.+) (?P<amount>[\d,]+\.\d+) 7007 \d\d/\d\d ([\d,]+\.\d+)\(CN\)"
# cmbc 账单
cmbc_pattern = r"(?P<date>\d\d/\d\d) \d\d/\d\d (?P<detail>.*) (?P<amount>[\d,]+\.\d+) 4643"
# ccb(建行) 账单
cbc_pattern = r"(?P<date>\d\d\d\d-\d\d-\d\d)\s+(\d\d\d\d-\d\d-\d\d)\s+3885\s+(?P<detail>\S+)\s+CNY\s+(?P<amount>[\d,]+\.\d+)\s+CNY\s+([\d,]+\.\d+)"

sort_rules = {"food": ["肯德基", "老盛昌", "全家", "水果", "汉堡王", "星巴克", "必胜客", "红宝石", "多乐之日", 
                      "金拱门", "鸡排", "鲜芋仙", "四海游龙", "雪芙", "汤包", "泡芙", "餐饮", "呷哺呷哺", "玛格萝妮", "烤肉",
                      "翠华", "美团 && amount >= 20", "集贸市场", "莉莲", "煌上煌", "Mo-Mo牧场", "阿文大虾", "冰淇淋", "蛋糕", "咖喱", 
                      "耶里夏丽", "维果部落", "巴黎贝甜", "宽窄巷", "甘兔庵", "泉盛公司", "茶食代", "早安巴黎", "面包", "谷田稻香", "烧肉",
                      "餐厅", "酒楼", "食堂", "果茶", "巴黎贝甜", "维果部落", "茶餐", "冰激凌", "陆祥店", "Coffee+Belt",
                      "麦卡尤娜", "马上诺", "好德便利", "吴宝春麦方店", "7-Eleven", "阿甘锅盔", "蘇小柳", "曼游记", "杂粮煎饼", "留夫鸭", "清美绿色食品" ,
                      "小面家人", "食云纪", "Cantina", "牛杂", "牛肉", ],

            "life": ["绿地优鲜超市", "华住", "宝岛眼镜", "上蔬永辉", "迪亚天天", "窝的鲜花", "茶阁里的猫",
                     "联华超市", "叮咚买菜", "万宁", "屈臣氏", "名创优品",  "顺丰速运"],
            "dressing": ["优衣库", "HM", "盖璞", "热风", "GU", "服装"],
            "traffic": ["嘀嗒", "美团 && amount < 20", "上海交通卡", "石油化工", "滴滴出行", "钧正网络", "地铁APP"],
            "shopping": ["京东", "久光", "芮欧", "JD", "开市客",],
            "basic": ["城投水务", "电力公司", "手机充值", "上海燃气有限公司"],
            "entertain": ["幸福蓝海", "格瓦拉", "主题乐园", "顾村公园管理", ],
            "health": ["复旦大学附属华山医院", "药房", "儿童医院", "第十人民医院", "望族国宾"],
            "raise child": ["网易考拉", "卡通尼", "麦淘亲子", "亲子",
                            "爱婴室", "玩具反斗城", "贤爸科学", "奈尔宝家庭中心", "菊泉卫生服务中心"],
            "education": ["otto2",  "教育", "当当网", "少儿英语", "彩贝壳"],
            "holiday": ["去哪儿网", "酒店"],
            "business": ["丽途国际公寓"],
            "security": ["相互宝"]
            }

sui_cat_table = {"food": ["食品酒水", "早午晚餐"],
                 "life": ["日常生活", "日常花销"],
                 "dressing": ["衣服饰品", "衣服裤子"],
                 "traffic": ["行车交通", "打车租车"],
                 "shopping": ["购置物品", "生活用品"],
                 "basic": ["固定支出", "水电煤气"],
                 "entertain": ["休闲娱乐", "休闲玩乐"],
                 "health": ["医疗保健", "药品费"],
                 "raise child": ["生儿育女", "养孩子"],
                 "education": ["生儿育女", "教育子女"],
                 "holiday": ["休闲娱乐", "旅游度假"],
                 "business": ["其他杂项", "公费垫付"],
                 "security": ["金融保险", "购买保险"],
                 "unsorted": ["XXX", "YYY"],
                 }


class Record():
    def __init__(self, entry_text, pattern):
        rslt = re.match(pattern, entry_text)
        if rslt:
#            self.date = rslt.groups()[0]
#            self.amount = float(rslt.groups()[2].replace(',',''))   #处理3,710
#            self.detail = rslt.groups()[1]
            
            date = rslt.groupdict()['date']
            if len(date) in (4, 5):  # 招行民生日期格式
                self.date = str(datetime.datetime.today().year) + '-' + date[:2] + '-' + date[-2:]
                if date.startswith('12'):
                    print("12月账单, 注意年份!!!")
            elif '-' in date:
                self.date = date
            else:
                assert 0, 'error date format{}'.format(date)
                    
            self.amount = float(rslt.groupdict()['amount'].replace(',','')) #处理千分号
            self.detail = rslt.groupdict()['detail']
            
        else:
            print(entry_text)
            assert 0, "entry error: {}".format(entry_text)
        
    def __str__(self):
        return "{:<8.2f} {:<8s} {:<s}".format(self.amount, self.date, self.detail)
    
    def sort(self, category=None):
        """ 获得一条记录的分类
        """
        if category is None:
            category = list(sort_rules.keys())
        
        for i, cat in enumerate(category):
            try:
                for sub in sort_rules[cat]:
                    if '&&' in sub:
                        # 如果是一条复合条件, 第一项为关键字, 后几项为条件
                        seg = sub.split('&&')
                        if seg[0].strip() in self.detail:
                            for item in seg[1:]:
                                ins = "self." + item.strip()    # 形成指令
                                if not eval(ins):
                                    break
                            else:
                                # 满足所有条件的则判定
                                return i, cat
                    else:
                        if sub in self.detail:
                            return i, cat
            except Exception as e:
                print("err!", self)
                raise e
                
        else:
            return -1, 'unsorted'
        
        
def org(bill_text, print_reverse=False):
    entry_text = [entry.strip() for entry in bill_text.split('\n') if len(entry) > 8]
    category = list(sort_rules.keys())
    sorted_bill = [[cat, []] for cat in category]
    sorted_bill.append(['unsorted', []])
    
    for pattern in (cmb_pattern, cmb_pattern_pdf, cmbc_pattern, cbc_pattern):
        rslt = re.match(pattern, entry_text[0])
        if rslt:
            break
    else:
        assert 0, 'no repr pattern match!'
    
    # 
    for each_entry in entry_text:
        a = Record(each_entry, pattern)
        rslt = a.sort(category)
        sorted_bill[rslt[0]][1].append(a)
        
    # 按details排序
    for cat_entrys in sorted_bill:
        cat_entrys[1].sort(key=lambda x: x.detail)
    
    # print
    for cate in sorted_bill:
        if len(cate) > 1:
            print('\n',cate[0])
            sum_t = 0
            for item in cate[1]:
                sum_t += item.amount
                print(item)
            print('--total:{:.2f}'.format(sum_t))
            
    # print reverse
    if print_reverse:
        print('reversed order:')
        for each_entry in entry_text[::-1]:
            print(each_entry)

    return sorted_bill


def generate_xls(sorted_bill, filename = 'cmb_xxxx.xls'):
    assert filename.startswith('cmb') or filename.startswith('cmbc') or filename.startswith('cbc') #xls必须以cmb或cmbc,ccb开头

    xls = SuiXlsTemplate('./xls/' + filename)
    
    if filename.startswith('cmbc'):
        member = ''
        account = '信用卡民生'
    elif filename.startswith('cmb_'):
        member = '郑之颖'
        account = '信用卡招行人民币'
    elif filename.startswith('cbc_'):
        member = ''
        account = '信用卡建行沪通'

    for category_entrys in sorted_bill:
        category_name = category_entrys[0]
        cat1 = sui_cat_table[category_name][0]
        cat2 = sui_cat_table[category_name][1]
            
        for entry in category_entrys[1]:
            date = entry.date
            detail = entry.detail
            
            # 微调
            if (detail.startswith('财付通-')):
                detail = detail[4:]
            
            if '美团' in detail:
                if category_name == 'food':
                    detail = '美团外卖'
                else:
                    detail = '美团打车'
                    
            if cat1 == '固定支出' and '手机充值' in detail:
                cat2 = '通话上网'
                
            
            xls_enpense_entry = ExpenseEntry(date=date, cat1=cat1, cat2=cat2, account1=account,
                         amount=entry.amount, member=member, detail=detail)
            xls.add_expense_entry(xls_enpense_entry)
            
    xls.save()


if "__main__" == __name__:
    bill = """
1205 1206 财付通-京东商城平台商户 ￥ 109.82 7007 CN 109.82
1205 1206 支付宝-上海城投水务(集团)有限公 ￥ 277.60 7007 CN 277.60
1206 1207 财付通-上海市儿童医院 ￥ 15.50 7007 CN 15.50
    """
    
    sorted_bill = org(bill)
    
    generate_xls(sorted_bill, 'cmb_test.xls')
    
    category = list(sort_rules.keys())
    a = Record('1205 1206 财付通-京东商城平台商户 ￥ 109.82 7007 CN 109.82')
    print(a)
    print(a.sort(category))
    
    a = Record('1205 1206 美团 ￥ 100.82 7007 CN 109.82')
    print(a)
    print(a.sort(category))
        
