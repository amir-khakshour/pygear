import os
import glob
from os.path import expanduser
from pygear.core.six import StringIO
from pygear.text.encoding import force_text
from pygear.core.six.moves.configparser import ConfigParser, NoSectionError, NoOptionError


def closest_cfg(name, path='.', prevpath=None):
    if path == prevpath:
        return ''
    path = os.path.abspath(path)
    cfgfile = os.path.join(path, name)
    if os.path.exists(cfgfile):
        return cfgfile
    return closest_cfg(name, os.path.dirname(path), path)


class BaseConfig(object):
    """A ConfigParser wrapper to support defaults when calling instance
    Methods, and also tied to a single section"""

    SECTION = 'default'

    def __init__(self, values=None, extra_sources=()):
        if values is None:
            self.cp = ConfigParser()
            try:
                default_config = self.get_default_config()
                if default_config:
                    self.cp.readfp(StringIO(force_text(default_config)))
            except NotImplementedError:
                pass
            try:
                sources = self.get_sources()
                self.cp.read(sources)
            except NotImplementedError:
                pass
            self.cp.read(sources)
            for fp in extra_sources:
                self.cp.readfp(fp)
        else:
            self.cp = ConfigParser(values)
            self.cp.add_section(self.SECTION)

    def get_sources(self):
        raise NotImplementedError

    def get_default_config(self):
        raise NotImplementedError

    def _getany(self, method, option, default, section):
        if not section:
            section = self.SECTION
        try:
            return method(section, option)
        except (NoSectionError, NoOptionError):
            if default is not None:
                return default
            raise

    def get(self, option, default=None, section=None):
        return self._getany(self.cp.get, option, default, section)

    def getint(self, option, default=None, section=None):
        return self._getany(self.cp.getint, option, default, section)

    def getfloat(self, option, default=None, section=None):
        return self._getany(self.cp.getfloat, option, default, section)

    def getboolean(self, option, default=None, section=None):
        return self._getany(self.cp.getboolean, option, default, section)

    def getlist(self, option, default=None, section=None):
        val = self._getany(self.cp.get, option, default, section)
        return val.split(',')

    def getdict(self, option, default=None, section=None):
        val = self._getany(self.cp.get, option, default, section)
        val = val[1:-1]
        val_dict = dict(tuple(item.split('=')) for item in val.split(';'))
        for i, j in val_dict.items():
            val_dict[i] = eval(j, {"__builtins__": None}, {"list": list, "str": str, "int": int})
        return val_dict

    def items(self, section, default=None):
        try:
            return self.cp.items(section)
        except (NoSectionError, NoOptionError):
            if default is not None:
                return default
            raise


class Config(BaseConfig):
    """A ConfigParser wrapper to support defaults when calling instance
    methods, and also tied to a single section"""

    SECTION = 'pygear'

    def get_sources(self):
        sources = [
            '/etc/{section}/{section}.conf'.format(section=self.SECTION),
            r'c:\{section}\{section}.conf'.format(section=self.SECTION)
        ]
        sources += sorted(glob.glob('/etc/{section}/conf.d/*'.format(section=self.SECTION)))
        sources += ['{section}.conf'.format(section=self.SECTION)]
        sources += [expanduser('~/.{section}.conf'.format(section=self.SECTION))]
        near_cfg = closest_cfg('{section}.conf'.format(section=self.SECTION))
        if near_cfg:
            sources.append(near_cfg)

        return sources

