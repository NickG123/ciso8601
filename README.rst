========
ciso8601
========

.. image:: https://circleci.com/gh/closeio/ciso8601/tree/master.svg?style=svg&circle-token=72fc522063916cb1c6c5c9882b97db9d2ed651d8
    :target: https://circleci.com/gh/closeio/ciso8601/tree/master

``ciso8601`` converts `ISO 8601`_ date time strings into Python datetime objects.
Since it's written as a C module, it is much faster than other Python libraries.
Tested with Python 2.7, 3.4, 3.5, 3.6, 3.7b.

.. _ISO 8601: https://en.wikipedia.org/wiki/ISO_8601

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

  +------------+----------+----------+----------+----------+-----------------------------------+
  |   Module   |Python 3.6|Python 3.5|Python 3.4|Python 2.7|Relative Slowdown (versus ciso8601)|
  +============+==========+==========+==========+==========+===================================+
  |ciso8601    |122 nsec  |117 nsec  |132 nsec  |105 nsec  |                                   |
  +------------+----------+----------+----------+----------+-----------------------------------+
  |udatetime   |711 nsec  |734 nsec  |770 nsec  |659 nsec  |5.8122x                            |
  +------------+----------+----------+----------+----------+-----------------------------------+
  |str2date    |6.81 usec |6.61 usec |8.41 usec |6.23 usec |55.717x                            |
  +------------+----------+----------+----------+----------+-----------------------------------+
  |iso8601utils|9.37 usec |9.22 usec |12 usec   |10.4 usec |76.589x                            |
  +------------+----------+----------+----------+----------+-----------------------------------+
  |pendulum    |9.53 usec |9.23 usec |11.9 usec |10.5 usec |77.92x                             |
  +------------+----------+----------+----------+----------+-----------------------------------+
  |iso8601     |9.8 usec  |9.7 usec  |13.5 usec |25.5 usec |80.142x                            |
  +------------+----------+----------+----------+----------+-----------------------------------+
  |isodate     |10.2 usec |10.8 usec |13.9 usec |43.4 usec |83.697x                            |
  +------------+----------+----------+----------+----------+-----------------------------------+
  |PySO8601    |15.4 usec |16 usec   |19.6 usec |16.3 usec |126.14x                            |
  +------------+----------+----------+----------+----------+-----------------------------------+
  |aniso8601   |20.9 usec |23.6 usec |31.5 usec |22.3 usec |171.06x                            |
  +------------+----------+----------+----------+----------+-----------------------------------+
  |zulu        |24.9 usec |24.1 usec |32 usec   |42.4 usec |203.38x                            |
  +------------+----------+----------+----------+----------+-----------------------------------+
  |maya        |48.2 usec |48.4 usec |60.3 usec |51.5 usec |394.23x                            |
  +------------+----------+----------+----------+----------+-----------------------------------+
  |arrow       |60.1 usec |57 usec   |77.3 usec |68.4 usec |491.26x                            |
  +------------+----------+----------+----------+----------+-----------------------------------+
  |dateutil    |71.9 usec |73.6 usec |92.1 usec |131 usec  |587.98x                            |
  +------------+----------+----------+----------+----------+-----------------------------------+
  |moment      |2 msec    |2.06 msec |3.1 msec  |2.39 msec |16316x                             |
  +------------+----------+----------+----------+----------+-----------------------------------+

ciso8601 takes 122 nsec, which is **5.8122x faster than udatetime**, the next fastest ISO 8601 parser in this comparison.

.. </include:benchmark_with_no_time_zone.rst>

Parsing a timestamp with time zone information (ex. ``2014-01-09T21:48:00-05:30``):

.. <include:benchmark_with_time_zone.rst>

.. table::

  +------------+----------+----------+----------+----------+-----------------------------------+
  |   Module   |Python 3.6|Python 3.5|Python 3.4|Python 2.7|Relative Slowdown (versus ciso8601)|
  +============+==========+==========+==========+==========+===================================+
  |ciso8601    |279 nsec  |234 nsec  |325 nsec  |308 nsec  |                                   |
  +------------+----------+----------+----------+----------+-----------------------------------+
  |udatetime   |867 nsec  |864 nsec  |912 nsec  |835 nsec  |3.1076x                            |
  +------------+----------+----------+----------+----------+-----------------------------------+
  |str2date    |8.33 usec |8.17 usec |10.6 usec |7.68 usec |29.844x                            |
  +------------+----------+----------+----------+----------+-----------------------------------+
  |iso8601     |14 usec   |13.7 usec |19.4 usec |31.1 usec |50.265x                            |
  +------------+----------+----------+----------+----------+-----------------------------------+
  |pendulum    |14 usec   |15.9 usec |19.9 usec |14.2 usec |50.331x                            |
  +------------+----------+----------+----------+----------+-----------------------------------+
  |isodate     |14.6 usec |17.6 usec |21 usec   |48.8 usec |52.18x                             |
  +------------+----------+----------+----------+----------+-----------------------------------+
  |PySO8601    |27.6 usec |25.8 usec |33.1 usec |25.9 usec |99.069x                            |
  +------------+----------+----------+----------+----------+-----------------------------------+
  |iso8601utils|28.3 usec |27.6 usec |33.3 usec |29.6 usec |101.41x                            |
  +------------+----------+----------+----------+----------+-----------------------------------+
  |zulu        |29.3 usec |29.1 usec |37.8 usec |48.8 usec |104.97x                            |
  +------------+----------+----------+----------+----------+-----------------------------------+
  |aniso8601   |30.4 usec |32.2 usec |42 usec   |26.8 usec |109.04x                            |
  +------------+----------+----------+----------+----------+-----------------------------------+
  |maya        |58.9 usec |66.4 usec |83.2 usec |59.7 usec |211.22x                            |
  +------------+----------+----------+----------+----------+-----------------------------------+
  |arrow       |72.8 usec |67.8 usec |92.5 usec |80.6 usec |260.83x                            |
  +------------+----------+----------+----------+----------+-----------------------------------+
  |dateutil    |98.5 usec |96.7 usec |119 usec  |153 usec  |352.87x                            |
  +------------+----------+----------+----------+----------+-----------------------------------+
  |moment      |1.03 sec  |975 msec  |1.36 sec  |1.22 sec  |3.6908e+06x                        |
  +------------+----------+----------+----------+----------+-----------------------------------+

ciso8601 takes 279 nsec, which is **3.1076x faster than udatetime**, the next fastest ISO 8601 parser in this comparison.

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
