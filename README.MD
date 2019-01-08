# About this project

This fun program takes an iTunes **XML** file, pulls out some of the info and converts it into a database. It is my first project using **Python**. Even though it's a tiny program and database,  I think it’s a good way to show my basic knowledge of:

* Python
* Parsing XML files
* SQL/SQLite
* Databases

---
To run this program, simply download idatabase.py, app.py (run first) and iTunes.xml (or use your own iTunes library.xml file). Open the created iTunes.sqlite  file with SQLite

---

## Database schema                  

**Artist Table** 

|  id | name  |
|:---:|:---:|
|  unique int | unique text  |

**Genre Table** 

|  id | name  |
|:---:|:---:|
|  unique int | unique text  |

**Album Table** 

|  id | artist_id  | album  |  year |
|:---:|:---:|:---:|:---:|
|  unique int | int  | unique text  | int  |

**Track Table**

|  id | song |  album_id | genre_id  | length  | count  | rating|
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
|  unique int | text  | int  | int  | int  | int  | int  |