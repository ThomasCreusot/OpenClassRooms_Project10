# OpenClassRooms_Project10
Create a secure RESTful API using Django REST


# Project presentation
The present project is the tenth one of the training course *Python Application Developer*, offered by OpenClassRooms and aims to *Create a secure RESTful API using Django REST*.

The main goal is to develop an **issue tracking system** wich allows users to **post and get technical issues**. 

This API must:
- be useful for websites, Android and iOS applications
- allow users to create projects, add contributors (users) to projects, create issues related to projects and comments related to issues.

Specifications:
- signup and login : user JWT authentification (tokens)
- Project is an entity which got collaborators (users), and each project can contain issues. A project is caracterised by a title, a description, a type (back-end, front-end, iOS or Android) and an author_user_id
- A project is accessible only to its contributors
- A user can CRUD an issue only if he/she is a contributor of the project.
- An issue is caracterised by a title, a description, an assignee, a priority, a tag, a status, a project_id and a created_time
- Contributors of a project can comment an issue. A comment is caracterised by a description, an author_user_id, an issue_id and a comment_id.
- **A project/issue/comment can be updated or deleted only by its author.**

- For details, please refer to the [endpoints documentation](https://documenter.getpostman.com/view/20371598/2s83tCLDEC).


# Project execution
To correctly execute the program, you need to activate the associated virtual environment which has been recorded in the ‘requirements.txt’ file.

## To create and activate the virtual environment 
Please follow theses instructions:

1. Open your Shell 
-Windows: 
>'windows + R' 
>'cmd'  
-Mac: 
>'Applications > Utilitaires > Terminal.app'

2. Find the folder which contains the program (with *cd* command)

3. Create a virtual environment: write the following command in the console
>'python -m venv env'

4. Activate this virtual environment : 
-Linux or Mac: write the following command in the console
>'source env/bin/activate'
-Windows: write the following command in the console 
>'env\Scripts\activate'

5. Install the python packages recorded in the *requirements.txt* file : write in the console the following command
>'pip install -r requirements.txt'

## To launch the server
Please follow this instruction
6. Execute the code : write the following command in the console (Python must be installed on your computer and virtual environment must be activated)
>'python manage.py runserver'

## To access to the API
7. Open POSTMAN (for example) and create an account by making a POST request on http://127.0.0.1:8000/api/signup/
Please, inform the following fields in the request body : username, password, first_name, last_name, email

8. Once your account is created, you can make a POST request on http://127.0.0.1:8000/api/token/ to get an access Token
Please, inform the following fields in the request body : username, password

9. Then, inform the following field in the request header : Authorization, with the value "Bearer TOKEN" (replace "TOKEN" by the value of your current token)

10. Please enjoy the API
