========
ciso8601
========

.. image:: https://circleci.com/gh/closeio/ciso8601/tree/master.svg?style=svg&circle-token=72fc522063916cb1c6c5c9882b97db9d2ed651d8
    :target: https://circleci.com/gh/closeio/ciso8601/tree/master

``ciso8601`` converts `ISO 8601`_ date time strings into Python datetime objects.
Since it's written as a C module, it is much faster than other Python libraries.
Tested with Python 2.7, 3.4, 3.5, 3.6, 3.7b.

**Note:** ciso8601 doesn't support the entirety of the ISO 8601 spec, `only a popular subset`_.

.. _ISO 8601: https://en.wikipedia.org/wiki/ISO_8601

.. _`only a popular subset`: https://github.com/closeio/ciso8601#supported-subset-of-iso-8601

(Interested in working on projects like this? `Close.io`_ is looking for `great engineers`_ to join our team)

.. _Close.io: https://close.io
.. _great engineers: https://jobs.close.io


.. contents:: Contents


Quick Start
-----------

.. code:: bash

  % pip install ciso8601

.. code:: python

  In [1]: import ciso8601

  In [2]: ciso8601.parse_datetime('2014-12-05T12:30:45.123456-05:30')
  Out[2]: datetime.datetime(2014, 12, 5, 12, 30, 45, 123456, tzinfo=pytz.FixedOffset(330))

  In [3]: ciso8601.parse_datetime('20141205T123045')
  Out[3]: datetime.datetime(2014, 12, 5, 12, 30, 45)

Migration to v2
---------------

Version 2.0.0 of ``ciso8601`` changed the core implementation. This was not entirely backwards compatible, and care should be taken when migrating
See `CHANGELOG`_ for the Migration Guide.

.. _CHANGELOG: https://github.com/closeio/ciso8601/blob/master/CHANGELOG.md

Error Handling
--------------

Starting in v2.0.0, ``ciso8601`` offers strong guarantees when it comes to parsing strings.

``parse_datetime(dt: String): datetime`` is a function that takes a string and either:

* Returns a properly parsed Python datetime, **if and only if** the **entire** string conforms to the supported subset of ISO 8601
* Raises a ``ValueError`` with a description of the reason why the string doesn't conform to the supported subset of ISO 8601

If time zone information is provided, an aware datetime object will be returned. Otherwise, a naive datetime is returned.

Benchmark
---------

Parsing a timestamp with no time zone information (ex. ``2014-01-09T21:48:00``):

.. <include:benchmark_with_no_time_zone.rst>

.. table:: 

    +------------+----------+----------+----------+----------+-------------------------------+-----------------------------------+
    |   Module   |Python 3.7|Python 3.6|Python 3.5|Python 3.4|          Python 2.7           |Relative Slowdown (versus ciso8601)|
    +============+==========+==========+==========+==========+===============================+===================================+
    |ciso8601    |111 nsec  |112 nsec  |110 nsec  |122 nsec  |111 nsec                       |                                   |
    +------------+----------+----------+----------+----------+-------------------------------+-----------------------------------+
    |pendulum    |200 nsec  |232 nsec  |201 nsec  |266 nsec  |196 nsec                       |1.7992x                            |
    +------------+----------+----------+----------+----------+-------------------------------+-----------------------------------+
    |udatetime   |668 nsec  |691 nsec  |649 nsec  |669 nsec  |655 nsec                       |5.9982x                            |
    +------------+----------+----------+----------+----------+-------------------------------+-----------------------------------+
    |str2date    |5.77 usec |6.64 usec |6.38 usec |7.51 usec |**Incorrect Result** (``None``)|51.793x                            |
    +------------+----------+----------+----------+----------+-------------------------------+-----------------------------------+
    |iso8601utils|7.48 usec |9.1 usec  |8.52 usec |10.9 usec |9.55 usec                      |67.142x                            |
    +------------+----------+----------+----------+----------+-------------------------------+-----------------------------------+
    |iso8601     |8.26 usec |9.59 usec |9.1 usec  |11.9 usec |24.2 usec                      |74.181x                            |
    +------------+----------+----------+----------+----------+-------------------------------+-----------------------------------+
    |isodate     |8.62 usec |10 usec   |9.92 usec |12.6 usec |43.8 usec                      |77.433x                            |
    +------------+----------+----------+----------+----------+-------------------------------+-----------------------------------+
    |PySO8601    |15.9 usec |14.3 usec |14.4 usec |18 usec   |16 usec                        |142.77x                            |
    +------------+----------+----------+----------+----------+-------------------------------+-----------------------------------+
    |aniso8601   |17.4 usec |20.8 usec |21.3 usec |29.1 usec |22.4 usec                      |155.84x                            |
    +------------+----------+----------+----------+----------+-------------------------------+-----------------------------------+
    |zulu        |20.4 usec |25 usec   |26.5 usec |30.8 usec |38.6 usec                      |183.23x                            |
    +------------+----------+----------+----------+----------+-------------------------------+-----------------------------------+
    |maya        |47.4 usec |54 usec   |50.1 usec |64.7 usec |51.7 usec                      |425.83x                            |
    +------------+----------+----------+----------+----------+-------------------------------+-----------------------------------+
    |arrow       |55.7 usec |58.9 usec |53.1 usec |73.9 usec |63.4 usec                      |500.51x                            |
    +------------+----------+----------+----------+----------+-------------------------------+-----------------------------------+
    |dateutil    |58.5 usec |68.2 usec |70.6 usec |83.9 usec |135 usec                       |525.23x                            |
    +------------+----------+----------+----------+----------+-------------------------------+-----------------------------------+
    |moment      |2.01 msec |2.15 msec |1.8 msec  |3.23 msec |2.67 msec                      |18010x                             |
    +------------+----------+----------+----------+----------+-------------------------------+-----------------------------------+

ciso8601 takes 111 nsec, which is **1.7992x faster than pendulum**, the next fastest ISO 8601 parser in this comparison.

.. </include:benchmark_with_no_time_zone.rst>

Parsing a timestamp with time zone information (ex. ``2014-01-09T21:48:00-05:30``):

.. <include:benchmark_with_time_zone.rst>

.. table:: 

    +------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-----------------------------------+
    |   Module   |          Python 3.7           |          Python 3.6           |          Python 3.5           |          Python 3.4           |          Python 2.7           |Relative Slowdown (versus ciso8601)|
    +============+===============================+===============================+===============================+===============================+===============================+===================================+
    |ciso8601    |163 nsec                       |287 nsec                       |239 nsec                       |308 nsec                       |291 nsec                       |                                   |
    +------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-----------------------------------+
    |pendulum    |225 nsec                       |233 nsec                       |241 nsec                       |291 nsec                       |212 nsec                       |1.3788x                            |
    +------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-----------------------------------+
    |udatetime   |778 nsec                       |812 nsec                       |796 nsec                       |857 nsec                       |754 nsec                       |4.7727x                            |
    +------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-----------------------------------+
    |str2date    |7 usec                         |7.58 usec                      |7.63 usec                      |9.6 usec                       |**Incorrect Result** (``None``)|42.936x                            |
    +------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-----------------------------------+
    |iso8601     |11.7 usec                      |13.1 usec                      |13 usec                        |17.1 usec                      |28.5 usec                      |71.727x                            |
    +------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-----------------------------------+
    |isodate     |11.8 usec                      |13.6 usec                      |14.4 usec                      |18.4 usec                      |44.1 usec                      |72.651x                            |
    +------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-----------------------------------+
    |iso8601utils|21.5 usec                      |24.9 usec                      |26.4 usec                      |32 usec                        |27.9 usec                      |131.61x                            |
    +------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-----------------------------------+
    |PySO8601    |22.1 usec                      |24.4 usec                      |26.3 usec                      |28.4 usec                      |23.9 usec                      |135.43x                            |
    +------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-----------------------------------+
    |zulu        |24.2 usec                      |27.5 usec                      |30.4 usec                      |33 usec                        |46.5 usec                      |148.29x                            |
    +------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-----------------------------------+
    |aniso8601   |24.5 usec                      |30.6 usec                      |28.9 usec                      |38.3 usec                      |25.7 usec                      |150.09x                            |
    +------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-----------------------------------+
    |maya        |55.4 usec                      |61.4 usec                      |60.4 usec                      |74.8 usec                      |60.3 usec                      |339.58x                            |
    +------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-----------------------------------+
    |arrow       |64.9 usec                      |64.8 usec                      |65.2 usec                      |79.7 usec                      |69.6 usec                      |397.89x                            |
    +------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-----------------------------------+
    |dateutil    |73.4 usec                      |85.7 usec                      |88.8 usec                      |104 usec                       |143 usec                       |450.31x                            |
    +------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-----------------------------------+
    |moment      |**Incorrect Result** (``None``)|**Incorrect Result** (``None``)|**Incorrect Result** (``None``)|**Incorrect Result** (``None``)|**Incorrect Result** (``None``)|7.4274e+06x                        |
    +------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-----------------------------------+

ciso8601 takes 163 nsec, which is **1.3788x faster than pendulum**, the next fastest ISO 8601 parser in this comparison.

.. </include:benchmark_with_time_zone.rst>

.. <include:benchmark_module_versions.rst>

Tested on Linux 3.10.0-693.21.1.el7.x86_64 using the following modules:

.. code:: python

  PySO8601==0.2.0
  aniso8601==3.0.0
  arrow==0.12.1
  ciso8601==2.0.1
  dateutil==2.7.3
  iso8601==0.1.12
  iso8601utils==0.1.2
  isodate==0.6.0
  maya==0.5.0
  moment==0.8.2
  pendulum==1.5.1
  str2date==0.905
  udatetime==0.0.16
  zulu==0.12.0

.. </include:benchmark_module_versions.rst>

**Note:** ciso8601 doesn't support the entirety of the ISO 8601 spec, `only a popular subset`_.

For full benchmarking details (or to run the benchmark yourself), see `benchmarking/README.rst`_

.. _`benchmarking/README.rst`: https://github.com/closeio/ciso8601/blob/master/benchmarking/README.rst

Dependency on pytz (Python 2)
-----------------------------

In Python 2, ``ciso8601`` uses the `pytz`_ library while parsing timestamps with time zone information. This means that if you wish to parse such timestamps, you must first install ``pytz``:

.. _pytz: http://pytz.sourceforge.net/

.. code:: python
  
  pip install pytz

Otherwise, ``ciso8601`` will raise an exception when you try to parse a timestamp with time zone information:

.. code:: python
  
  In [2]: ciso8601.parse_datetime('2014-12-05T12:30:45.123456-05:30')
  Out[2]: ImportError: Cannot parse a timestamp with time zone information without the pytz dependency. Install it with `pip install pytz`.

``pytz`` is intentionally not an explicit dependency of ``ciso8601``. This is because many users use ``ciso8601`` to parse only naive timestamps, and therefore don't need this extra dependency.
In Python 3, ``ciso8601`` makes use of the built-in `datetime.timezone`_ class instead, so pytz is not necessary.

.. _datetime.timezone: https://docs.python.org/3/library/datetime.html#timezone-objects

Supported Subset of ISO 8601
----------------------------

``ciso8601`` only supports the most common subset of ISO 8601.

Date Formats
^^^^^^^^^^^^

The following date formats are supported:

.. table::
   :widths: auto

   ============================= ============== ==================
   Format                        Example        Supported
   ============================= ============== ==================
   ``YYYY-MM-DD``                ``2018-04-29`` ✅
   ``YYYY-MM``                   ``2018-04``    ✅
   ``YYYYMMDD``                  ``2018-04``    ✅
   ``--MM-DD`` (omitted year)    ``--04-29``    ❌              
   ``--MMDD`` (omitted year)     ``--0429``     ❌
   ``±YYYYY-MM`` (>4 digit year) ``+10000-04``  ❌   
   ``+YYYY-MM`` (leading +)      ``+2018-04``   ❌   
   ``-YYYY-MM`` (negative -)     ``-2018-04``   ❌   
   ============================= ============== ==================

Week dates or ordinal dates are not currently supported.

.. table::
   :widths: auto

   ============================= ============== ==================
   Format                        Example        Supported
   ============================= ============== ==================
   ``YYYY-Www`` (week date)      ``2009-W01``   ❌
   ``YYYYWww`` (week date)       ``2009W01``    ❌
   ``YYYY-Www-D`` (week date)    ``2009-W01-1`` ❌
   ``YYYYWwwD`` (week date)      ``2009-W01-1`` ❌
   ``YYYY-DDD`` (ordinal date)   ``1981-095``   ❌
   ``YYYYDDD`` (ordinal date)    ``1981095``    ❌ 
   ============================= ============== ==================

Time Formats
^^^^^^^^^^^^

Times are optional and are separated from the date by the letter ``T``.

Consistent with `RFC 3339`_, ``ciso860`` also allows either a space character, or a lower-case ``t``, to be used instead of a ``T``.

.. _RFC 3339: https://stackoverflow.com/questions/522251/whats-the-difference-between-iso-8601-and-rfc-3339-date-formats)

The following time formats are supported:

.. table::
   :widths: auto

   =================================== =================== ==============  
   Format                              Example             Supported          
   =================================== =================== ============== 
   ``hh``                              ``11``              ✅ 
   ``hhmm``                            ``1130``            ✅ 
   ``hh:mm``                           ``11:30``           ✅ 
   ``hhmmss``                          ``113059``          ✅ 
   ``hh:mm:ss``                        ``11:30:59``        ✅ 
   ``hhmmss.ssssss``                   ``113059.123456``   ✅ 
   ``hh:mm:ss.ssssss``                 ``11:30:59.123456`` ✅ 
   ``hhmmss,ssssss``                   ``113059,123456``   ✅ 
   ``hh:mm:ss,ssssss``                 ``11:30:59,123456`` ✅ 
   Midnight (special case)             ``24:00:00``        ✅               
   ``hh.hhh`` (fractional hours)       ``11.5``            ❌               
   ``hh:mm.mmm`` (fractional minutes)  ``11:30.5``         ❌               
   =================================== =================== ============== 

**Note:** Python datetime objects only have microsecond precision (6 digits). Any additional precision will be truncated.

Time Zone Information
^^^^^^^^^^^^^^^^^^^^^

Time zone information may be provided in one of the following formats:

.. table::
   :widths: auto

   ========== ========== =========== 
   Format     Example    Supported          
   ========== ========== =========== 
   ``Z``      ``Z``      ✅
   ``z``      ``z``      ✅
   ``±hh``    ``+11``    ✅
   ``±hhmm``  ``+1130``  ✅
   ``±hh:mm`` ``+11:30`` ✅
   ========== ========== ===========

While the ISO 8601 specification allows the use of MINUS SIGN (U+2212) in the time zone separator, ``ciso8601`` only supports the use of the HYPHEN-MINUS (U+002D) character.

Consistent with `RFC 3339`_, ``ciso860`` also allows a lower-case ``z`` to be used instead of a ``Z``.

Ignoring Timezone Information While Parsing
-------------------------------------------

It takes more time to parse timestamps with time zone information, especially if they're not in UTC. However, there are times when you don't care about time zone information, and wish to produce naive datetimes instead.
For example, if you are certain that your program will only parse timestamps from a single time zone, you might want to strip the time zone information and only output naive datetimes.

In these limited cases, there is a second function provided.
``parse_datetime_as_naive`` will ignore any time zone information it finds and, as a result, is faster for timestamps containing time zone information.

.. code:: python

  In [1]: import ciso8601

  In [2]: ciso8601.parse_datetime_as_naive('2014-12-05T12:30:45.123456-05:30')
  Out[2]: datetime.datetime(2014, 12, 5, 12, 30, 45, 123456)

NOTE: ``parse_datetime_as_naive`` is only useful in the case where your timestamps have time zone information, but you want to ignore it. This is somewhat unusual.
If your timestamps don't have time zone information (i.e. are naive), simply use ``parse_datetime``. It is just as fast.
