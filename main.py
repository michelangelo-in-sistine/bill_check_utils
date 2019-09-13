# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 03:14:12 2019

@author: Mac
"""
import bill_checker as bc

if "__main__" == __name__:
    bill = """

0705 0706 财付通-上海能志餐饮管理有限 ￥ 29.00 7007 CN 29.00
0705 0706 财付通-美团点评平台商户 ￥ 17.32 7007 CN 17.32 
0705 0706 财付通-美团点评平台商户 ￥ 13.19 7007 CN 13.19 
0705 0706 财付通-热风 ￥ 99.90 7007 CN 99.90 
0706 0707 财付通-上海立爱教育科技有限 ￥ 15,120.00 7007 CN 15,120.00 
0706 0707 财付通-美团点评平台商户 ￥ 12.10 7007 CN 12.10 
0707 0708 财付通-泉盛公司 ￥ 90.00 7007 CN 90.00 
0707 0708 财付通-美团点评平台商户 ￥ 8.00 7007 CN 8.00 
0707 0708 财付通-巴黎贝甜（顾村缤纷绿 ￥ 89.00 7007 CN 89.00 
0708 0709 财付通-EVER+NAKED裸蛋糕（巨 ￥ 84.00 7007 CN 84.00 
0708 0709 财付通-Bistro+buiger ￥ 248.00 7007 CN 248.00 
0709 0710 腾讯财付通 ￥ 378.60 7007 CN 378.60 
0709 0710 财付通-奥依修商贸（上海）有 ￥ 349.00 7007 CN 349.00 
0709 0710 财付通-上海荟天餐饮管理有限 ￥ 51.00 7007 CN 51.00 
0711 0712 财付通-翠华餐厅（宝山店） ￥ 115.00 7007 CN 115.00 
0711 0712 财付通-美团点评平台商户 ￥ 20.00 7007 CN 20.00 
0711 0712 财付通-武汉屈臣氏个人用品商 ￥ 127.00 7007 CN 127.00 
0712 0713 财付通-美团点评平台商户 ￥ 14.29 7007 CN 14.29 
0712 0713 财付通-上海晴安餐饮管理有限 ￥ 14.00 7007 CN 14.00 
0714 0715 财付通-艾影(上海)商贸有限公 ￥ 12.00 7007 CN 12.00 
0714 0715 财付通-么么果茶大悦城 ￥ 16.00 7007 CN 16.00 
0714 0715 财付通-马上诺 ￥ 186.00 7007 CN 186.00 
0715 0716 财付通-美团点评平台商户 ￥ 8.00 7007 CN 8.00 
0715 0716 财付通-热风 ￥ 46.70 7007 CN 46.70 
0715 0716 财付通-麦卡尤娜 ￥ 21.60 7007 CN 21.60 
0715 0716 财付通-优衣库 ￥ 377.00 7007 CN 377.00 
0715 0716 财付通-京东商城平台商户 ￥ 140.80 7007 CN 140.80 
0716 0717 财付通-玩具反斗城中国 ￥ 25.70 7007 CN 25.70 
0716 0717 财付通-复旦大学附属华山医院 ￥ 6.00 7007 CN 6.00 
0716 0717 财付通-美团点评平台商户 ￥ 55.50 7007 CN 55.50 
0717 0718 财付通-上海能志餐饮管理有限 ￥ 18.00 7007 CN 18.00 
0719 0720 财付通-上海西贝飞波餐饮管理 ￥ 220.43 7007 CN 220.43 
0719 0720 财付通-鲜丰水果 ￥ 19.00 7007 CN 19.00 
0719 0720 财付通-上海晴安餐饮管理有限 ￥ 32.00 7007 CN 32.00 
0719 0720 财付通-爱婴室 ￥ 39.90 7007 CN 39.90 
0719 0720 腾讯财付通 ￥ 38.00 7007 CN 38.00 
0720 0721 财付通-上海领食餐饮管理有限 ￥ 139.00 7007 CN 139.00 
0720 0721 财付通-上海鸥翼教育科技有限 ￥ 5,000.00 7007 CN 5,000.00 
0720 0721 财付通-全家FamilyMart ￥ 6.50 7007 CN 6.50 
0720 0721 财付通-kiwi新西兰酸奶冰激凌 ￥ 25.00 7007 CN 25.00 
0720 0721 财付通-生活馆 ￥ 288.00 7007 CN 288.00 
0720 0721 财付通-美团点评平台商户 ￥ 14.00 7007 CN 14.00 
0721 0722 财付通-树实文化 ￥ 213.00 7007 CN 213.00 
0721 0722 财付通-美团点评平台商户 ￥ 86.53 7007 CN 86.53 
0721 0722 财付通-美团点评平台商户 ￥ 18.99 7007 CN 18.99 
0721 0722 财付通-Currify咖喱南京西路 ￥ 393.00 7007 CN 393.00 
0721 0722 财付通-上海大鸿运酒楼 ￥ 5.00 7007 CN 5.00 
0721 0722 腾讯财付通 ￥ 70.00 7007 CN 70.00 
0721 0722 财付通-美团点评平台商户 ￥ 82.82 7007 CN 82.82 
0722 0723 财付通-上海华氏大药房有限公 ￥ 13.20 7007 CN 13.20 
0723 0724 财付通-猫眼/格瓦拉生活 ￥ 72.00 7007 CN 72.00 
0724 0725 腾讯财付通 ￥ 15.00 7007 CN 15.00 
0725 0726 财付通-唛宜德大食堂 ￥ 3.00 7007 CN 3.00 
0725 0726 财付通-魔盒集团 ￥ 99.00 7007 CN 99.00 
0726 0727 财付通-江苏爸爸糖餐饮管理有 ￥ 70.00 7007 CN 70.00 
0726 0727 财付通-老盛昌 ￥ 15.00 7007 CN 15.00 
0726 0727 财付通-美团点评平台商户 ￥ 73.09 7007 CN 73.09 
0726 0727 财付通-老盛昌 ￥ 5.00 7007 CN 5.00 
0726 0727 拉卡拉支付有限公司 ￥ 7,049.00 7007 CN 7,049.00 
0729 0730 财付通-巴黎贝甜（顾村缤纷绿 ￥ 59.00 7007 CN 59.00 
0729 0730 财付通-叮咚买菜 ￥ 32.68 7007 CN 32.68 
0730 0731 财付通-必胜客 ￥ 146.50 7007 CN 146.50 
0730 0731 财付通-美团点评平台商户 ￥ 29.14 7007 CN 29.14 
0730 0731 财付通-美团点评平台商户 ￥ 5.00 7007 CN 5.00 
0730 0731 财付通-美团点评平台商户 ￥ 18.44 7007 CN 18.44 
0731 0801 财付通-京东商城平台商户 ￥ 269.78 7007 CN 269.78 
0801 0802 财付通-点点心港式茶餐（海宁 ￥ 318.00 7007 CN 318.00 
0801 0802 财付通-贤爸科学馆优选 ￥ 118.00 7007 CN 118.00 
0801 0802 腾讯财付通 ￥ 14.00 7007 CN 14.00 
0802 0803 财付通-久光鲜品馆 ￥ 245.90 7007 CN 245.90 
0802 0803 财付通-久光鲜品馆 ￥ 40.00 7007 CN 40.00 
0802 0803 财付通-上海银平餐厅仙霞店 ￥ 166.00 7007 CN 166.00 
0802 0803 财付通-幸福蓝海国际影城 ￥ 200.00 7007 CN 200.00 
0802 0803 腾讯财付通 ￥ 590.00 7007 CN 590.00 
0803 0804 财付通-去哪儿网 ￥ 18,046.00 7007 CN 18,046.00 
0804 0805 财付通-维果部落中国 ￥ 15.00 7007 CN 15.00 
0804 0805 财付通-美团点评平台商户 ￥ 11.90 7007 CN 11.90 
0804 0805 财付通-美团点评平台商户 ￥ 27.90 7007 CN 27.90




    """
    
    bc.org(bill, print_reverse=1)
    