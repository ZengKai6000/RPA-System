from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
import json

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.set_window_size(800, 700) 
wait = WebDriverWait(driver, 30)
shortwait = WebDriverWait(driver, 2)
with open("Test.json", "r", encoding="utf-8") as file:
    data = json.load(file)

## 文字 ## 多行文字 ## 數字 ## 關聯性
def fillData_Text(element, inputText):
    element.click()
    action = ActionChains(driver)
    action.send_keys(inputText)
    action.perform()

  
## 下拉選單
def fillData_dropdown(element, inputText):
    element.click()
    option = wait.until(EC.visibility_of_element_located((By.XPATH, f"//li[@class='el-select-dropdown__item']/span[text()='{inputText}']")))
    action = ActionChains(driver)
    time.sleep(0.5)
    action.move_to_element(option).click().perform()
    

## 單選
def fillData_radiogroup(element, inputText):
    labels = element.find_elements(By.XPATH, ".//label[@role='radio']")

    for label in labels:
        radio_input = label.find_element(By.XPATH, ".//input[@class='el-radio__original']")

        if radio_input.get_attribute("value") == inputText:
            label.click()
            break
       

## 多選
def fillData_checkboxgroup(element, inputText):
    if isinstance(inputText, str):
        inputText = eval(inputText)  

    labels = element.find_elements(By.XPATH, ".//label[@class='el-checkbox']")

    for text in inputText:
        for label in labels:
            checkbox_input = label.find_element(By.XPATH, ".//input[@class='el-checkbox__original']")
            if checkbox_input.get_attribute("value") == text:
                label.click()
                break  


## 時間
def fillData_dateandtime(element, inputText):
    element.click()
    element.find_element(By.XPATH, './input').send_keys(inputText)
    action = ActionChains(driver)
    action.move_by_offset(10, 10).click().perform()


## 標籤
def fillData_tag(element, inputText):
    element.click()
    action = ActionChains(driver)
    action.send_keys(inputText)
    action.send_keys(Keys.RETURN)
    action.perform()


## 流程人員
def fillData_people(block, value, idx):
    block.click()
    action = ActionChains(driver)
    action.send_keys(value)
    action.perform()
    dropdown_item = driver.find_elements(By.XPATH, "/html/body/*/div/div/div/ul/li[2]")[idx]
    dropdown_item.click()
    


## 進階表單
def fillData_advancedform(idx,inputList):
    time.sleep(0.5)
    for column_idx , column_item in enumerate(inputList):
        if column_idx > 0:
            element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[%d]/div[%d]/button' %(idx,column_idx+1))))
            element.click()
        element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[%d]/div[%d]/div/div[1]/span[2]/span[2]' %(idx,column_idx+1))))
        element.click()
        num = 1
        column = 1
        while column>0:
            try:
                column += 1
                element = shortwait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[2]/div/div[2]/div[%d]' %column)))
                element_text = element.find_element(By.XPATH, ".").text.strip()  ## 獲取文本
                normalized_text = element_text.split(" ")[0]

                if normalized_text in column_item.keys():
                    num += 1
                    time.sleep(0.5)
                    site =  wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[2]/div/div[2]/div[%d]/div/span[2]/div' %num)))
                    site_type = site.get_attribute("class")
                    if site_type == 'el-input' or site_type == 'el-textarea' or site_type == 'normalField normalField-write': ##文字、網址、多行文字、數字
                        fillData_Text(site, column_item[normalized_text])
                    elif site_type == 'el-date-editor el-input el-input--prefix el-input--suffix el-date-editor--datetime' or site_type == 'el-date-editor el-input el-input--prefix el-input--suffix el-date-editor--date': ##日期與時間
                        fillData_dateandtime(site, column_item[normalized_text])
                    elif site_type == 'el-radio-group': ##單選(資料集)、單選
                        fillData_radiogroup(site, column_item[normalized_text])
                    elif site_type == 'el-checkbox-group': ##多選(資料集)、多選
                        fillData_checkboxgroup(site, column_item[normalized_text])
                    elif site_type == 'el-select': ##下拉(資料集)
                        fillData_dropdown(site, column_item[normalized_text])
                    
            except Exception as e:
                button = driver.find_element(By.XPATH, "//button[@class='editBtn' and contains(text(),'完成')]")
                button.click()
                break
    

def initialization():
    url = "https://member.gsscloud.com/cas/login?service=https%3A%2F%2Fbizform.vitalyun.com%2FBackend%2Fsignin-cas%3Fstate%3DlsQ85OqVxz1o1K20PJGrEsFlxUmIiFY0WROZWrfEUWByJmNwu9TKZk2dslBGW9-Jc0mLqStzLiTT-nglYmUWvdLDj4TCEd_524UohEFd0jCBfbFNkneQW0tNMLjDjuSnKJUZ_0neWtOrhy3bxhQWJHhzpffyPSZ5kB6prJZy-W3mbygDxs0rJiEallX_BxNkK1ey5AqxNiSJ65fOdrZ9r9KyRgvGUNc7KJxFc_4CDVw"
    driver.get(url)
    driver.find_element(By.ID, "username").send_keys('ima.intern001@gmail.com')
    driver.find_element(By.ID, "password").send_keys('intern@42838254')
    login_button = driver.find_element(By.XPATH, "//button[@type='submit' and text()='登入']")
    login_button.click()

def fillForm(formData):
    try:
        fill_form_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='button']")))
        driver.execute_script("arguments[0].scrollIntoView();", fill_form_button)
        fill_form_button.click()
        all_forms_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '全部表單樣板')]")))
        all_forms_button.click()
        search_element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="searchInput"]')))
        search_element.click()
        action = ActionChains(driver) 
        action.send_keys(formData['Title']) #搜尋解決掃不到資料的錯誤
        action.perform()
        leave_form_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='%s' and contains(text(), '%s')]" %(formData["Title"], formData["Title"]))))
        leave_form_button.click()
    except:
        print("沒有正確進入表單")
        pass
    idx = 2
    counter = 0
    while idx>0:
        try:
            idx += 1
            element = shortwait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[%d]' %idx)))
            element_text = element.find_element(By.XPATH, ".").text.strip()  ## 獲取文本
            normalized_text = element_text.splitlines()[0].strip()  # 清理多餘 只取第一
            pattern = r"^第\d+欄$"

            if re.match(pattern, normalized_text):
                fillData_advancedform(idx, formData[f"AdvancedForm{counter}"]) ## 進階表單
                counter += 1
            else:
                if normalized_text in formData.keys():
                    block = element.find_element(By.CLASS_NAME, 'column-content').find_element(By.XPATH, './span[1]/div[1]')
                    block_type = block.get_attribute("class")
                    if block_type == "el-input bizf-fields-textalign is-left" or block_type == "el-textarea bizf-fields-textalign is-left" or block_type == "normalField normalField-write bizf-fields-textalign is-left" or block_type == "el-autocomplete bizf-fields-textalign is-left": 
                        fillData_Text(block, formData[normalized_text]) ## 文字、多行文字、數字、關聯性
                    elif block_type == 'el-select bizf-fields-textalign is-left':
                        fillData_dropdown(block, formData[normalized_text]) ## 下拉選單
                    elif block_type == 'el-radio-group bizf-fields-textalign is-left':
                        fillData_radiogroup(block, formData[normalized_text]) ## 單選
                    elif block_type == 'el-checkbox-group bizf-fields-textalign is-left': 
                        fillData_checkboxgroup(block, formData[normalized_text]) ## 多選
                    elif block_type == "el-date-editor el-input el-input--prefix el-input--suffix el-date-editor--date bizf-fields-textalign is-left" or block_type == "el-date-editor el-input el-input--prefix el-input--suffix el-date-editor--datetime bizf-fields-textalign is-left":
                        fillData_dateandtime(block, formData[normalized_text]) ## 日期與時間      
        except Exception as e:
            break

    
    idy = 1
    while idy > 0:
        try:
            idy += 1
            element_1 = shortwait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="FormEditor"]/div/main/div/div/div[%d]' % idy)))
            element_1_text = element_1.find_element(By.XPATH, ".").text.strip()
            normalized_1_text = element_1_text.splitlines()[0].strip()

            if normalized_1_text in formData.keys():
                block_1 = element_1.find_element(By.XPATH, './div[2]/form/div/input[@class="react-autosuggest__input"]')#標籤
                fillData_tag(block_1, formData[normalized_1_text])
            else:
                continue  
        except Exception as e:
            break


    while True:
        try:
            element_2 = shortwait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="FormEditor"]/div/div/div/div/div[3]')))
            element_2_text = element_2.find_element(By.XPATH, ".").text.strip()
            lines = element_2_text.splitlines() # 將 element_2_text 轉換為多行文本
            filtered_lines = list(filter(lambda x: '第' in x and '關' in x, lines)) # 過濾出包含 "第" 和 "關" 的行
            filtered_lines_no_spaces = [line.replace(" ", "") for line in filtered_lines] # 移除每行中的空格
            matching_lines = [line for line in filtered_lines_no_spaces if line in formData.keys()] # 找到與 formData 鍵匹配的行

            numbers = [line.split("第")[1].split("關")[0] for line in matching_lines if "第" in line and "關" in line]

            for idx, number in enumerate(numbers):
                block_2 = element_2.find_element(By.XPATH, f'./div[{number}]/div[2]/div/div/div/div/div')
                fillData_people(block_2, formData['第%d關' %int(number)], idx)
            break
        except Exception as e:
            break
            

def sent():
    try:
        # Wait until the logout button is present
        sent_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="FormEditor"]/header/div[2]/button[3]')))
        sent_btn.click()
        time.sleep(10)
        back_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="wrapper"]/div[3]/div/main/div[1]/div[1]')))
        back_btn.click()
    except Exception:
        time.sleep(5)
        cancel_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="FormEditor"]/header/div[2]/button[2]')))
        cancel_btn.click()
        print("Logout button not found or took too long to appear.")

def logout():
    try:
        # Wait until the logout button is present
        avatar_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="wrapper"]/div[3]/div[2]/header/div/div[2]/span[3]/div')))
        avatar_btn.click()
        logout_btn = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div/div[4]/div')))
        logout_btn.click()
        time.sleep(5)
        alert = driver.switch_to.alert
        alert.accept()
    except Exception:
        print("Logout button not found or took too long to appear.")




def main(demandList):
    initialization()
    for i in demandList:
        fillForm(i)
        sent()
    logout()

if __name__ == '__main__':
    demandList = data
    
    main(demandList)