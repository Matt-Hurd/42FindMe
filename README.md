# Introduction

42Find.me is currently a clone of [Stud42](https://stud42.fr/) for 42US. The aim is to present the locations of all the students in the cluster in an effective manner.

Currently, it is only being worked on by me (Mhurd). It is running on a cloud9 server, but I aim to soon move it to a dedicated server with it's own domain.

My knowledge of webdev is extremely limited, and I am looking for more people to join the team. If you're interested please let me know.

# Instructions to Setup & Run

1. Clone the git repository into a local folder & cd into it.
2. Install the requirements: `pip install -r requirements.txt --user`
3. Run Migrations to create the database: `python manage.py migrate`
4. Start the server: `python manage.py runserver --insecure`
5. Access the Site on `http://127.0.0.1:8000`

# Questions and Issues

If there are any issues, feel free to bring it up in the Issues Tracker. Otherwise, contact me.

# Contact

Message me on slack (mhurd) or send an email to me at <mhurd@student.42.us.org>

## Thanks

Thanks [Mfernand](https://github.com/MatiasFMolinari) for guidance on the frontend. Without him, this site would not be anywhere near where it is.

Shoutouts to [Rmichelo](https://twitter.com/angrevol) for the swag 404 page.
