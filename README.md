# qtspider

* qtspider is a spider specifically targeting quantnet.com. You can use it to download quantnet trackers as you wish.
* There are three different ways to parse raw web pages:
  1. re
  2. BeautifulSoup
  3. xpath

* Particularly, qtspider_xpath.py is the most developed one within all three files.

* result.csv contains over 4800 records of trackers.

* proxyspider.py and proxies.npy are used to solve the proxy problem.

  **NOTICE!**  Now save to csv function is abandoned and all data are collected using mongodb.