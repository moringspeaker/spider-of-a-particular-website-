from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as e
import pandas as pd
import requests
import time
from bs4 import BeautifulSoup

def get_result(df):
    driver = webdriver.Chrome()
    re1=[]
    re2=[]
    for i in range(len(df)):
        url = 'https://m.medsci.cn/scale/show.do?s_id=4&id=d2252563f1'
        driver.get(url)
        LSM = driver.find_element_by_id('item1')
        CAP = driver.find_element_by_id('item2')
        AST = driver.find_element_by_id('item3')
        lsm=str(df.iloc[i].at['LSM'])
        LSM.send_keys(lsm)
        time.sleep(0.5)
        CAP.send_keys(str(df.iloc[i].at['CAP']))
        time.sleep(0.5)
        AST.send_keys(str(df.iloc[i].at['AST']))
        time.sleep(0.5)
        driver.find_element_by_id('result').click()
        time.sleep(0.3)
        driver.find_element_by_id('result2').click()
        time.sleep(0.3)
        result1=driver.find_element_by_id('result').get_attribute('value')
        result2=driver.find_element_by_id('result2').get_attribute('value')
        re1.append(result1)
        re2.append(result2)
    # df_result=pd.DataFrame.from_dict({'得分':re1,'NAS≥4 + F≥2风险（%）':re2})
    df.insert(loc=4, column='得分', value=re1)
    df.insert(loc=5, column='NAS≥4 + F≥2风险（%）', value=re2)
    return df
def read():
    df=pd.read_excel('./test.xlsx',index_col=0)
    df1=df.iloc[0:46]
    df2=df.iloc[46:len(df)]
    return df1,df2



if __name__=='__main__':
    df1,df2=read()
    df1_result=get_result(df1)
    df2_result=get_result(df2)
    df3=df1_result.append(df2_result, ignore_index = True)
    df3.to_excel('./result.xlsx',index=False)
