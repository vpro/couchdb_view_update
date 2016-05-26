CouchDB View Update
===================

This is a Python script that triggers view updates for all views in all design documents in all databases in all CouchDB instances that you supply as arguments to it.

Dependencies
------------

This script depends on [couchdbkit](http://couchdbkit.org/). To install or upgrade to the latest
version

1. Install couchdbkit: http://couchdbkit.org/download.html
2. Install a supported JSON module for Python. This script also requires a supported JSON module for Python. You can use
cjson (or simplejson, or probably a few others if you like). Debian/Ubuntu have a package called python-cjson, which works.

Usage
-----

Provide URL's to CouchDB instances as arguments to the script:

    $ ./couchdb_view_update.py http://localhost:5984 http://example.com

To periodically update all views, you can run this via cron.
