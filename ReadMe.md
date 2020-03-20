# FSND: Capstone Project

## Content

1. [Motivation](#motivation)
2. [Start Project locally](#start-locally)
3. [API Documentation](#api)
4. [Authentification](#authentification)

<a name="motivation"></a>
## Motivations & Covered Topics

Capstone in the `Udacity-Full-Stack-Nanodegree` Course.
It covers:

1. Database modeling with `postgres` & `sqlalchemy` (see `models.py`)
2. API to performance CRUD Operations on database with `Flask` (see `app.py`)
3. Automated testing with `Unittest` (see `test_app`)
4. Authorization & Role based authentication control with `Auth0` (see `auth.py`)
5. web server deployment on `Heroku`

<a name="local run"></a>
## Start Project locally

You need the latest version of [Python 3](https://www.python.org/downloads/)
and [postgres](https://www.postgresql.org/download/) installed on your machine.

To start and run the local development server,

1. Initialize and activate a virtualenv:
  ```bash
  $ virtualenv --no-site-packages env_capstone
  $ source env_capstone/scripts/activate
  ```

2. Install the dependencies:
```bash
$ pip install -r requirements.txt
```

Running this project locally means that it can´t access `Herokus` env variables.

3. Change Model.py so it can connect to your local postgres database. 
    - comment out ```database_path= os.environ['DATABASE_URL']```
    - uncomment the two lines below and fill in your postgres database information

4. Setup Auth0
    If you only want to test the API (i.e. Project Reviewer), you can get bearer tokend from config files. 
    

5. Run the development server:
  ```bash 
  $ python app.py
  ```

6. (optional) To execute tests, run
```bash 
$ python test_app.py
```
If you choose to run all tests, it should give this response if everything went fine:

```bash
$ python test_app.py
.........................
----------------------------------------------------------------------
Ran 25 tests in 18.132s

OK

```
## API Documentation
<a name="api"></a>

Here you can find all existing endpoints, which methods can be used, how to work with them & example responses you´ll get.

Additionally, common pitfalls & error messages are explained, if applicable.

### Base URL

**https://fsnd-capstone-alo.herokuapp.com/**

### How to work with each endpoint

Click on a link to directly get to the ressource.

1. Donor
   1. [GET /donors]
   2. [POST /donors]
   3. [DELETE /donors/<donor_id>]
   4. [PATCH /donors/<donor_id>]
2. Program
   1. [GET /programs]
   2. [POST /programs]


# <a name="get-donors"></a>
### 1. GET /donors

Pull a list of donors

- Fetches a list of dictionaries of examples in which the keys are the ids with all available fields
- Requires permission: `get:donors`
- Returns: 
  1. List of dict of actors with following fields:
      - **integer** `id`
      - **string** `name`
      - **integer** `donation`
  2. **boolean** `success`

#### Example response
```json
{
  "donors": [
    {
      "id": 1,
      "name": "Matthew",
      "donation": 20
    }
  ],
  "success": true
}
```
# <a name="get-programs"></a>
### 1. GET /programs

Pull a list of programs

- Fetches a list of dictionaries of examples in which the keys are the ids with all available fields
- Requires permission: `get:programs`
- Returns: 
  1. List of dict of actors with following fields:
      - **integer** `id`
      - **string** `division`
      - **integer** `director`
  2. **boolean** `success`

#### Example response
```json
{
  "donors": [
    {
      "id": 1,
      "division": "CRD",
      "director": "Person"
    }
  ],
  "success": true
}
```

# <a name="post-donors"></a>
### 2. POST /donors

Insert new donor into database.


- Request Arguments: **None**
- Request body: {
    "name": "bob",
    "donation": 100
}
- Requires permission: `post:donors`


#### Example response
```{
    "donors": [
        {
            "donation": 3,
            "id": 6,
            "name": "Humanish"
        }
    ],
    "success": true
}
```

# <a name="post-programs"></a>
### 2. POST /programs

Insert new program into database.


- Request Arguments: **None**
- Request body: {
    "division": "Green",
    "director": "Humans"
}
- Requires permission: `post:programs`

#### Example response
```{
    "programs": [
        {
            "division": "Green,
            "id": 6,
            "name": "Humans"
        }
    ],
    "success": true
}
```


# <a name="patch-donors"></a>
### 3. PATCH /donors

Edit an existing donor


- Request Arguments: **integer** `id from actor you want to update`
- Request Headers: (_application/json_)
       1. **string** `name` 
       2. **integer** `donation` 
- Requires permission: `post:donor`

#### Example response
{
    "donors": {
        "donation": 2090,
        "id": 4,
        "name": "Humanish"
    },
    "success": true
}


# <a name="delete-donors"></a>
### 4. DELETE /donors

Delete an existing donor

- Request Arguments: **integer** `id from donor you want to delete`
- Request Headers: `None`
- Requires permission: `delete:donor`

#### Example response
```js
{
    "delete": 1,
    "success": true
}

```

# the last on is just "/" 
    this is just to ensure the app is actually running
    no requests
    it returns hello