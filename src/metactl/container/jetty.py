import metactl
from metactl.container.java import java_section

def find_jetty():
    return '/usr/share/jetty'

def jetty_home(section):
    if 'jetty.home' not in section:
        section['jetty.home'] = find_jetty()
    if 'java.jar' not in section:
        section['java.jar'] = '${jetty.home}/start.jar'

def jetty_properties(section):
    if 'jetty.properties' not in section:
        properties = {}
        for key in ['jetty.port','jetty.home']:
            if key in section:
                properties[key] = '${' + key + '}'
        propargs = ['-D' + k + '=' + v for k, v in properties.iteritems()]
        if propargs:
            section['jetty.properties'] = ' '.join(propargs)
    if 'jetty.properties' in section:
        section['java.properties'] = '${jetty.properties}'

def jetty_arguments(section):
    if 'jetty.ini' not in section:
        section['jetty.ini'] = '/dev/null'
    if 'jetty.lib' not in section:
        section['jetty.lib'] = '${jetty.home}/lib'
    if 'jetty.xml' not in section:
        section['jetty.xml'] = 'etc/jetty.xml'
    if 'jetty.arguments' not in section:
        arguments = '--ini=${jetty.ini} lib=${jetty.lib}'
        if 'jetty.options' in section:
            arguments += ' OPTIONS=${jetty.options}'
        if 'jetty.xml' in section:
            arguments += ' ${jetty.xml}'
        section['jetty.arguments'] = arguments
    section['java.arguments'] = '${jetty.arguments}'

def jetty_section(section):
    jetty_home(section)
    jetty_properties(section)
    jetty_arguments(section)

def jetty_config(config):
    for section in config.sections():
        if section.startswith('daemon.'):
            if config[section].get('container','none') == 'jetty':
                jetty_section(config[section])
                java_section(config[section])

metactl.processors.append(jetty_config)
