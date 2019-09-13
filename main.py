# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 03:14:12 2019

@author: Mac
"""
import bill_checker as bc

if "__main__" == __name__:
    bill = """
0806 0807 财付通-京东商城平台商户 ￥ 888.00 7007 CN 888.00 
0808 0809 财付通-吴宝春麦方店 ￥ 155.00 7007 CN 155.00 
0808 0809 财付通-上海好德便利有限公司 ￥ 15.00 7007 CN 15.00 
0809 0810 财付通-京东商城平台商户 ￥ 190.00 7007 CN 190.00 
0809 0810 财付通-上海西贝飞波餐饮管理 ￥ 164.58 7007 CN 164.58 
0809 0810 财付通-麦淘亲子 ￥ 299.00 7007 CN 299.00 
0810 0811 财付通-美团点评平台商户 ￥ 188.00 7007 CN 188.00 
0811 0812 财付通-上海华氏大药房有限公 ￥ 33.00 7007 CN 33.00 
0811 0812 财付通-上海多乐之日 ￥ 49.80 7007 CN 49.80 
0812 0813 财付通-维果部落中国 ￥ 15.00 7007 CN 15.00 
0812 0813 财付通-M+cake ￥ 167.00 7007 CN 167.00 
0812 0813 财付通-美团点评平台商户 ￥ 11.10 7007 CN 11.10 
0812 0813 财付通-撷上海兴业太古店 ￥ 159.00 7007 CN 159.00 
0812 0813 财付通-维果部落中国 ￥ 15.00 7007 CN 15.00 
0814 0815 财付通-美团点评平台商户 ￥ 9.00 7007 CN 9.00 
0814 0815 财付通-全家FamilyMart ￥ 42.30 7007 CN 42.30 
0815 0816 财付通-上海晴安餐饮管理有限 ￥ 30.00 7007 CN 30.00 
0815 0816 财付通-上海多乐之日 ￥ 80.00 7007 CN 80.00 
0815 0816 财付通-上海西贝飞波餐饮管理 ￥ 298.97 7007 CN 298.97 
0815 0816 财付通-美团点评平台商户 ￥ 29.00 7007 CN 29.00 
0816 0817 腾讯财付通 ￥ 9.00 7007 CN 9.00 
0816 0817 财付通-美团点评平台商户 ￥ 11.10 7007 CN 11.10 
0816 0817 财付通-水滴筹做好事得福报 ￥ 20.00 7007 CN 20.00 
0817 0818 财付通-茗品汇上海正大乐城店 ￥ 58.00 7007 CN 58.00 
0819 0820 财付通-万物心选 ￥ 45.90 7007 CN 45.90 
0821 0822 财付通-美团点评平台商户 ￥ 11.40 7007 CN 11.40 
0821 0822 财付通-全家FamilyMart ￥ 4.00 7007 CN 4.00 
0821 0822 财付通-全家FamilyMart ￥ 19.60 7007 CN 19.60 
0821 0822 财付通-美团点评平台商户 ￥ 11.10 7007 CN 11.10 
0821 0822 财付通-美团点评平台商户 ￥ 11.10 7007 CN 11.10 
0822 0823 财付通-美团点评平台商户 ￥ 29.00 7007 CN 29.00 
0823 0824 财付通-上海金拱门食品有限公 ￥ 24.00 7007 CN 24.00 
0823 0824 财付通-美团点评平台商户 ￥ 11.40 7007 CN 11.40 
0824 0825 财付通-美团点评平台商户 ￥ 64.00 7007 CN 64.00 
0824 0825 财付通-美团点评平台商户 ￥ 388.00 7007 CN 388.00 
0824 0825 财付通-美团点评平台商户 ￥ 10.90 7007 CN 10.90 
0825 0826 财付通-全家FamilyMart ￥ 29.40 7007 CN 29.40 
0826 0827 财付通-京东商城平台商户 ￥ 399.00 7007 CN 399.00 
0826 0827 财付通-红宝石食品有限公司 ￥ 44.00 7007 CN 44.00 
0827 0828 财付通-京东商城平台商户 ￥ 64.80 7007 CN 64.80 
0827 0828 财付通-美团点评平台商户 ￥ 15.26 7007 CN 15.26 
0827 0828 财付通-美团点评平台商户 ￥ 9.00 7007 CN 9.00 
0827 0828 财付通-美团点评平台商户 ￥ 9.37 7007 CN 9.37 
0829 0830 财付通-美团点评平台商户 ￥ 11.50 7007 CN 11.50 
0829 0830 财付通-顺丰速运 ￥ 12.00 7007 CN 12.00 
0830 0831 财付通-美团点评平台商户 ￥ 14.00 7007 CN 14.00 
0830 0831 财付通-上海润全餐饮管理有限 ￥ 15.00 7007 CN 15.00 
0830 0831 财付通-美团点评平台商户 ￥ 14.00 7007 CN 14.00 
0830 0831 财付通-TNINE ￥ 88.00 7007 CN 88.00 
0830 0831 财付通-久光鲜品馆 ￥ 103.50 7007 CN 103.50 
0830 0831 财付通-全家FamilyMart ￥ 7.60 7007 CN 7.60 
0830 0831 财付通-GU ￥ 149.00 7007 CN 149.00 
0830 0831 财付通-嘉会医疗在线商城 ￥ 151.20 7007 CN 151.20 
0831 0901 财付通-奈尔宝家庭中心 ￥ 20.00 7007 CN 20.00 
0901 0902 财付通-手机充值 ￥ 99.80 7007 CN 99.80 
0901 0902 财付通-美团点评平台商户 ￥ 12.70 7007 CN 12.70 
0902 0903 财付通-上海开市客闵行店 ￥ 1,260.80 7007 CN 1,260.80 
0902 0903 财付通-开市客 Costco ￥ 299.00 7007 CN 299.00 
0903 0904 财付通-美团点评平台商户 ￥ 66.00 7007 CN 66.00 
0904 0905 财付通-名创优品上海宝山陆翔 ￥ 45.00 7007 CN 45.00 
0904 0905 财付通-茗品汇上海正大乐城店 ￥ 69.00 7007 CN 69.00 
0904 0905 财付通-京东商城平台商户 ￥ 73.90 7007 CN 73.90
    """
    
    sorted_bill = bc.org(bill, print_reverse=1)
    bc.generate_xls(sorted_bill, 'cmb_1909.xls')
    
    
