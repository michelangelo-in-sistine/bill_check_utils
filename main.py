# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 03:14:12 2019

@author: Mac
"""
import bill_checker as bc
import sys
import os.path

if "__main__" == __name__:
    if len(sys.argv) == 1:
#        bill = """
#            0806 0807 财付通-京东商城平台商户 ￥ 888.00 7007 CN 888.00 
#            0808 0809 财付通-吴宝春麦方店 ￥ 155.00 7007 CN 155.00 
#            0808 0809 财付通-上海好德便利有限公司 ￥ 15.00 7007 CN 15.00 
#            0809 0810 财付通-京东商城平台商户 ￥ 190.00 7007 CN 190.00 
#        """
        sorted_bill = bc.org(bill, print_reverse=0)
        bc.generate_xls(sorted_bill, 'test.xls')

    else:
        # 主要用法 "python main.py ./txt/cmb_1009.txt cmb_1009.xls"
        with open(sys.argv[1]) as f:
            bill_txt = f.read()
            bills = bc.org(bill_txt)
            if len(sys.argv) == 2:
                xls_file = os.path.split(sys.argv[1])[-1].split('.')[-2] + '.xls'
            else:
                xls_file = sys.argv[2]
            bc.generate_xls(bills, xls_file)
        
    
    
    
