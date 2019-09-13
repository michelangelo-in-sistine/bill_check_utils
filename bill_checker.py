# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 22:36:18 2018

@author: Mac
"""
import re

# email 账单
cmb_pattern = r"(\d+) \d+ (.+) [￥$] ([\d,]+\.\d+) 7007 (.+) ([\d,]+\.\d+)"
# pdf 账单
#cmb_pattern = r"(\d\d/\d\d) (.+) ([\d,]+\.\d+) 7007 \d\d/\d\d ([\d,]+\.\d+)\(CN\)"

sort_rules = {"food": ["肯德基", "老盛昌", "全家", "水果", "汉堡王", "星巴克", "必胜客", "红宝石", "多乐之日", 
                      "金拱门", "鸡排", "鲜芋仙", "四海游龙", "雪芙", "汤包", "泡芙", "餐饮", "呷哺呷哺", "玛格萝妮", "烤肉",
                      "翠华", "美团 && amount >= 20", "集贸市场", "莉莲", "煌上煌", "Mo-Mo牧场", "阿文大虾", "冰淇淋", "蛋糕", "咖喱", 
                      "耶里夏丽", "维果部落", "巴黎贝甜", "宽窄巷", "甘兔庵", "泉盛公司", "茶食代",
                      "餐厅", "酒楼", "食堂", "果茶", "巴黎贝甜", "维果部落"],

            "life": ["绿地优鲜超市", "华住", "宝岛眼镜", "上蔬永辉", "迪亚天天", "窝的鲜花", "茶阁里的猫",
                     "联华超市", "叮咚买菜", "万宁"],
            "dressing": ["优衣库", "HM", "盖璞", "热风", "GU"],
            "traffic": ["嘀嗒", "嘀嘀", "美团 && amount < 20"],
            "shopping": ["京东", "久光", "芮欧"],
            "basic": ["城投水务", "电力公司", "手机充值"],
            "entertain": ["幸福蓝海", "格瓦拉", "主题乐园", "顾村公园管理"],
            "health": ["复旦大学附属华山医院"],
            "raise child": ["儿童医院", "第十人民医院", "网易考拉", "卡通尼", "麦淘亲子", "亲子",],
            "education": ["otto2",  "教育", "当当网"]
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

if "__main__" == __name__:
    bill = """
1205 1206 财付通-京东商城平台商户 ￥ 109.82 7007 CN 109.82
1205 1206 支付宝-上海城投水务(集团)有限公 ￥ 277.60 7007 CN 277.60
1206 1207 财付通-上海市儿童医院 ￥ 15.50 7007 CN 15.50
    """
    
    org(bill)
    
    category = list(sort_rules.keys())
    a = Record('1205 1206 财付通-京东商城平台商户 ￥ 109.82 7007 CN 109.82')
    print(a)
    print(a.sort(category))
    
    a = Record('1205 1206 美团 ￥ 100.82 7007 CN 109.82')
    print(a)
    print(a.sort(category))
        
