# -*- coding: utf-8 -*-
"""
Created on 2020-05-03
@author: Mac

重构 bill_checker.py
"""

import re
import datetime
from sui_xls_writer import SuiEntry, SuiXlsTemplate
from bill_category_variables import *


class Record:
    """ 一条消费(退款)记录
    """
    def __init__(self, entry_text, pattern, bill_year, bill_month):
        rslt = re.match(pattern, entry_text)
        if rslt:
            #            self.date = rslt.groups()[0]
            #            self.amount = float(rslt.groups()[2].replace(',',''))   #处理3,710
            #            self.detail = rslt.groups()[1]

            date = rslt.groupdict()['date']
            if len(date) in (4, 5):  # 招行民生日期格式
                if date.startswith('12'):
                    print("12月账单, 注意年份!!!")
                    assert bill_month == 12 or bill_month == 1
                    if bill_month == 12:
                        self.date = str(bill_year) + '-' + date[:2] + '-' + date[-2:]
                    else:
                        print("去年12月记录")
                        self.date = str(bill_year - 1) + '-' + date[:2] + '-' + date[-2:]
                else:
                    self.date = str(bill_year) + '-' + date[:2] + '-' + date[-2:]
            elif '-' in date:
                self.date = date
            else:
                assert 0, 'error date format{}'.format(date)

            amount = rslt.groupdict()['amount']
            amount = amount.replace(',', '')  # 处理千分号
            amount = amount.replace(' ', '')  # 空格

            self.amount = float(amount)
            self.detail = rslt.groupdict()['detail']
            self.valid = True
            self.comment = None

            self.classification = None
            self.category_index = None
            self.category_key = None

        else:
            print("Entry:", entry_text, " can't get sorted!")
            self.valid = False
            # assert 0, "entry error: {}".format(entry_text)

    def __str__(self):
        return "{:12s} {:<8s} {:<8.2f} {:<s}".format(self.category_key, self.date, self.amount, self.detail)

    def get_category(self, category_keywords):
        """ 根据传入的分类keyword字典, 逐条判定本条记录的detail中是否包含keyword, 获得本条记录的分类
        """
        if self.amount >= 0:
            classification = 0
        else:
            classification = 1
            self.amount = -self.amount  # 退货数额需转成正数
        category_keywords_dict = category_keywords[classification]
        category_keys = list(category_keywords_dict.keys())

        for i, key in enumerate(category_keys):
            try:
                for keyword in category_keywords_dict[key]:
                    if '#' in keyword:
                        # 如果包含'#', 后半部分为注释
                        pos_comment_start = keyword.find('#')
                        pos_comment_end = keyword.rfind('#')
                        if pos_comment_end > pos_comment_start:
                            comment = keyword[pos_comment_start + 1: pos_comment_end]
                        else:
                            comment = keyword[pos_comment_start + 1:]
                        keyword = keyword[:pos_comment_start]
                    else:
                        comment = None

                    if '&&' in keyword:
                        # 如果是一条复合条件, 第一项为关键字, 后几项为条件
                        seg = keyword.split('&&')
                        if seg[0].strip() in self.detail:
                            for item in seg[1:]:
                                ins = "self." + item.strip()  # 形成指令
                                if not eval(ins):
                                    break
                            else:
                                # 满足所有条件的则判定
                                self.classification = classification
                                self.category_index = i
                                self.category_key = key
                                self.comment = comment
                                return classification, i, key
                    else:
                        if keyword in self.detail:
                            self.classification = classification
                            self.category_index = i
                            self.category_key = key
                            self.comment = comment
                            return classification, i, key
            except Exception as e:
                print("err!", self)
                raise e
        else:
            self.classification = classification
            self.category_index = -1
            self.category_key = 'unsorted'
            return classification, -1, 'unsorted'


class BillParser:
    def __init__(self, ):
        # 账单文本格式的正则表达式pattern
        self.bill_record_str_patterns = [pattern_cmb, pattern_cmb_pdf, pattern_cmbc, pattern_ccb]
        self.bill_cards = ['信用卡招行人民币', '信用卡招行人民币', '信用卡民生', '信用卡建行沪通'] # 两种格式都是招行的
        self.bill_category_keywords = bill_category_keywords
        self.account_category_expense = sui_category_expense
        self.account_category_income = sui_category_income

        self.records = None
        self.card_name = None
        self.bill_year = None
        self.bill_month = None
        pass
    
    def judge_bill_date(self, all_entry, pattern):
        month_set = []
        
        for entry_text in all_entry:
            rslt = re.match(pattern, entry_text)
            if rslt:
                date = rslt.groupdict()['date']
                if len(date) in (4, 5):  # 招行民生日期格式
                    month = int(date[:2])
                elif '-' in date:
                    month = int(date[5:7])
                else:
                    assert 0, 'error date format{}'.format(date)
    
                if int(month) not in month_set:
                    month_set.append(month)
        
        assert len(month_set) <= 2, "error month data in bill:{}".format(month_set) 
        month_set.sort()
        if(len(month_set) == 2 and month_set[0] == 1 and month_set[-1] == 12):
            # 跨年账单
            print("跨年账单")
            self.bill_year = datetime.datetime.today().year
            self.bill_month = 1
        else:
            if month_set[-1] > datetime.datetime.today().month:
                # 如账单月份比当前时间大, 说明是去年账单, 除此之外, 都是今年账单
                self.bill_year = datetime.datetime.today().year - 1
            else:
                self.bill_year = datetime.datetime.today().year
            self.bill_month = month_set[-1]
        
        return self.bill_year, self.bill_month        

    def read_credit_card_bill_file(self, bill_file):
        with open(bill_file) as f:
            bill_text = f.read()
        entry_text = [entry.strip() for entry in bill_text.split('\n') if len(entry) > 8]
        
        # 用第一条记录文本确定bill text是哪个银行
        for i, pattern in enumerate(self.bill_record_str_patterns):
            rslt = re.match(pattern, entry_text[0])
            if rslt:
                self.card_name = self.bill_cards[i]
                break
        else:
            assert 0, 'no repr pattern match! "{}"'.format(entry_text[0])

        # 招行信用卡民生信用卡先浏览全部记录确定账单日期, 避免跨年账单前后年份错乱
        if self.card_name in ('信用卡招行人民币', '信用卡民生'):
            self.judge_bill_date(entry_text, pattern)

        # 得到消费记录
        self.records = [Record(each_entry, pattern, self.bill_year, self.bill_month) for each_entry in entry_text]

        # 计算消费记录分类
        for rec in self.records:
            rec.get_category(self.bill_category_keywords)

    def print_bill(self,):
        for rec in self.records:
            print(rec)

    def sort_bill(self,):
        self.records.sort(key=lambda x: x.category_key)

    def write_xls(self, filename='cmb_xxxx.xls'):
        assert filename.startswith('cmb') or filename.startswith('cmbc') or filename.startswith('ccb'), "xls file name:{}".format(filename)  # xls必须以cmb或cmbc,ccb开头

        xls = SuiXlsTemplate('./xls/' + filename)
        account = self.card_name
        if self.card_name == '信用卡招行人民币':
            member = '郑之颖'
        else:
            member = ''

        for record in self.records:
            classification = record.classification                  # expense or income
            date = record.date
            amount = record.amount
            if record.comment is not None:
                detail = record.detail + '({:s})'.format(record.comment) 
            else:
                detail = record.detail
            category_key = record.category_key

            if classification == 0:
                cat1 = self.account_category_expense[category_key][0]
                cat2 = self.account_category_expense[category_key][1]
            else:
                cat1 = self.account_category_income[category_key][0]
                cat2 = self.account_category_income[category_key][1]

            # 微调
            if (detail.startswith('财付通-')):
                detail = detail[4:]

            if '美团' in detail:
                if category_key == 'food':
                    detail = '美团外卖'
                else:
                    detail = '美团打车'

            if cat1 == '固定支出' and '手机充值' in detail:
                cat2 = '通话上网'

            xls_entry = SuiEntry(date=date, cat1=cat1, cat2=cat2, account1=account, amount=amount,
                                 member=member, detail=detail, classification=classification)
            xls.add_entry(xls_entry)

        xls.save()
        print('generate xls file at ', xls.file_path)
        
if "__main__" == __name__:
    bill = BillParser()
#    bill.read_credit_card_bill_file(r'e:\work\work_py\project\bill_check_utils\txt\cmb_202012.txt')
#    bill.sort_bill()
#    bill.print_bill()
#    bill.write_xls('cmb_2004.xls')
#    bill.test_bill_date(r'e:\work\work_py\project\bill_check_utils\txt\cmbc_1912.txt')
