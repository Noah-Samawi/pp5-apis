# Wander Wise API
The testing.md file provides an overview of the testing conducted on Wander Wise webapp. It covers code validation, accessibility, performance, testing on various devices, browser compatibility, testing user stories, and user feedback and improvements. Each section describes the tools used, the issues found (if any), and the corresponding test results.

## Table of Content
1. [Code Validation](#code-validation)
2. [Automated testing](#automated-testing)
3. [Manual testing](#manual-testing)
4. [Summary](#summary)

### Code Validation 
[PEP 8](https://pep8ci.herokuapp.com/) is a style guide for writing Python code to ensure consistency and readability. It provides guidelines on how to format code, naming conventions for variables and functions, and other best practices. Following PEP 8 helps to improve code quality, readability, and maintainability.

#### Pp5-api backend
| **Tested** | **Result** | **View Result** | **Pass** |
--- | --- | --- | :---:
|serializers|No errors|[Result](/docs/testing/backend/serializers.png)| :white_check_mark:
|settings|No errors|[Result](/docs/testing/backend/settings.png)| :white_check_mark:
|urls|No errors|[Result](/docs/testing/backend/urls.png)| :white_check_mark:
|views|No errors|[Result](/docs/testing/backend/views.png)| :white_check_mark:


#### Countryside
| **Tested** | **Result** | **View Result** | **Pass** |
--- | --- | --- | :---:
|models|No errors|[Result](/docs/testing/countryside/models.png)| :white_check_mark:
|serializers|No errors|[Result](/docs/testing/countryside/serializers.png)| :white_check_mark:
|tests|No errors|[Result](/docs/testing/wanderers/tests.png)| :white_check_mark:
|urls|No errors|[Result](/docs/testing/countryside/urls.png)| :white_check_mark:
|views|No errors|[Result](/docs/testing/countryside/views.png)| :white_check_mark:

#### Comments
| **Tested** | **Result** | **View Result** | **Pass** |
--- | --- | --- | :---:
|models|No errors|[Result](/docs/testing/comments/models.png)| :white_check_mark:
|serializers|No errors|[Result](/docs/testing/comments/serializers.png)| :white_check_mark:
|tests|No errors|[Result](/docs/testing/comments/tests.png)| :white_check_mark:
|urls|No errors|[Result](/docs/testing/comments/urls.png)| :white_check_mark:
|views|No errors|[Result](/docs/testing/comments/views.png)| :white_check_mark:

#### Followers
| **Tested** | **Result** | **View Result** | **Pass** |
--- | --- | --- | :---:
|models|No errors|[Result](/docs/testing/followers/models.png)| :white_check_mark:
|merializers||[Result](/docs/testing/followers/serializers.png)| :white_check_mark:
|tests|No errors|[Result](/docs/testing/followers/tests.png)| :white_check_mark:
|urls|No errors|[Result](/docs/testing/followers/urls.png)| :white_check_mark:
|views|No errors|[Result](/docs/testing/followers/views.png)| :white_check_mark:

#### Likes
| **Tested** | **Result** | **View Result** | **Pass** |
--- | --- | --- | :---:
|models|No errors|[Result](/docs/testing/likes/models.png)| :white_check_mark:
|merializers|No errors|[Result](/docs/testing/likes/serializers.png)| :white_check_mark:
|tests|No errors|[Result](/docs/testing/likes/tests.png)| :white_check_mark:
|urls|No errors|[Result](/docs/testing/likes/urls.png)| :white_check_mark:
|views|No errors|[Result](/docs/testing/likes/views.png)| :white_check_mark:

#### Posts
| **Tested** | **Result** | **View Result** | **Pass** |
--- | --- | --- | :---:
|models|No errors|[Result](/docs/testing/posts/models.png)| :white_check_mark:
|serializers|No errors|[Result](/docs/testing/posts/serializers.png)| :white_check_mark:
|tests|No errors|[Result](/docs/testing/posts/tests.png)| :white_check_mark:
|urls|No errors|[Result](/docs/testing/posts/urls.png)| :white_check_mark:
|views|No errors|[Result](/docs/testing/posts/views.png)| :white_check_mark:

#### Wanderers
| **Tested** | **Result** | **View Result** | **Pass** |
--- | --- | --- | :---:
|models|No errors|[Result](/docs/testing/wanderers/models.png)| :white_check_mark:
|serializers|No errors|[Result](/docs//testing/wanderers/serializers.png)| :white_check_mark:
|tests|No errors|[Result](/docs/testing/wanderers/tests.png)| :white_check_mark:
|urls|No errors|[Result](/docs/testing/wanderers/urls.png)| :white_check_mark:
|views|No errors|[Result](/docs//testing/wanderers/views.png)| :white_check_mark:

Note: The specific details and validation results for each file can be viewed by expanding the corresponding sections.

### Automated testing

The application have used some automated testing to ensure the functionality of the Post API endpoints as well as the consistent extension of teh User model with the Wanderer model. Her is an overview of the tests:

**Post Listing:** To verify that the API correctly lists the posts available.
**Post Creation:** To check whether an authenticated user can successfully create a post.
**Unauthorized Post Creation:** To ensure that unauthenticated users are not allowed to create posts.
**Post Retrieval:** The test verify that posts can be retrieved using valid identifiers. Additionally, it will check that the system correctly handles retrieval requests for non-existent posts.
**Post Updates:** To confirm that a user can update their own posts, and importantly, they cannot modify other user's posts. 
**User-Wanderer Consistency:** We run tests to confirm that each user is always extended with the Wanderer model. 

To run the tests, navigate to the main directory of the project and execute the following command in the terminal:

```bash
python manage.py test 
```
Upon successful execution of the tests, you should see output similar to the following:
```bash
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
............{'id': 1, 'created_at': '28 May 2024', 'owner': 'user1', 'post': 1, 'comment': None}
.204
.OrderedDict({'count': 1, 'next': None, 'previous': None, 'results': [OrderedDict({'id': 1, 'created_at': '28 May 2024', 'owner': 'user1', 'post': 1, 'comment': None})]})
.[ErrorDetail(string='You have already liked this post.', code='invalid')]
..
----------------------------------------------------------------------
Ran 17 tests in 4.161s

OK
Destroying test database for alias 'default'...
```

This signifies that all tests have passed successfully. If any test fails, the output will clearly specify which test failed and the reason to failure. If you see an output similar to the above, it means your setup is working as expected. 

### Manual testing
During the manual testing of the API, the following steps were performed:
1. Ensured that all URL paths were created correctly and functioning without any errors.
2. Verification of CRUD Functionality:
- Verified the functionality of Create, Read, Update, and Delete operations for various entities such as posts, countryside, comments, followers, likes, and wanderer
- Created new items and confirmed the proper functioning of the corresponding URLs
- Verified the Edit functionality (excluding followers and likes).
- Tested the delete function to ensure its correctness.
- Check delete function
3. Validation of Post Search Functionality:
- Tested the search functionality specifically for posts.
- Ensured that the search feature for posts was functioning as expected.

These manual testing steps were undertaken to validate the correct functioning and behavior of the API.

#### URL Testing
| **Tested** | **Expected result** | **Result** | **Pass** |
--- | --- | --- | :---:
|Root URL|Show welcome message|Works as expected| :white_check_mark:
|/countryside|Display countryside |Works as expected| :white_check_mark:
|/countryside/{id}|Display countryside detail|Works as expected| :white_check_mark:
|/posts|Display posts list |Works as expected| :white_check_mark:
|/posts/{id}|Display posts detail|Works as expected| :white_check_mark:
|/comments|Display comments list |Works as expected| :white_check_mark:
|/comments/{id}|Display comment detail|Works as expected| :white_check_mark:
|/likes|Display likes list |Works as expected| :white_check_mark:
|/likes/{id}|Display like detail|Works as expected| :white_check_mark:
|/wanderers|Display wanderers list |Works as expected| :white_check_mark:
|/wanderers/{id}|Display wanderer detail|Works as expected| :white_check_mark:
|/followers|Display followers list |Works as expected| :white_check_mark:
|/followers/{id}|Display follower detail|Works as expected| :white_check_mark:

#### CRUD functionality
| **Tested** | **Create** | **View** | **Update** | **Delete** |
--- | --- | --- | :---:| :---:
|Countryside|:white_check_mark:|:white_check_mark:|-|:white_check_mark:
|Post|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:
|Comment|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:
|Like|:white_check_mark:|:white_check_mark:|-|:white_check_mark:
|Follow|:white_check_mark:|:white_check_mark:|-|:white_check_mark:
|Wanderer|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:

#### Search functionality
- Searching for Title, Wanderer and Country is working as expected.

### Summary
The testing process for the Wander Wise API has been exhaustive and meticulous, reinforcing the robustness and reliability of the platform. Python's best coding practices were upheld by utilizing the PEP 8 tool to check for errors in each application module.

Automated testing has been a critical part of the process, covering key functionalities such as post listing, post creation, post retrieval, post updates, and user-wanderer consistency.

All tests for the Wander Wise API have been passed, demonstrating its readiness for deployment and public use. For a detailed account of the front-end testing, please  [click here](https://github.com/Noah-Samawi/pp5-apis/blob/main/TESTING.md).