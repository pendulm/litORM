# MetaProgramming in Python3

## 1. Purpose

I am going to implement a _ORM_ in _Python3_. This work requires a lot of
knowledge in magic methods of _Python_, known as _MetaProgramming_.

### 1.1 What is ORM ?

ORM means Object-relational mapping, for whom has interest, please consult
the Wikipedia.

In a few words, ORM try to mapping Relational model to Object-oriented model.
There are some rules:

* One table maps to One class
* Row in table maps to instance of class
* Columns in table map to attributes type of class

### 1.2 Any ORM package already ?

Yes, quite a lot.

* SQLAlchemy
* Django ORM
* peewee
* ...

### 1.3 Why a new one ?

Well, I want to do some cool things in Python, and share whole learning progress
to others. So, I think ORM is a good choice and I could eat myself's dog foot.

## 2. First Step

