## Test task for Insider

###  Structure:

* .meta folder contains  requirements file with all package dependencies
* api folder with API test task for https://petstore.swagger.io/ 
* load - test task for https://www.n11.com/
* ui folder contains UI Test task for https://useinsider.com/

#### Installation
* Create virtualenv with python 3.9 and activate it
* `pip install -r .meta/requirements.txt`
* For UI tests you have to install Chrome and Firefox, after that, you can visit
https://chromedriver.chromium.org/downloads and download needed driver packages
After that you can specify path to installed Firefox and Chrome drivers in conftest_ui.py file for 
fixtures chrome_options and firefox_options
* You can specify path to drivers with cli, f.e `--driver-path /path/to/geckodriver`


#### Execution

* UI:

```bash
cd ui
pytest --driver Chrome tests/test_insider.py
```

* API:

```bash
cd api
pytest --alluredir=allure_results -v tests
allure serve allure_results
```

* Load

```bash
cd load
locust --host=https://www.n11.com -f n11_load_test.py
```

#### Notes
Projects were done all in one to not create few different repositories for different subtasks

From CI/CD perspective drivers will be configured in different way, such approach written here is only for local development and for test task purposes. 
