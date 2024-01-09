# example/urls.py
from django.urls import path
from worth2watch.views import check_empty_comments, database_test_main, delete_comment, get_top_ten, index, logInAdmin, getAuth, get_requested_movie, get_searched_movie, drop_database, log_out_admin, pull_comments, pull_content, sent_analysis, test_popular_database, total_pages, create_csv, remove_admin, get_admin_list, register_admin, admin_password_change, get_movie_names, youtube_empty_comments

urlpatterns = [
    path('getAuth', getAuth),

    path('allmovies', index),
    path('totalpages', total_pages),


    path('mod/pullcontent', pull_content),
    path('mod/log', logInAdmin),
    path('mod/logout', log_out_admin),
    path('mod/dropdatabase', drop_database),
    path('mod/createcsv', create_csv),
    path('mod/createadmin', register_admin),
    path('mod/adminlist', get_admin_list),
    path('mod/changeadminpassword', admin_password_change),
    path('mod/deleteadmin', remove_admin),
    path('mod/testpopulardb', test_popular_database),
    path('mod/checkemptycomments', check_empty_comments),
    path('mod/emptyyoutubecomments', youtube_empty_comments),
    path('mod/testdb', database_test_main),
    path('mod/deletecomments', delete_comment),

    path('movies/getmovie', get_requested_movie),
    path('movies/search', get_searched_movie),
    path('movies/topten', get_top_ten),

    path('comments/analysesentiment', sent_analysis),
    path('comments/pullcomments', pull_comments),
    path('comments/getmovienames', get_movie_names)
]
