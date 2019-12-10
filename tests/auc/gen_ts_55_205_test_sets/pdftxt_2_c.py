#!/usr/bin/env python3
# Convert test sets pasted from 3GPP TS 55.205 to C code.
 
# (C) 2016 by sysmocom s.f.m.c. GmbH <info@sysmocom.de>
#
# All Rights Reserved
#
# Author: Neels Hofmeyr <nhofmeyr@sysmocom.de>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys, os

script_dir = sys.path[0]

fields = (
  'Ki',
  'RAND',
  'OP',
  'OPc',
  'MIL3G-RES',
  'SRES#1',
  'SRES#2',
  'MIL3G-CK',
  'MIL3G-IK',
  'Kc',
)

test_sets_lines = []
test_set_lines = None

for line in [l.strip() for l in open(os.path.join(script_dir, 'ts55_205_test_sets.txt'), 'r')]:
  if line.startswith('Test Set'):
    if test_set_lines:
      test_sets_lines.append(test_set_lines)
    test_set_lines = []
  elif len(line) == 8:
    try:
      is_hex = int(line, 16)
      test_set_lines.append(line)
    except ValueError:
      pass

if test_set_lines:
  test_sets_lines.append(test_set_lines)

# Magic fixups for PDF-to-text uselessness
idx = (( 0, 10, 15, 19),
       ( 1, 11, 16, 20),
       ( 2, 12, 17, 21),
       ( 3, 13, 18, 22),
       ( 4, 14),
       ( 5, ),
       ( 6, ),
       ( 7, 23, 26, 28),
       ( 8, 24, 27, 29),
       ( 9, 25 ),
      )

test_sets = []
for l in test_sets_lines:
  test_sets.append( [ ''.join([l[i] for i in li]) for li in idx ] )

func_templ = open(os.path.join(script_dir, 'func_template.c'), 'r').read()

funcs = []
func_calls = []
nr = 0
for test_set in test_sets:
  nr += 1
  func_name = 'test_set_%d' % nr
  kwargs = dict(zip(fields, test_set))
  kwargs['func_name'] = func_name

  func_calls.append('\t%s();' % func_name)
  funcs.append(func_templ.format(**kwargs))

templ = open(os.path.join(script_dir, 'main_template.c')).read()

code = templ.replace('FUNCTIONS', '\n'.join(funcs)).replace('FUNCTION_CALLS', '\n'.join(func_calls))

print('''
/***** DO NOT EDIT THIS FILE -- THIS CODE IS GENERATED *****
 ***** by gen_ts_55_205_test_sets/pdftxt_2_c.py        *****/
''')
print(code)

