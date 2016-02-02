***
# Cfg Parser - Configuration parser class.
***

Parsing config files with predetermined structure and generating default one if no config file found.

Structure is as follows:
    * All sections are lowercase without whitespaces
    * All fields are camel case and leading character represent type field contains

Available types are:
    * i - integer, i.e. iInterval=30
    * f - float, i.e. fPrice=45.67
    * b - boolean, i.e. bEnableSpoofing=1
    * s - string, i.e. sEntryPointClass=MainMethanina
    * l - list, i.e. lProxyList=127.0.0.1:3456,127.0.0.1:2333,127.0.0.1:4565

## Installation

### Requirements

* python 2.7.x
* easy_install

### Installation and configuration

Build simple daemon egg file:

```bash
    $ python ./setup.py bdist_egg
```

Install Simple Daemon package that you build by easy_install:

```bash
    $ easy_install /path/to/dist/CfgParser-1.0.0-py2.7.egg
```

## Example

```python

    import os
    from cfg_parser import Configuration
    
    ROOT = os.path.dirname(os.path.realpath(__file__))

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
```
