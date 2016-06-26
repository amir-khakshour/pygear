from __future__ import absolute_import
import signal
from pydispatch import dispatcher

from zope.interface import implementer
from zope.interface import Interface

from twisted.internet import reactor
from twisted.application import service
from twisted.python.failure import Failure
from twisted.internet.defer import maybeDeferred, DeferredList, Deferred

from pygear.logging import log
from pydispatch.robustapply import robustApply
from pydispatch.dispatcher import (
    Any, Anonymous, liveReceivers, getAllReceivers, disconnect
)

from .interfaces import ISignalManager


signal_names = {}

for signame in dir(signal):
    if signame.startswith("SIG"):
        signum = getattr(signal, signame)
        if isinstance(signum, int):
            signal_names[signum] = signame


def send_catch_log(signal=Any, sender=Anonymous, *arguments, **named):
    """Like pydispatcher.robust.sendRobust but it also logs errors and returns
    Failures instead of exceptions.
    """
    dont_log = named.pop('dont_log', None)
    responses = []
    for receiver in liveReceivers(getAllReceivers(sender, signal)):
        try:
            response = robustApply(receiver, signal=signal, sender=sender,
                                   *arguments, **named)
            if isinstance(response, Deferred):
                log.msg(format="Cannot return deferreds from signal handler: %(receiver)s",
                        level=log.ERROR, receiver=receiver)
        except dont_log:
            result = Failure()
        except Exception:
            result = Failure()
            log.err(result, "Error caught on signal handler: %s" % receiver)
        else:
            result = response
        responses.append((receiver, result))
    return responses


def send_catch_log_deferred(signal=Any, sender=Anonymous, *arguments, **named):
    """Like send_catch_log but supports returning deferreds on signal handlers.
    Returns a deferred that gets fired once all signal handlers deferreds were
    fired.
    """

    def logerror(failure, recv):
        if dont_log is None or not isinstance(failure.value, dont_log):
            log.err(failure, "Error caught on signal handler: %s" % recv)
        return failure

    dont_log = named.pop('dont_log', None)
    dfds = []
    for receiver in liveReceivers(getAllReceivers(sender, signal)):
        d = maybeDeferred(robustApply, receiver, signal=signal, sender=sender,
                          *arguments, **named)
        d.addErrback(logerror, receiver)
        d.addBoth(lambda result: (receiver, result))
        dfds.append(d)
    d = DeferredList(dfds)
    d.addCallback(lambda out: [x[1] for x in out])
    return d


def disconnect_all(signal=Any, sender=Any):
    """Disconnect all signal handlers. Useful for cleaning up after running
    tests
    """
    for receiver in liveReceivers(getAllReceivers(sender, signal)):
        disconnect(receiver, signal=signal, sender=sender)


def get_signal_manager(app):
    return app.getComponent(ISignalManager)


def install_shutdown_handlers(function, override_sigint=True):
    """Install the given function as a signal handler for all common shutdown
    signals (such as SIGINT, SIGTERM, etc). If override_sigint is ``False`` the
    SIGINT handler won't be install if there is already a handler in place
    (e.g.  Pdb)
    """
    reactor._handleSignals()
    signal.signal(signal.SIGTERM, function)
    if signal.getsignal(signal.SIGINT) == signal.default_int_handler or \
            override_sigint:
        signal.signal(signal.SIGINT, function)
    # Catch Ctrl-Break in windows
    if hasattr(signal, "SIGBREAK"):
        signal.signal(signal.SIGBREAK, function)


@implementer(ISignalManager)
class SignalManager(service.Service):
    name = 'signal_manager'

    def __init__(self, sender=dispatcher.Anonymous):
        self.sender = sender

    def startService(self):
        log.msg("Starting signal manager...")

    def connect(self, *a, **kw):
        kw.setdefault('sender', self.sender)
        return dispatcher.connect(*a, **kw)

    def disconnect(self, *a, **kw):
        kw.setdefault('sender', self.sender)
        return dispatcher.disconnect(*a, **kw)

    def send_catch_log(self, *a, **kw):
        kw.setdefault('sender', self.sender)
        return send_catch_log(*a, **kw)

    def send_catch_log_deferred(self, *a, **kw):
        kw.setdefault('sender', self.sender)
        return send_catch_log_deferred(*a, **kw)

    def disconnect_all(self, *a, **kw):
        kw.setdefault('sender', self.sender)
        return disconnect_all(*a, **kw)

