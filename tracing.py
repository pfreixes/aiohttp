__all__ = ('TraceRequest',)

class TraceRequest:
    """First-class used to trace requests"""

    signals = (
        'on_request_start', 
        'on_request_end',
        'on_request_exception',
        'on_request_redirect',
        'on_connection_queued_start',
        'on_connection_queued_end',
        'on_connection_create_start',
        'on_connection_create_end',
        'on_connection_reuseconn',
        'on_dns_resolvehost_start',
        'on_dns_resolvehost_end',
        'on_dns_cache_hit',
        'on_dns_cache_miss'
    )

    def __init__(self, trace_context_class=SimpleNamespace):
        for signal in TraceRequest.signals:
            setattr(self, signal) = Signal()

        self._trace_context_class = trace_context_class

    def trace_context(self):
        """ Return a new trace_context instance """
        return self._trace_context_class()

    def freeze(self):
        for signal in TraceRequest.signals:
            getattr(self, signal).freeze()


class Trace:

    def __init__(self, trace_request, session, trace_context):
        self._trace_request = trace_request
        self._session = session
        self._trace_context = trace_context

    async def send(self, signal, *args, **kwargs):
        return await getattr(self._trace_request, signal)(
            self._session,
            self._trace_context,
            *args,
            **kwargs
        )
