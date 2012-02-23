#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2012                                      ##
##                                                                       ##
## This program is free software: you can redistribute it and/or modify  ##
## it under the terms of the GNU General Public License as published by  ##
## the Free Software Foundation, either version 3 of the License, or     ##
## (at your option) any later version.                                   ##
##                                                                       ##
## This program is distributed in the hope that it will be useful,       ##
## but WITHOUT ANY WARRANTY; without even the implied warranty of        ##
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         ##
## GNU General Public License for more details.                          ##
##                                                                       ##
## You should have received a copy of the GNU General Public License     ##
## along with this program.  If not, see <http://www.gnu.org/licenses/>. ##
##                                                                       ##
###########################################################################

from Analyser_Osmosis import Analyser_Osmosis

sql10 = """
SELECT
    id,
    ST_ASText(geom)
FROM
    nodes AS nodes
    JOIN relation_members ON
        member_id = id AND
        member_type = 'N' AND
        member_role = ''
WHERE
    array_ndims(akeys(tags - 'created_by'::text - 'source'::text)) IS NULL
;
"""

sql20 = """
SELECT
    id,
    ST_ASText(ST_Centroid(linestring))
FROM
    ways
    JOIN relation_members ON
        member_id = id AND
        member_type = 'W' AND
        member_role = ''
WHERE
    array_ndims(akeys(tags - 'created_by'::text - 'source'::text)) IS NULL
;
"""

class Analyser_Osmosis_Useless_Member(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = {"item":"1140", "desc":{"fr":"Membre inutile de relation", "en":"Useless relation member"} }
        self.callback10 = lambda res: {"class":1, "data":[self.node_full, self.positionAsText]}
        self.callback20 = lambda res: {"class":2, "data":[self.way_full, self.positionAsText]}

    def analyser_osmosis_all(self):
        self.run(sql10, self.callback10)
        self.run(sql20, self.callback20)
