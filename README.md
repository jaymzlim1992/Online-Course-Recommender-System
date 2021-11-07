---
## SECTION 1 : PROJECT TITLE
## Online-Course-Recommender-System 
!('/Miscellaneous/Home-Page.png')

## SECTION 2 : EXECUTIVE SUMMARY
With digital transformation across the world, the education sector has shown positive initiatives to embrace e-learning or online learning in the past decade. The adoption is further accelerated since Covid-19 outbreak. Schools, universities and institutions are forced to shift their operation online in order to comply with safe distancing measure. Inevitably, this has caused an exploding growth the in the online learning market. People are looking for alternatives to bricks and mortars institutions and starting to embrace the convenience of online learning.  

Nowadays, there are many online platforms that offers courses in many different topics and languages. With an internet connection, they promote the spirit of learning anything, anytime and anywhere. However, inquisitive learners searching for online courses to learn often find themselves experiencing option fatigue as there are so many options and platforms to choose from. This often leads to a longer search time and effort in order to find the best matching course to start learning.  

Our team have designed and built an Online Course Recommender System that aims to be a one-stop-platform that solves this inefficiency. Given a learner’s preference, our system is able to perform meaningful cross-platform course recommendations. Learners would no longer need to spend countless hours visiting each of the online course platforms in order to find a best matching course for their needs. 

The knowledge base of our system is constructed through data mining from the three major online course platform: Coursera, Edx and Udemy. While building the knowledge model, we utilized tools such Python and web-scrapping methods to scrape course data from the platforms. The knowledge base is represented and stored in the form of SQL database. A recommendation reasoning system is developed within our system that is capable of performing cross-platform course recommendations using a customized content-based filtering approach. The frontend user-interface is built based on a web framework using tools such as JavaScript and HTML. To integrate the system frontend and backend including the database and recommendation reasoning system, we utilized the Python Flask app to manage the routes and request across the system.  

The first version of our Online Course Recommender System serves as a prototype for proof-of-concept. Besides, we have identified future improvements such as adding more online course platforms into our knowledge base, adding more user functionalities within our system as well as further tuning and improving the recommendation algorithm.

---

## SECTION 3 : CREDITS / PROJECT CONTRIBUTION

| Official Full Name  | Student ID (MTech Applicable)  | Work Items (Who Did What) | Email (Optional) |
| :------------ |:---------------:| :-----| :-----|
| Lim Jun Ming | A0231523U | Knowledge Model, Recommendation Module, Frontend | e0703555@u.nus.edu |
| Sarah Elita Shi Yuan Wong | A0231507N | Knowledge Model, Database, Frontend | e0703539@u.nus.edu |
| Zhang Yunduo | A0231349H | Knowledge Model, Frontend, System Evaluation | e0703381@u.nus.edu |

---

## SECTION 4 : VIDEO OF SYSTEM MODELLING & USE CASE DEMO
  
<a href="https://www.youtube.com/watch?v=HqXFM_iB2zc">
<img src="Miscellaneous/Promotional Video - Image.png"
     style="float: left; margin-right: 0px;" />
</a>

IRS-PM - Online Course Recommender System - Promotional Presentation
  
<a href="https://www.youtube.com/watch?v=nqYWZMIf6C8">
<img src="Miscellaneous/Technical Presentation - Image.jpg"
     style="float: left; margin-right: 0px;" />
</a>

IRS-PM - Online Course Recommender System - Technical Presentation

---

## SECTION 5 : USER GUIDE

### Installation Guide
As the Online Course Recommender WebApp is mainly written in Python, in order to install and start using the application, Python is required to be install on the user machine. To avoid the complications and version compatibility issues of Python modules, we recommend the user to create a new python or conda environment and to install and run the WebApp in the new environment.
  
### Pre-requisite
[**Anaconda**](https://www.anaconda.com/products/individual)

### Installation Procedure
#### *Windows OS*
Follow and type in the commands below in the command prompt to execute:
  
1. Create New Conda Environment<br>
`conda create --name py39_ocrs python=3.9 -y`

2. Activate The Created Conda Environment<br>
`conda activate py39_ocrs`
 
3. Download and Clone This Github Repository into a Folder

4. Change Directory to the Cloned Github Repository Folder and Go into SystemCode Folder<br>
`cd <path to repo>\SystemCode`
  
5. Install The Required Python Packages<br>
`pip install -r requirements.txt`
  
6. Install The NLTK Corpora<br>
`python nltk_setup.py`

  
#### *Linux Ubuntu 20.04*
Follow and type in the commands below in the terminal to execute:
  
1. Create New Conda Environment<br>
`conda create --name py39_ocrs python=3.9 -y`

2. Activate The Created Conda Environment<br>
`conda activate py39_ocrs`
 
3. Download and Clone This Github Repository into a Folder

4. Change Directory to the Cloned Github Repository Folder and Go into SystemCode Folder<br>
`cd <path to repo>\SystemCode`
  
5. Install The Required Python Packages<br>
`pip install -r requirements.txt`
  
6. Install The NLTK Corpora<br>
`python nltk_setup.py`
  

### Launching The Application
Starting the WebApp is easy, user just need to navigate to the SystemCode folder in the Repository and run with python environment activated

#### *Windows OS*
Follow and type in the commands below in the command prompt to execute:
  
1. Activate The Created Conda Environment<br>
`conda activate py39_ocrs`

2. Change Directory to the Cloned Github Repository Folder and Go into SystemCode Folder<br>
`cd <path to repo>\SystemCode`
  
3. Run The Launching Python File - run.py<br>
`python run.py` 

 
#### *Linux Ubuntu 20.04*
Follow and type in the commands below in the terminal to execute:

1. Activate The Created Conda Environment<br>
`conda activate py39_ocrs`

2. Change Directory to the Cloned Github Repository Folder and Go into SystemCode Folder<br>
`cd <path to repo>\SystemCode`
  
3. Run The Launching Python File - run.py<br>
`python run.py`  
  
For more details on User Manual: <br>
`Refer to appendix <User Manual Guide> in project report at Github Folder: ProjectReport`

---
## SECTION 6 : PROJECT REPORT / PAPER

`Refer to project report at Github Folder: ProjectReport`

---
## SECTION 7 : KNOWLEDGE MODELLING

The Knowledge Models are constructed using various series of python files and notebooks.
They are saved in the following 3 folder structure:

1. Data Mining & Preparation
2. Database
3. Feature Extraction 
  
`Refer to Github Folder: KNOWLEDGE MODELLING`

---
