# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 22:36:18 2018

@author: Mac
"""
import re
from xls_writer import SuiXlsTemplate, ExpenseEntry
import datetime

# email 账单
cmb_pattern = r"(\d+) \d+ (.+) [￥$] ([\d,]+\.\d+) 7007 (.+) ([\d,]+\.\d+)"
# pdf 账单
#cmb_pattern = r"(\d\d/\d\d) (.+) ([\d,]+\.\d+) 7007 \d\d/\d\d ([\d,]+\.\d+)\(CN\)"

sort_rules = {"food": ["肯德基", "老盛昌", "全家", "水果", "汉堡王", "星巴克", "必胜客", "红宝石", "多乐之日", 
                      "金拱门", "鸡排", "鲜芋仙", "四海游龙", "雪芙", "汤包", "泡芙", "餐饮", "呷哺呷哺", "玛格萝妮", "烤肉",
                      "翠华", "美团 && amount >= 20", "集贸市场", "莉莲", "煌上煌", "Mo-Mo牧场", "阿文大虾", "冰淇淋", "蛋糕", "咖喱", 
                      "耶里夏丽", "维果部落", "巴黎贝甜", "宽窄巷", "甘兔庵", "泉盛公司", "茶食代",
                      "餐厅", "酒楼", "食堂", "果茶", "巴黎贝甜", "维果部落", "茶餐", "冰激凌"],

            "life": ["绿地优鲜超市", "华住", "宝岛眼镜", "上蔬永辉", "迪亚天天", "窝的鲜花", "茶阁里的猫",
                     "联华超市", "叮咚买菜", "万宁", "屈臣氏"],
            "dressing": ["优衣库", "HM", "盖璞", "热风", "GU"],
            "traffic": ["嘀嗒", "嘀嘀", "美团 && amount < 20"],
            "shopping": ["京东", "久光", "芮欧"],
            "basic": ["城投水务", "电力公司", "手机充值"],
            "entertain": ["幸福蓝海", "格瓦拉", "主题乐园", "顾村公园管理"],
            "health": ["复旦大学附属华山医院", "药房", "儿童医院", "第十人民医院",],
            "raise child": ["网易考拉", "卡通尼", "麦淘亲子", "亲子",
                            "爱婴室", "玩具反斗城", "贤爸科学"],
            "education": ["otto2",  "教育", "当当网"],
            "holiday": ["去哪儿网"],
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
                 "education": ["生儿育女", "教育孩子"],
                 "holiday": ["休闲娱乐", "旅游度假"],
                 "unsorted": ["XXX", "YYY"]
                 }





class Record():
    def __init__(self, entry_text):
        rslt = re.match(cmb_pattern, entry_text)
        if rslt:
            self.date = rslt.groups()[0]
            self.amount = float(rslt.groups()[2].replace(',',''))   #处理3,710
            self.detail = rslt.groups()[1]
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
    
    # 
    for each_entry in entry_text:
        a = Record(each_entry)
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
    assert filename.startswith('cmb') or filename.startswith('cmbc'), 'xls必须以cmb或cmbc开头'

    xls = SuiXlsTemplate('./xls/' + filename)
    
    if filename.startswith('cmb'):
        member = '郑之颖'
        account = '信用卡招行人民币'
    elif filename.startswith('cmbc'):
        member = ''
        account = '信用卡民生人民币'

    for category_entrys in sorted_bill:
        category_name = category_entrys[0]
        cat1 = sui_cat_table[category_name][0]
        cat2 = sui_cat_table[category_name][1]
            
        for entry in category_entrys[1]:
            date = str(datetime.datetime.today().year) + '-' + entry.date[:2] + '-' +entry.date[-2:]
            
            xls_enpense_entry = ExpenseEntry(date=date, cat1=cat1, cat2=cat2, account1=account,
                         amount=entry.amount, member=member, detail=entry.detail)
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
        
