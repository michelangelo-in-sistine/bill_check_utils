# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 03:14:12 2019

@author: Mac
"""
from credit_card_bill_parser import BillParser
import sys
import os.path

if "__main__" == __name__:
    # 主要用法 "python main.py ./txt/cmb_1009.txt cmb_1009.xls"
    assert len(sys.argv) >= 2, 'usage example: python main.py ./txt/cmb_1009.txt'

    parser = BillParser()
    parser.read_credit_card_bill_file(sys.argv[1])
    parser.sort_bill()
    if len(sys.argv) == 2:
        txt_path = os.path.abspath(sys.argv[1])
        xls_file = os.path.split(sys.argv[1])[-1].split('.')[-2] + '.xls'
        xls_file = os.path.split(txt_path)[0] + '/../xls/' + os.path.split(txt_path)[1].split('.')[0] + '.xls'
        print(xls_file)
    else:
        xls_file = sys.argv[2]
    parser.write_xls(xls_file)

    
    
    
