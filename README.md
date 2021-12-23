# scrape_platzi_courses
_This is a script that obtains detailed information of Platzi courses, the query is made by career or school._

_The data obtained are:_
* **General_Info:** Route_Name, Title, Level, Course, Link.
* **Detailed_Courses:** Course, Teacher, Hours of study, Hours of practice, Quantity of classes, Avg min/class, Link.

_This project is not an api, it is a python executable._

## Starting 🚀
_To be able to use the script you must download it in your local environment, you can download it as a zip, to make it easier._

### Pre-requirements 📋
_If you don't program constantly you may have to install the following libraries, if you already have them skip this step._

_requests_
```
pip install requests
```
_bs4_
```
pip install bs4
```
_pandas_
```
pip install pandas
```
_openpyxl - This library is necessary to use pandas_
```
pip install openpyxl
```
_cloudscraper_
```
pip install cloudscraper
```


### Execution 🔧
_Now that you have all the necessary libraries installed, we can proceed to execute the script._

_1. Open the command console, locate the folder where you downloaded the project_

_2. Run the script_

```
python main.py
```

_3. Write the necessary data requested by the script_

_4. Check the folder where you downloaded the script and you will see the excel file with the data._

### Download all courses - platzi_course_analysis
_You may came from [platzi_course_analysis](https://github.com/diegomedflo/platzi_course_analysis), in this case you have to download the Notebook named **ExtractionDataPlatzi** and execute it in a Jupyter Notebook._


## Author ✒️

⌨️ con ❤️ por [diegomedflo](https://github.com/diegomedflo) 😊

Note: Since Platzi has a couldfare captcha, the library cloudscraper tries to scrape the website anyway, but sometimes it gives an error, you just have execute the code again until it works.
