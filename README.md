![Try Django 1.9 Logo](https://cfe-static.s3.amazonaws.com/media/try-django-19/images/try_django_19.png)

# Try Django 1.9

Try Django 1.9 is an introduction to Django version 1.9 by creating a simple, yet robust, Django blog. This series covers a variety of Django basics as well as Django 1.9 specific material. Created by Team CFE @ http://joincfe.com.

The tutorial videos are available on our [YouTube channel](http://joincfe.com/youtube) and ad-free on [Coding for Entrepreneurs](http://joincfe.com/projects/).

Subscribe to our [YouTube Channel]()

Thanks for watching!

Team CFE

---

#### it's the Same code from Team CFE with  tiny changes from me :+1:



* ##### photo while working :


![app at sleep mode](http://www13.0zz0.com/2017/06/21/04/501200483.png)

---

## Changes:

*  **like for example :**
  **Previous & Next** Button and add them to **Form1** which for Post     search, to make the page more dynamic
  ```html
 {% if queryset.has_previous %}
 <button id ="btn_post" type="submit" form="form1" name="page"
 value="{{ queryset.previous_page_number}}">Previous</button>
 {% endif %}
 ```
