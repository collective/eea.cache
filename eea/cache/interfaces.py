""" Cache public interface
"""
import six
from zope import interface
from zope import schema
from eea.cache.subtypes.interfaces import ICacheAware
from eea.cache.browser.interfaces import ILayer
from eea.cache.browser.interfaces import VARNISH

servers_value = schema.TextLine()
servers_value._type = (six.text_type, str)

class IMemcachedClient(interface.Interface):
    """A memcache client utility
    """

    defaultNS = schema.TextLine(
        title=u'Default Namespace',
        description=u"The default namespace used by this client",
        required=False,
        default=None)

    servers = schema.List(
        title=u'Servers',
        description=u"Servers defined as <hostname>:<port>",
        value_type=servers_value,
        required=True,
        default=['127.0.0.1:11211']
        )

    defaultLifetime = schema.Int(
        title=u'Default Lifetime',
        description=u'The default lifetime of entries',
        required=True,
        default=3600,
        )

    trackKeys = schema.Bool(
        title=u'Track Keys',
        description=u'Enable the keys method',
        required=False,
        default=False,
        )

    def getStatistics():
        """ Returns the memcached stats
        """

    def set(data, key, lifetime=None, ns=None, raw=False, dependencies=None):
        """
        Sets data with the given key in namespace. Lifetime
        defaults to defautlLifetime and ns defaults to the
        default namespace.

        The dependencies argument can be used to invalidate on
        specific dependency markers.

        This method returns the key that is generated by the utility.

        If raw is True, the key is taken as is, and is not modified by
        the utility, the key and the namespace need to be strings in
        this case, otherwise a ValueError is raised.
        """

    def query(key, default=None, ns=None, raw=False):
        """
        Query the cache for key in namespace, returns default if
        not found. ns defaults to default namespace.
        """

    def invalidate(key=None, ns=None, raw=False, dependencies=None):
        """
        Invalidates key in namespace which defaults to default
        namespace, currently we can not invalidate just a namespace.

        If dependencies are provided all, entries with such
        dependencies are invalidated.
        """

    def invalidateAll():
        """
        Invalidates all data of the memcached servers, not that all
        namespaces are invalidated
        """

    def keys(ns=None):
        """
        If trackKeys is True, returns the keys defined in the
        namespace
        """

class IInvalidateEvent(interface.Interface):
    """ Abstract cache invalidation interface
    """

#
# Memcache
#
class IInvalidateMemCacheEvent(IInvalidateEvent):
    """An event which invalidates memcache entries."""

    cacheName = schema.TextLine(
        title=u'cacheName',
        description=u"""
            Invalidate in the cache with this name.
            If no name is given all caches are invalidated.
            """,
        required=False,
    )

    key = schema.TextLine(
        title=u'key',
        required=False,
    )

    ns = schema.TextLine(
        title=u'namespace',
        required=False,
    )

    raw = schema.Bool(
        title=u'raw',
        required=False,
        default=False,
    )

    dependencies = schema.List(
        title=u'Dependencies',
        required=False,
    )

# BBB
IInvalidateCacheEvent = IInvalidateMemCacheEvent

#
# Varnish
#
class IInvalidateVarnishEvent(IInvalidateEvent):
    """ An event which invalidates varnish entries
    """

#
# All caching invalidation event
#
class IInvalidateEverythingEvent(IInvalidateEvent):
    """ Invalidate both varnish and memcache entries
    """


__all__ = [
    ICacheAware.__name__,
    ILayer.__name__,
    IMemcachedClient.__name__,
    IInvalidateEvent.__name__,
    IInvalidateMemCacheEvent.__name__,
    IInvalidateVarnishEvent.__name__,
    IInvalidateEverythingEvent.__name__,
    VARNISH.__name__,
]
