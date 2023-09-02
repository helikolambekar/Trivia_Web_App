from selenium import webdriver
import time

run_selenium = False

if run_selenium:
    #This test only works on a windows device with the chromedriver.exe in the correct location, while the knowitall application is running in another terminal
    driver = webdriver.Chrome(executable_path='C:\Webdrivers\chromedriver.exe')
    driver.maximize_window()

#Navigate your mouse to the middle of the screen before running the test.
def test_game():

    #Check if the selenium test run is true, if not don't run it
    if run_selenium:
            #This navigates the browsesr to the game with the category 'TV Shows'
            driver.get('http://localhost:5000')
            time.sleep(1)
            driver.find_element_by_id('startgame').click()
            time.sleep(1)
            driver.find_element_by_id("TV shows").click()
            time.sleep(1)
            driver.find_element_by_id("startgame").click()
            time.sleep(1)

            #Establish the initial state of the game
            elem = driver.find_element_by_id('div1')
            assert 'LIVES: 3/3' == elem.text

            elem = driver.find_element_by_id('SkipQuestion')
            assert 'Skip Question (3)' == elem.text

            elem = driver.find_element_by_id('FiftyFifty')
            assert '50/50 (3)' == elem.text

            first_question = driver.find_element_by_id('question').text

            #Select an answer and submit it - we want to find a wrong one, but we can't get the answer location without being logged in and that isn't part of this test
            driver.find_element_by_id("option_1").click()
            time.sleep(1)
            driver.find_element_by_id('submit').click()
            time.sleep(1)
            driver.find_element_by_id('next').click()
            time.sleep(1)

            #Use both the life lines so that they're background logic is called
            driver.find_element_by_id('FiftyFifty').click()
            time.sleep(1)
            driver.find_element_by_id('SkipQuestion').click()

            #Select another answer and submit it, this is so it is very likely that we have submitted a wrong answer and lives have decremented once (87.5% of the time)
            driver.find_element_by_id("option_1").click()
            time.sleep(1)
            driver.find_element_by_id('submit').click()
            time.sleep(1)
            driver.find_element_by_id('next').click()
            time.sleep(1)

            #Check the current state of the game
            elem = driver.find_element_by_id('div1')
            assert 'LIVES: 2/3' or 'LIVES: 1/3' == elem.text

            elem = driver.find_element_by_id('SkipQuestion')
            assert 'Skip Question (2)' == elem.text

            elem = driver.find_element_by_id('FiftyFifty')
            assert '50 / 50 (2)' == elem.text

            fourth_question = driver.find_element_by_id('question').text
            assert first_question != fourth_question
            time.sleep(1)


            driver.close()
            driver.quit()





