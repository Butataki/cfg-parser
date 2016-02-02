"""
Created on 02.02.16 13:26

This module contains examples on config parser usage

.. py:module:: cfg_parsing_example
    :synopsis: This module contains examples on config parser usage


.. moduleauthor:: Roman Shuvalov <orangato@yandex.ru>
"""
import sys
import os

# Hack if you don't want to install cfg parser and just try call example file as is
ROOT = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(ROOT))

from cfg_parser import Configuration


c = Configuration(os.path.join(ROOT, 'empty_example.cfg'))
try:
    c.get_configuration()
except IOError:
    pass

if os.path.isfile(os.path.join(ROOT, 'empty_example.cfg')):
    print 'Successfully created empty config file'
else:
    raise RuntimeError('Unexpected error. Failed to create configuration file.')

template_example = '''
[section_one]
iInterval=30
fPrice=45.67
bEnableSpoofing=1
sEntryPointClass=MainMethanina
lProxyList=127.0.0.1:3456,127.0.0.1:2333,127.0.0.1:4565

[section_two]
iAnotherInterval=45
'''

with open(os.path.join(ROOT, 'example_template.txt'), 'w+') as f:
    f.write(template_example)

c = Configuration(os.path.join(ROOT, 'example.cfg'), os.path.join(ROOT, 'example_template.txt'))
try:
    c.get_configuration()
except IOError:
    pass

if os.path.isfile(os.path.join(ROOT, 'empty_example.cfg')):
    print 'Successfully created config file from template'
else:
    raise RuntimeError('Unexpected error. Failed to create configuration file from template.')

# we call again to actually read data after new cfg file was created and filled
options = c.get_configuration()
print 'section one'
print 'interval {}={}'.format(options.section_one.interval, 30)
print 'price {}={}'.format(options.section_one.price, 45.67)
print 'enable spoofing {}={}'.format(options.section_one.enable_spoofing, True)
print 'entry point class {}={}'.format(options.section_one.entry_point_class, 'MainMethanina')
print 'proxy list {}'.format(repr(options.section_one.proxy_list))
print 'section two'
print 'another interval {}={}'.format(options.section_two.another_interval, 45)

