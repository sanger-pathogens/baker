import enum

from jinja2 import Environment
from pkg_resources import get_distribution, DistributionNotFound

from bakerlib.argument_parsing import ArgumentParserBuilder
from bakerlib.catalog_decorator import CatalogDecorator
from bakerlib.function_decorator import FunctionDecorator
from bakerlib.image_repository import ImageRepository
from bakerlib.missing_image_software_repository import MissingImageSoftwareRepository
from bakerlib.software_decorator import SoftwareDecorator
from bakerlib.software_enrichments import url_enrichments, software_name_version_validation, function_enrichments, \
    image_enrichment
from bakerlib.software_repository import SoftwareRepository
from bakerlib.template_file_loader import TemplateFileLoader
from bakerlib.templating import ScriptTemplateRenderer

_missing = object()


class CachedProperty(object):
    """A decorator that converts a function into a lazy property.  The
    function wrapped is called the first time to retrieve the result
    and then that calculated result is used the next time you access
    the value::

        class Foo(object):

            @CachedProperty
            def foo(self):
                # calculate something important here
                return 42

    The class has to have a `__dict__` in order for this property to
    work.
    """

    # implementation detail: this property is implemented as non-data
    # descriptor.  non-data descriptors are only invoked if there is
    # no entry with the same name in the instance's __dict__.
    # this allows us to completely get rid of the access function call
    # overhead.  If one choses to invoke __get__ by hand the property
    # will still work as expected because the lookup logic is replicated
    # in __get__ for manual invocation.

    def __init__(self, func, name=None, doc=None):
        self.__name__ = name or func.__name__
        self.__module__ = func.__module__
        self.__doc__ = doc or func.__doc__
        self.func = func

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        value = obj.__dict__.get(self.__name__, _missing)
        if value is _missing:
            value = self.func(obj)
            obj.__dict__[self.__name__] = value
        return value


class Action(enum.Enum):
    help = 1
    function_decorate = 2
    software_decorate = 3
    catalog_decorate = 4


class ParameterDI:

    @CachedProperty
    def print_help(self):
        return lambda: self._parameter_parser.print_help()

    @CachedProperty
    def action(self):
        return self._parameters.get("func", Action.help)

    @CachedProperty
    def output_dir(self):
        return self._parameters["output_dir"]

    @CachedProperty
    def output_format(self):
        return self._parameters["output_format"]

    @CachedProperty
    def input_dir(self):
        return self._parameters["input_dir"]

    @CachedProperty
    def images(self):
        return self._parameters["images"]

    @CachedProperty
    def verbose(self):
        return self._parameters["verbose"]

    @CachedProperty
    def template(self):
        return self._parameters["template"]

    @CachedProperty
    def file_mode(self):
        return self._parameters["file_mode"]

    @CachedProperty
    def _parameters(self):
        return dict(vars(self._parameter_parser.parse_args()))

    @CachedProperty
    def _baker_version(self):
        try:
            return get_distribution("baker").version
        except DistributionNotFound:
            return '<Unknown>'

    @CachedProperty
    def _parameter_parser(self):
        return ArgumentParserBuilder.new_instance() \
            .with_decorating('function', Action.function_decorate) \
            .with_decorating('software', Action.software_decorate) \
            .with_decorating('catalog', Action.catalog_decorate) \
            .with_verbose() \
            .build()


class ImageRepositoryDI(ParameterDI):

    @CachedProperty
    def image_repository(self):
        return ImageRepository(self.images)


class SoftwareCatalogDI(ImageRepositoryDI):

    @CachedProperty
    def _missing_software_repository(self):
        return MissingImageSoftwareRepository(self._software_repository, self.image_repository)

    @CachedProperty
    def _software_repository(self):
        return SoftwareRepository(self.input_dir, self._software_enrichments)

    @CachedProperty
    def software_repository(self):
        return self._software_repository if self.images is None else self._missing_software_repository

    @CachedProperty
    def _software_enrichments(self):
        return [url_enrichments, software_name_version_validation, image_enrichment, function_enrichments]


class ScriptTemplateRendererDI(ParameterDI):

    @CachedProperty
    def script_template_renderer(self):
        return ScriptTemplateRenderer(self._jinja_environment, self.template, self.file_mode)

    @CachedProperty
    def _jinja_file_system_loader(self):
        return TemplateFileLoader()

    @CachedProperty
    def _jinja_environment(self):
        return Environment(loader=self._jinja_file_system_loader)


class BakerDI(SoftwareCatalogDI, ScriptTemplateRendererDI):

    @CachedProperty
    def command(self):
        action = self.action
        switcher = {
            Action.help: lambda: self.print_help,
            Action.function_decorate: lambda: self._function_decorator,
            Action.software_decorate: lambda: self._software_decorator,
            Action.catalog_decorate: lambda: self._catalog_decorator,
        }
        return switcher[action]()

    @CachedProperty
    def _function_decorator(self):
        return FunctionDecorator(self.output_format, self.script_template_renderer, self.software_repository)

    @CachedProperty
    def _catalog_decorator(self):
        return CatalogDecorator(self.output_format, self.script_template_renderer, self.software_repository)

    @CachedProperty
    def _software_decorator(self):
        return SoftwareDecorator(self.output_format, self.script_template_renderer, self.software_repository)
