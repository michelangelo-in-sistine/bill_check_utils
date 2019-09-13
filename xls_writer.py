# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 22:34:02 2019

@author: Mac

按随手网的模板xls写入数据

"""

import xlwt

class ExpenseEntry():
    def __init__(self, date='', cat1='', cat2='', account1='', account2='', 
                 amount=0, member='', merchant='', project='', detail=''):
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
        
class SuiXlsTemplate():
    def __init__(self, file_path):
        self.file_path = file_path
        self.workbook = xlwt.Workbook(encoding='utf-8')

        def add_title(sheet, titles):
            items = titles.split(' ')
            for i in range(len(items)):
                sheet.write(0, i, items[i])

        titles = '交易类型 日期 分类 子分类 账户1 账户2 金额 成员 商家 项目 备注'
        self.expense_sheet = self.workbook.add_sheet("支出")
        add_title(self.expense_sheet, titles)
    
        self.income_sheet = self.workbook.add_sheet("收入")
        add_title(self.income_sheet, titles)
        
        self.transfer_sheet = self.workbook.add_sheet("转账")
        add_title(self.transfer_sheet, titles)

        self.expense_sheet_entry_index = 1

    
    def add_expense_entry(self, enpense_entry):
        self.expense_sheet.write(self.expense_sheet_entry_index, 0, '支出')
        self.expense_sheet.write(self.expense_sheet_entry_index, 1, enpense_entry.date)
        self.expense_sheet.write(self.expense_sheet_entry_index, 2, enpense_entry.cat1)
        self.expense_sheet.write(self.expense_sheet_entry_index, 3, enpense_entry.cat2)
        self.expense_sheet.write(self.expense_sheet_entry_index, 4, enpense_entry.account1)
        self.expense_sheet.write(self.expense_sheet_entry_index, 5, enpense_entry.account2)
        self.expense_sheet.write(self.expense_sheet_entry_index, 6, enpense_entry.amount)
        self.expense_sheet.write(self.expense_sheet_entry_index, 7, enpense_entry.member)
        self.expense_sheet.write(self.expense_sheet_entry_index, 8, enpense_entry.merchant)
        self.expense_sheet.write(self.expense_sheet_entry_index, 9, enpense_entry.project)
        self.expense_sheet.write(self.expense_sheet_entry_index, 10, enpense_entry.detail)
        
        self.expense_sheet_entry_index += 1
        
    def save(self, ):
        self.workbook.save(self.file_path)
        
    
if '__main__' == __name__:
#    workbook = xlwt.Workbook(encoding='utf-8')
#    worksheet = workbook.add_sheet("sheet1")
#    worksheet.write(1,1,'test2')
#    workbook.save("test.xls")
    enpense_entry = ExpenseEntry(date='2019-09-14', amount=393.00, detail = '财付通-Currify咖喱南京西路')
    xls = SuiXlsTemplate("cmb_test1.xls")
    xls.add_expense_entry(enpense_entry)

    enpense_entry = ExpenseEntry(date='2019-09-14', amount=25, detail = 'xxx', member='郑之颖')
    xls.add_expense_entry(enpense_entry)
    xls.save()
    