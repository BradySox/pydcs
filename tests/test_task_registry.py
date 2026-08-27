import inspect

import dcs.task


def test_every_wrapped_action_is_readable() -> None:
    """Every WrappedAction that can be written must also be readable.

    `wrappedactions` is the lookup `_create_from_dict` uses to turn a task id
    back into a class. A class missing from it can be serialized into a .miz
    that then raises KeyError on load, so the file is write-only.

    ActivateACLS/DeactivateACLS/DeactivateLink4 were in exactly that state from
    2022 until this test was added: the classes shipped, the registry entries
    did not, and any mission using them could not be re-opened.
    """
    unreadable = []
    for name, obj in vars(dcs.task).items():
        if not inspect.isclass(obj):
            continue
        if not issubclass(obj, dcs.task.WrappedAction):
            continue
        if obj is dcs.task.WrappedAction:
            continue
        key = getattr(obj, "Key", None)
        if key is None:
            continue
        if dcs.task.wrappedactions.get(key) is not obj:
            unreadable.append((name, key))

    assert not unreadable, "WrappedAction classes missing from wrappedactions: %s" % (
        ", ".join("%s (Key=%r)" % (n, k) for n, k in sorted(unreadable))
    )
