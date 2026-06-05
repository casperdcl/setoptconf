try:
    from tomllib import loads
except ModuleNotFoundError:
    from toml import loads

from .filebased import FileBasedSource

__all__ = ('TomlFileSource',)


class TomlFileSource(FileBasedSource):
    def __init__(self, *args, **kwargs):
        self.section = kwargs.pop('section', None)
        super(TomlFileSource, self).__init__(*args, **kwargs)

    def get_settings_from_file(self, file_path, settings, manager=None):
        section = self.section or manager.name.lower()

        with open(file_path, 'r') as f:
            content = loads(f.read())

        if section:
            for part in section.split('.'):
                if part in content:
                    content = content[part]
                else:
                    return None

        for setting in settings:
            if setting.name in content:
                setting.value = content[setting.name]

        return settings
