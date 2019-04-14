# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 22:36:18 2018

@author: Mac
"""
import re

cmb_pattern = r"(\d+) \d+ (.+) [￥$] (\d+\.\d+) 7007 (.+) (\d+\.\d+)"

keywords = {"food" : ["美团", "肯德基", "老盛昌", "全家", "水果", "汉堡王", "星巴克", "必胜客", "红宝石", "多乐之日", 
                      "金拱门", ],
            "life": ["绿地优鲜超市", "华住", "宝岛眼镜", ],
            "traffic": ["嘀嗒", "嘀嘀", "美团"],
            "shopping": ["京东", "久光", ],
            "basic": ["城投水务", "电力公司"],
            "entertain":["幸福蓝海",],
            "raise child":["儿童医院", "第十人民医院", "网易考拉", "卡通尼", "麦淘亲子"],
            "life":["上蔬永辉"]
            }

class TransactionRecord():
    def __init__(self, pattern, keywords_dict):
        self.pattern = pattern
        self.records = []
        self.unknown = []
        
        self.category = list(keywords.keys())
        self.bills = [[cat,] for cat in self.category]
        self.bills.append(['unknown',])
    
    def add_record(self, record_text):
        rslt = re.match(self.pattern, record_text)
        if rslt:
            record = {'date': rslt.groups[0],
                      'amount': float(rslt.groups[2]),
                      'tag': rslt.groups[1],
                    }
            self.records.append(record)
        else:
            self.unknown.append(record)
            
    def classify_records(self, ):
        pass
#        for record in self.records:
#            index = search_category
#            
#            
#            if record['tag']


def org(bill):
    """ bill是招行账单, 每一行是一条记录, 以\n分隔
        将按keywords中的关键字将bill有序分隔开 打印出来
    """
    entrys = [entry.strip() for entry in bill.split('\n') if len(entry) > 8]
    category = list(keywords.keys())
    sorted_bill = [[cat] for cat in category]
    remained_bill = ['remained']
    
    def get_money_amout(entry):
        """ 得到一条记录的金额
        """
        return int(entry[entry.rfind(' '):])
    
    
    def sort_entry(entry, category, keywords, extra_cond=True):
        """ 获得一条记录的分类
        """
        for (i, cat) in enumerate(category):
            for sub in keywords[cat]:
                if sub in entry:
                    return i
        else:
            return -1
    
    for each_entry in entrys:
        a = sort_entry(each_entry, category, keywords)
        if a == -1:
            remained_bill.append(each_entry)
        else:
            sorted_bill[a].append(each_entry)
    
    for cate in sorted_bill:
        if len(cate) > 1:
            print('\n',cate[0])
            for item in cate[1:]:
                print(item)

    print('\n',remained_bill[0])
    for item in remained_bill[1:]:
        print(item)
    
    
    print('\n\n\n\nreversed order:')
    for item in entrys[::-1]:
        print(item)

    return sorted_bill, remained_bill
    

if "__main__" == __name__:
    bill = """
1205 1206 财付通-京东商城平台商户 ￥ 109.82 7007 CN 109.82
1205 1206 支付宝-上海城投水务(集团)有限公 ￥ 277.60 7007 CN 277.60
1206 1207 财付通-上海市儿童医院 ￥ 15.50 7007 CN 15.50
    """
    
    org(bill)
    
        