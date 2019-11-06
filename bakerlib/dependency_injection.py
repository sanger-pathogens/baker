import enum

from jinja2 import FileSystemLoader, Environment
from pkg_resources import get_distribution, DistributionNotFound

from bakerlib.argument_parsing import ArgumentParserBuilder
from bakerlib.docker_config import DockerConfig
from bakerlib.function_decorator import FunctionDecorator
from bakerlib.image_comparator import ImageComparator
from bakerlib.image_reconciler import ImageReconciler
from bakerlib.image_repository import ImageRepository
from bakerlib.singularity_build import SingularityBaker, SingularityExecutor
from bakerlib.singularity_build_legacy import SingularityLegacyBaker
from bakerlib.software_enrichments import url_enrichments, software_name_version_validation, function_enrichments, \
    image_enrichment
from bakerlib.software_repository import SoftwareRepository
from bakerlib.specified_image_builder import SpecifiedImageBuilder
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
    help = 2
    decorate = 3
    singularity_check = 4
    singularity_bake = 5
    singularity_legacy_bake = 6


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
    def input_dir(self):
        return self._parameters["input_dir"]

    @CachedProperty
    def missing(self):
        return self._parameters["missing"]

    @CachedProperty
    def template_dir(self):
        return self._parameters["template_dir"]

    @CachedProperty
    def images(self):
        return self._parameters["images"]

    @CachedProperty
    def config(self):
        return self._parameters["config"]

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
            .with_decorating(Action.decorate) \
            .with_version(lambda: self._baker_version) \
            .with_singularity_check(Action.singularity_check) \
            .with_singularity_bake(Action.singularity_bake) \
            .with_legacy_bake(Action.singularity_legacy_bake) \
            .with_verbose() \
            .build()


class SoftwareCatalogDI(ParameterDI):

    @CachedProperty
    def software_repository(self):
        return SoftwareRepository(self.input_dir, self._software_enrichments)

    @CachedProperty
    def _software_enrichments(self):
        return [url_enrichments, software_name_version_validation, image_enrichment, function_enrichments]


class SingularityBakerDI(SoftwareCatalogDI):

    @CachedProperty
    def singularity_baker(self):
        return SingularityBaker(self.output_dir, self._docker_config, self.software_repository,
                                self._singularity_executor)

    @CachedProperty
    def _docker_config(self):
        return DockerConfig(self.config)

    @CachedProperty
    def _singularity_executor(self):
        return SingularityExecutor()


class ImageRepositoryDI(ParameterDI):

    @CachedProperty
    def image_repository(self):
        return ImageRepository(self.output_dir)


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


class BakerDI(SingularityBakerDI, ImageRepositoryDI, ScriptTemplateRendererDI):

    @CachedProperty
    def command(self):
        action = self.action
        switcher = {
            Action.help: lambda: self.print_help,
            Action.decorate: lambda: self._decorator,
            Action.singularity_bake: lambda:
            self._singularity_missing_image_baker if self.missing else self._singularity_specified_image_baker,
            Action.singularity_check: lambda: self._singularity_checker,
            Action.singularity_legacy_bake: lambda: self._legacy_singularity_baker
        }
        return switcher[action]()

    @CachedProperty
    def _legacy_singularity_baker(self):
        return SingularityLegacyBaker(self.output_dir, self.template_dir, self.software_repository, self.images)

    @CachedProperty
    def _singularity_checker(self):
        return ImageReconciler(self.software_repository, self.image_repository,
                               ImageComparator(lambda s: print("missing %s" % s),
                                               lambda s: print("unknown %s" % s)))

    @CachedProperty
    def _singularity_missing_image_baker(self):
        return ImageReconciler(self.software_repository, self.image_repository,
                               ImageComparator(lambda s: self.singularity_baker.bake(s), lambda s: None))

    @CachedProperty
    def _singularity_specified_image_baker(self):
        return SpecifiedImageBuilder(self.images, self.singularity_baker)

    @CachedProperty
    def _decorator(self):
        return FunctionDecorator(self.output_dir, self.script_template_renderer, self.software_repository)
