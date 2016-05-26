#!/usr/bin/env python
#
# Copyright (c) 2016 Nils Breunese <N.Breunese@vpro.nl>, VPRO Digitaal.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from couchdbkit import Server
import logging
import sys

### Configuration

# Change to logging.DEBUG to debug
log_level = logging.WARNING

# List of CouchDB instances to update views for
server_urls = sys.argv[1:]

### Program

logging.basicConfig(level=log_level)

if not server_urls:
    logging.error("Please supply one or more URL's of CouchDB instances to update views for.")
    sys.exit(1)

for server_url in server_urls:
    try:
        server = Server(server_url)
    except:
        logging.error("Could not connect to CouchDB at %s", server_url)
        continue
    logging.info("Connected to CouchDB server at %s", server_url)

    logging.info("Getting list of databases...")
    try:
        db_names = server.all_dbs()
    except:
        logging.error("Could not get list of databases for CouchDB at %s", server_url)
        continue
    logging.info("Databases: %s", ", ".join(db_names))

    for db_name in db_names:
        if db_name.startswith('_'):
            logging.info("Skipping database starting with '_': %s", db_name)
            continue

        logging.info("Database: %s", db_name)
        db = server.get_or_create_db(db_name)

        for design_doc in db.all_docs(startkey="_design", endkey="_design0", include_docs=True):
            logging.info("Design document: %s...", design_doc['id'])
            if 'views' in design_doc['doc']:
                for view in design_doc['doc']['views'].keys():
                    logging.info("View: %s", view)
                    view_name = "%s/%s" % (design_doc['id'][len('_design/'):], view)

                    # couchdbkit uses lazy dicts, so we need to do something with the ViewResult or no view request will be sent to CouchDB
                    view_result = db.view(view_name, limit=1, stale="update_after")
                    logging.info(view_result.count())
            else:
                logging.info("No views found in %s", design_doc['id'])

logging.info("All view updates requested.")
sys.exit()