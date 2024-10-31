from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import re

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.set_window_size(800, 700) 
wait = WebDriverWait(driver, 30)


## 文字
def fillData_Text(element, inputText):
    element.click()
    action = ActionChains(driver)
    action.send_keys(inputText)
    action.perform()

## 多行文字
def fillData_multiRowText(element, inputText):
    element.click()
    action = ActionChains(driver)
    action.send_keys(inputText)
    action.perform()
  

## 下拉選單
def fillData_dropdown(element, inputText):
    element.click()
    option = wait.until(EC.visibility_of_element_located((By.XPATH, f"//li[@class='el-select-dropdown__item']/span[text()='{inputText}']")))
    action = ActionChains(driver)
    time.sleep(1)
    action.move_to_element(option).click().perform()
    

## 數字
def fillData_number(element, inputText):
    element.click()
    action = ActionChains(driver)
    action.send_keys(inputText)
    action.perform()


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


## 關聯性
def fillData_autocomplete(element, inputText):
    element.click()
    action = ActionChains(driver)
    action.send_keys(inputText)
    action.perform()


## 標籤
def fillData_tag(element, inputText):
    element.click()
    action = ActionChains(driver)
    action.send_keys(inputText)
    action.perform()


## 流程人員
def fillData_people(block, value, idx):
    block.click()
    action = ActionChains(driver)
    action.send_keys(value)
    action.perform()
    dropdown_item = driver.find_elements(By.XPATH, "/html/body/*/div/div/div/ul/li[2]")[idx]
    dropdown_item.click()
    

## 進階表單 文字
def fillData_advancedform_input(element,inputText):
    element.cilck()

## 進階表單ing
def fillData_advancedform(idx,inputList):
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
                element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[2]/div/div[2]/div[%d]' %column)))
                element_text = element.find_element(By.XPATH, ".").text.strip()  ## 獲取文本
                normalized_text = element_text.split(" ")[0]

                if normalized_text in column_item.keys():
                    num += 1
                    site =  wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[2]/div/div[2]/div[%d]/div/span[2]/div' %num)))
                    site_type = site.get_attribute("class")
                    if site_type == 'el-input': ##文字、網址
                        fillData_Text(site, column_item[normalized_text])#未測
                    elif site_type == 'el-date-editor el-input el-input--prefix el-input--suffix el-date-editor--datetime' or site_type == 'el-date-editor el-input el-input--prefix el-input--suffix el-date-editor--date': ##日期與時間
                        fillData_dateandtime(site, column_item[normalized_text])
                    elif site_type == 'el-radio-group': ##單選(資料集)、單選
                        fillData_radiogroup(site, column_item[normalized_text])
                    elif site_type == 'el-checkbox-group': ##多選(資料集)、多選
                        fillData_checkboxgroup(site, column_item[normalized_text])
                    elif site_type == 'el-select': ##下拉(資料集)
                        fillData_dropdown(site, column_item[normalized_text])
                    elif site_type == 'el-textarea': ##多行文字
                        fillData_multiRowText(site, column_item[normalized_text])
                    elif site_type == 'normalField normalField-write': ##數字
                        fillData_number(site, column_item[normalized_text])
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
        leave_form_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='%s' and contains(text(), '%s')]" %(formData["Title"], formData["Title"]))))
        leave_form_button.click()
    except:
        pass
    ## Loop through dictionary to fill the data
    idx = 2
    counter = 0
    while idx>0:
        try:
            idx += 1
            element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[%d]' %idx)))
            print(idx)

            element_text = element.find_element(By.XPATH, ".").text.strip()  ## 獲取文本
            normalized_text = element_text.splitlines()[0].strip()  # 清理多餘 只取第一
            print(normalized_text)
            pattern = r"^第\d+欄$"

            if re.match(pattern, normalized_text):
                print("Match found")
                fillData_advancedform(idx, formData[f"AdvancedForm{counter}"]) ## 進階表單
                counter += 1
            else:
                if normalized_text in formData.keys():
                    block = element.find_element(By.CLASS_NAME, 'column-content').find_element(By.XPATH, './span[1]/div[1]')
                    block_type = block.get_attribute("class")

                    if block_type == "el-input bizf-fields-textalign is-left": 
                        fillData_Text(block, formData[normalized_text]) ## 文字
                    elif block_type == 'el-textarea bizf-fields-textalign is-left': 
                        fillData_multiRowText(block, formData[normalized_text]) ## 多行文字
                    elif block_type == 'normalField normalField-write bizf-fields-textalign is-left':
                        fillData_number(block, formData[normalized_text]) ## 數字
                    elif block_type == 'el-select bizf-fields-textalign is-left':
                        fillData_dropdown(block, formData[normalized_text]) ## 下拉選單
                    elif block_type == 'el-radio-group bizf-fields-textalign is-left':
                        fillData_radiogroup(block, formData[normalized_text]) ## 單選
                    elif block_type == 'el-checkbox-group bizf-fields-textalign is-left': 
                        fillData_checkboxgroup(block, formData[normalized_text]) ## 多選
                    elif block_type == "el-date-editor el-input el-input--prefix el-input--suffix el-date-editor--date bizf-fields-textalign is-left" or block_type == "el-date-editor el-input el-input--prefix el-input--suffix el-date-editor--datetime bizf-fields-textalign is-left":
                        fillData_dateandtime(block, formData[normalized_text]) ## 日期與時間
                    elif block_type == 'el-autocomplete bizf-fields-textalign is-left':
                        fillData_autocomplete(block, formData[normalized_text]) ## 關聯性       
        except Exception as e:
            print(e)
            break

    
    idy = 1
    while idy > 0:
        try:
            idy += 1
            element_1 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="FormEditor"]/div/main/div/div/div[%d]' % idy)))
            element_1_text = element_1.find_element(By.XPATH, ".").text.strip()
            normalized_1_text = element_1_text.splitlines()[0].strip()

            if normalized_1_text in formData.keys():
                block_1 = None
                block_1_type = None

                try:
                    block_1 = element_1.find_element(By.XPATH, './div[2]/form/div/input[@class="react-autosuggest__input"]')
                    block_1_type = "標籤"
                except NoSuchElementException:
                    pass


                if block_1_type == "標籤":
                    fillData_tag(block_1, formData[normalized_1_text])
            else:
                continue  
        except Exception as e:
            print(e)
            break

    while True:
        try:
            element_2 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="FormEditor"]/div/div/div/div/div[3]')))
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
            print(e)
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
    demandList = [{
        "Title": "RPA測試表單",
        "文字": "123",
        "多行文字": "456"
    },
    {
        "Title": "RPA測試表單",
        "文字": "賴逸庭",
        "文字填寫規則（電話）": "0909430046",
        "多行文字": "這是多行\n1\n2\n3\n4",
        "數字": "10",
        "網址": "https://faq.vitalyun.com/faq/TW/BizForm",
        "下拉選單": "選項1",
        "單選": "單選1",
        "多選": ["多選1", "多選2"],
        "日期": "2021/08/05",
        "日期與時間": "2021/08/05 17:23",
        "API關聯欄位":"(主) / ",
        "下拉選單資料集": "251231101_安泰登峰",
        "單選資料集": "200:5A",
        "多選資料集": ["th.chu_0901429403", "jw.lin_0901429431"],
        "關聯表單":"(主)今時科技派工表單",
        "AdvancedForm0":[
            {"單選(資料集)" :"批次生產", "多選(資料集)" :["業務協助","整案合作"], "下拉(資料集)" :"彭正鎧", "日期與時間1" :"2021/08/05 17:23", "日期1" :"2021/08/05", "文字1" :"文字", "多行文字1" :"這是多行\n1\n2\n3\n4", "數字1" :"123", "網址1" :"https://faq.vitalyun.com/faq/TW/BizForm", "下拉選單1" :"下拉1", "單選1" :"單選1", "多選1" :["多選1","多選2"]},
            {"單選(資料集)" :"三段式", "多選(資料集)" :["業務協助","工務協助","整案合作"], "下拉(資料集)" :"蔡坤霖", "日期與時間1" :"2021/10/08 17:23", "日期1" :"2021/10/08", "文字1" :"文字", "多行文字1" :"這是多行\n1\n2\n3\n4", "數字1" :"123", "網址1" :"https://faq.vitalyun.com/faq/TW/BizForm", "下拉選單1" :"下拉2", "單選1" :"單選3", "多選1" :["多選1","多選2","多選3"]}
        ],
        "AdvancedForm1":[
            {"單選2" :"彭正鎧", "文字2" :"文字1", "日期2" :"2021/08/05"},
            {"單選2" :"YS", "文字2" :"文字2", "日期2" :""},
            {"單選2" :"Hill", "日期2" :"2021/08/07"}
        ],
        "標籤": "標籤1",
        "第3關":"Luo, You-Siang",
        "第4關":"Luo, You-Siang",
    }]
   
    
    main(demandList)