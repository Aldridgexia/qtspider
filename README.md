# qtspider: Quantnet Trackers All in One

## Introduction

qtspider is written in Python 2.7. It automatically downloads all trackers at [quantnet](https://www.quantnet.com/tracker/).

- **Tested on macOS Sierra 10.12, with Python 2.7.11**

One typical tracker looks like below,

![tracker](https://cloud.githubusercontent.com/assets/10599422/24226628/e242501e-0f3d-11e7-847a-8b011a38fba5.png)

We want to get all info in it, including program name, GPA, submitted time, etc.

You will be asked to enter your login name and password. This is to ensure the spider run without interruption. After about 4 mins, depending on your system environment, you'll get a DataFrame named df_trackers, which contains all tracker info.

## Quik Start

Tips: Make sure you installed Python 2.7

**Clone this project**

```shell
git clone https://github.com/Aldridgexia/qtspider.git
cd qtspider
```

**Get required packages (optional)**

- BeautifulSoup


- requests
- pandas
- lxml

```shell
sudo pip install -r requirements.txt
```

**Run the spider**

```shell
python qtspider_2017.py
```

**What you got**

```python
# show columns
df_trackers.columns
# output
# Index([u'days_elapsed', u'days_to_result', u'gre_awa', u'gre_q', u'gre_v',
#       u'interview', u'note', u'program_name', u'program_type', u'status',
#       u'submitted', u'ugpa', u'will_join'],
#       dtype='object')
```