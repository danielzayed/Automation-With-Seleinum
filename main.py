import re

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, expected_conditions
from confedintial import  USER,PassWord
import time
class BOT() :
    def __init__(self):
        self.driver = webdriver.Chrome("./chromedriver_win32/chromedriver")
        self.user_name, self.pass_word = USER ,PassWord
        self.checkLogin=True

    def login(self):
        self.driver.get("https://github.com/login")
        # find username/email field and send the username itself to the input field
        self.driver.find_element_by_id("login_field").send_keys(self.user_name)
        # find password input field and insert password as well
        self.driver.find_element_by_id("password").send_keys(self.pass_word)
        # click login button
        self.driver.find_element_by_name("commit").click()
        # wait the ready state to be complete
        WebDriverWait(driver=self.driver, timeout=10).until(
            lambda x: x.execute_script("return document.readyState === 'complete'")
        )

        error_message = "Incorrect username or password."
        # get the errors (if there are)
        errors = self.driver.find_elements_by_class_name("flash-error")
        # print the errors optionally
        for e in errors:
           print(e.text)
        # if we find that error message within errors, then login is failed
        if any(error_message in e.text for e in errors):
            print("[!] Login failed")
            self.checkLogin=False
            #close driver
            self.close()

        else:
            print("[+] Login successful")

    def newRepo(self):
        self.driver.get('https://github.com/new')
        self.repo = input("Enter your repository name: ")
        description = input("Enter your repository description: ")

        # Input repo name
        repoName = self.driver.find_element_by_xpath('//*[@id="repository_name"]')
        repoName.click()
        repoName.send_keys(self.repo)

        # Input repo description
        repoDes = self.driver.find_element_by_xpath('//*[@id="repository_description"]')
        repoDes.click()
        repoDes.send_keys(description)

        # Create a public repo
        public = self.driver.find_element_by_xpath('//*[@id="repository_visibility_public"]')
        public.click()

        # select to add a readme file
        checkBox = self.driver.find_element_by_xpath('//*[@id="repository_auto_init"]')
        checkBox.click()

        # create repo
        create = self.driver.find_element_by_xpath("/html/body[@class='logged-in env-production page-responsive page-new-repo intent-mouse']/div[@class='application-main ']/main[@id='js-pjax-container']/div[@class='container-md my-6 px-3 px-md-4 px-lg-5']/form[@id='new_repository']/div[@class='js-with-permission-fields']/button[@class='btn btn-primary first-in-line']")
        create.submit()
    def uploadAFile(self):
         self.driver.maximize_window()
         upload=WebDriverWait(driver=self.driver, timeout=10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"summary.btn.ml-2")))
         upload.click()
         upload_A_File= WebDriverWait(driver=self.driver, timeout=10).until(EC.presence_of_element_located((By.XPATH,"/html/body[@class='logged-in env-production page-responsive intent-mouse']/div[@class='application-main ']/div/main[@id='js-repo-pjax-container']/div[@class='container-xl clearfix new-discussion-timeline px-3 px-md-4 px-lg-5']/div[@id='repo-content-pjax-container']/div/div[@class='gutter-condensed gutter-lg flex-column flex-md-row d-flex']/div[@class='flex-shrink-0 col-12 col-md-9 mb-4 mb-md-0']/div[@class='file-navigation mb-3 d-flex flex-items-start']/details[@class='details-overlay details-reset position-relative d-block']/div/ul[@class='dropdown-menu dropdown-menu-sw']/li[3]/a[@class='dropdown-item']")))
         upload_A_File.click()
         choose_Files = self.driver.find_element_by_id("upload-manifest-files-input")
         choose_Files.send_keys("C:\\Users\\danie\\Se\\main.py")

         commit =self.driver.find_element_by_id("commit-summary-input")
         commit.send_keys("Seleinum automation code - main.py")
         option_commit=self.driver.find_element_by_id("commit-description-textarea")
         option_commit.send_keys("Seleinum code - main.p \n the file includes all the project requirements in READ.md file")
         commit_changes=self.driver.find_element_by_xpath("//button[@class='btn btn-primary js-blob-submit']")
         try:
             WebDriverWait(self.driver, 20).until(
                 expected_conditions.presence_of_element_located((By.ID,"upload-manifest-files-input")))
         except (WebDriverException, TimeoutException) as py_ex:
             print("text not found -main.py")
             print(py_ex)
             print(py_ex.args)
         time.sleep(5)
         commit_changes.submit()

    def addNoteToREADMEFile(self):
        self.repo=re.sub(r"[ ]* ",'-',self.repo)
        print(self.repo)
        self.driver.get("https://github.com/danielzayed/"+self.repo)
        edit_R=self.driver.find_element_by_css_selector("svg.octicon.octicon-pencil")
        edit_R.click()
        #write to third line in REAME file which has 2 lines .
        '''  third=WebDriverWait(self.driver,10).until(
              expected_conditions.visibility_of_element_located(
              (By.XPATH,"//div/textarea[@class='form-control file-editor-textarea js-blob-contents js-code-textarea']")
              ))'''
        third=self.driver.find_elements_by_css_selector("pre.CodeMirror-line")
        #write in forth line
        third[2].send_keys("\nNote: in order the file to run you need to provide username and password that are active :)\n "
                           + "       my username and password was not included in this page ...Please provide your username and password in confedintial.py new file :) ")
        commit=self.driver.find_element_by_id("commit-summary-input")
        commit.click()
        commit_description=self.driver.find_element_by_id("commit-description-textarea")
        commit_description.click()
        self.driver.execute_script("window.scrollTo(0,document.body.scrollheight)")
        commit_changes=self.driver.find_element_by_id("submit-file")
        commit_changes.submit()



    def close(self):
        self.driver.close()


if __name__ == "__main__":
    github = BOT()
    github.login()
    if(not github.checkLogin) :
        exit(-1)
    github.newRepo()
    github.uploadAFile()
    github.addNoteToREADMEFile()
    github.close()