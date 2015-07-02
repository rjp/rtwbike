# rtwbike - experiments in Eddington numbers

[Stuart Lowe][rtwbike] is going around the world on his bike.

This code groks his 'GPS log' updates and calculates his Eddington Number in a clunky fashion.

It's all very hairy and ad-hoc but it's slowly moving to a sensible set of scripts, etc.

The HTML templating is done with DOM manipulation; inspired by ['spaghetti code'][spagcode] and facilitated by [BeautifulSoup][bs4].

## Requirements

* [Python minimal Twitter](https://pypi.python.org/pypi/twitter)
* [Beautiful Soup][bs4]
* [Bootstrap](http://getbootstrap.com/)
* [SQLite3](https://www.sqlite.org/)
* [Python SQLite3](https://docs.python.org/2/library/sqlite3.html)

[rtwbike]: https://twitter.com/rtwbike
[spagcode]: http://www.workingsoftware.com.au/page/Your_templating_engine_sucks_and_everything_you_have_ever_written_is_spaghetti_code_yes_you
[bs4]: http://www.crummy.com/software/BeautifulSoup/
