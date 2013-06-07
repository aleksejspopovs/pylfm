pylfm
=====

pylfm is a simple Python client for Last.fm's API. Its functionality is limited to what I needed myself, but feature and/or pull requests are welcome.

pylfm lacks documentation at the moment, though the code should be simple enough. I'd love to say that the absence of documentation is only temporary, but I don't want to promise anything.

Dependencies
============

pylfm and supplied tools require Python 3, as well as the following libraries:

* `python-requests`
* `python-lxml`

pylfm is developed and tested under Linux. Feedback regarding other platforms is welcome.

Tools
=====

Unless specified otherwise, tools export fetched data in python's pickle format, as well as in JSON.

* `group_artists` generates a dictionary containing all the artists ever scrobbled by users of a specified group toghether with the users who scrobbled them & their playcounts.

* `friends_bfs` runs a breadth-first search on a user's friend graph, fetching his friends, his friends' friends etc up to a specified level.
