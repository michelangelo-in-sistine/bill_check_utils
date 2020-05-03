# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 22:34:02 2019

@author: Mac

按随手网的模板xls写入数据

"""

import xlwt
import os

class SuiEntry():
    def __init__(self, date='', cat1='', cat2='', account1='', account2='', 
                 amount=0, member='', merchant='', project='', detail='', classification=0):
        self.date = date
        self.cat1 = cat1
        self.cat2 = cat2
        self.account1 = account1
        self.account2 = account2
        self.amount = amount
        self.member = member
        self.merchant = merchant
        self.project = project
        self.detail = detail
        self.classification = classification


class SuiXlsTemplate():
    def __init__(self, file_path):
        def add_title(sheet, titles):
            items = titles.split(' ')
            for i in range(len(items)):
                sheet.write(0, i, items[i])

        self.file_path = file_path
        self.workbook = xlwt.Workbook(encoding='utf-8')

        titles = '交易类型 日期 分类 子分类 账户1 账户2 金额 成员 商家 项目 备注'
        self.sheet_expense = self.workbook.add_sheet("支出")
        add_title(self.sheet_expense, titles)
    
        self.sheet_income = self.workbook.add_sheet("收入")
        add_title(self.sheet_income, titles)
        
        self.sheet_transfer = self.workbook.add_sheet("转账")
        add_title(self.sheet_transfer, titles)

        self.sheet_entry_index_expense = 1
        self.sheet_entry_index_income = 1

    def add_entry(self, entry):
        if entry.classification == 0:
            sheet = self.sheet_expense
            index = self.sheet_entry_index_expense
            transaction_type = '支出'
            self.sheet_entry_index_expense += 1

        else:
            sheet = self.sheet_income
            index = self.sheet_entry_index_income
            transaction_type = '收入'
            self.sheet_entry_index_income += 1

        sheet.write(index, 0, transaction_type)
        sheet.write(index, 1, entry.date)
        sheet.write(index, 2, entry.cat1)
        sheet.write(index, 3, entry.cat2)
        sheet.write(index, 4, entry.account1)
        sheet.write(index, 5, entry.account2)
        sheet.write(index, 6, entry.amount)
        sheet.write(index, 7, entry.member)
        sheet.write(index, 8, entry.merchant)
        sheet.write(index, 9, entry.project)
        sheet.write(index, 10, entry.detail)

    def save(self, ):
        self.workbook.save(self.file_path)
        
    
if '__main__' == __name__:
    xls = SuiXlsTemplate("./cmb_test1.xls")

    entry = SuiEntry(date='2019-09-14', amount=393.00, detail='财付通-Currify咖喱南京西路')
    xls.add_entry(entry)

    entry = SuiEntry(date='2019-09-14', amount=25, detail='xxx', member='郑之颖')
    xls.add_entry(entry)

    entry = SuiEntry(date='2019-09-14', amount=25, detail='yyy', member='郑之颖', classification=1)
    xls.add_entry(entry)

    xls.save()
    