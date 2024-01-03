# example/urls.py
from django.urls import path
from worth2watch.views import check_empty_comments, get_top_ten, index, logInAdmin, getAuth, get_requested_movie, get_searched_movie, drop_database, pull_comments, pull_content, test_popular_database, total_pages, create_csv, remove_admin, get_admin_list, register_admin, change_admin_password, get_movie_names, youtube_empty_comments

urlpatterns = [

    path('allmovies', index),
    path('totalpages', total_pages),


    path('mod/pullcontent', pull_content),
    path('mod/log', logInAdmin),
    path('getAuth', getAuth),
    path('mod/dropdatabase', drop_database),
    path('mod/createcsv', create_csv),
    path('mod/createadmin', register_admin),
    path('mod/adminlist', get_admin_list),
    path('mod/changeadminpassword', test_popular_database),
    path('mod/deleteadmin', remove_admin),
    path('mod/testpopulardb', test_popular_database),
    path('mod/checkemptycomments', check_empty_comments),
    path('mod/emptyyoutubecomments', youtube_empty_comments),

    path('movies/getmovie', get_requested_movie),
    path('movies/search', get_searched_movie),
    path('movies/topten', get_top_ten),

    path('comments/pullcomments', pull_comments),
    path('comments/getmovienames', get_movie_names)
]
