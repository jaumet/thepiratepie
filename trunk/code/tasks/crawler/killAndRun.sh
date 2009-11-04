kill -9 `ps ax | grep crawlCategories.py | grep -v grep | awk '{print $1}'`
/home/david/local/bin/python2.5 /home/david/code/tasks/crawler/crawlCategories.py
