# -*- coding: utf-8 -*-


class TreeElement(object):
    def __repr__(self):
        return u'{}'.format(self.__class__.__name__)


class UndefinedToken(KeyError):
    """Raised if a given context does not contain a particular Token."""


class Token(TreeElement):
    def __init__(self, value):
        if isinstance(value, TreeElement):
            raise TypeError
        self._value = value

    def __repr__(self):
        return u'{}({})'.format(self.__class__.__name__, self._value)

    def __gt__(self, other):
        if not isinstance(other, self.__class__):
            return hash(self) > hash(other)
        return self._value > other._value

    def __ge__(self, other):
        if not isinstance(other, self.__class__):
            return hash(self) >= hash(other)
        return self._value >= other._value

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self._value == other._value

    def __hash__(self):
        return hash((self.__class__.__name__, self._value))

    def tokens(self):
        yield self._value

    def __call__(self, context):
        if self._value not in context:
            msg = u'Token "{}" is not defined in context {}'
            raise UndefinedToken(msg.format(self._value, context))
        return context[self._value]


class Not(TreeElement):
    def __init__(self, child):
        if not isinstance(child, TreeElement):
            raise TypeError
        self._child = child

    def __repr__(self):
        return u'{}({})'.format(self.__class__.__name__, self._child)

    def __gt__(self, other):
        if not isinstance(other, self.__class__):
            return hash(self) > hash(other)
        return self._child > other._child

    def __ge__(self, other):
        if not isinstance(other, self.__class__):
            return hash(self) >= hash(other)
        return self._child >= other._child

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self._child == other._child

    def __hash__(self):
        return hash((self.__class__.__name__, self._child))

    def tokens(self):
        for token in self._child.tokens():
            yield token

    def __call__(self, context):
        return not self._child(context)


class GroupMixin(object):
    def __init__(self, a, b, *others):
        children = (a, b) + others

        for child in children:
            if not isinstance(child, TreeElement):
                raise TypeError
        self._children = tuple(sorted(children))

    def __repr__(self):
        return u'{}({})'.format(
            self.__class__.__name__,
            u', '.join(repr(child) for child in self._children)
        )

    def __gt__(self, other):
        if not isinstance(other, self.__class__):
            return hash(self) > hash(other)
        return self._children > other._children

    def __ge__(self, other):
        if not isinstance(other, self.__class__):
            return hash(self) >= hash(other)
        return self._children >= other._children

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self._children == other._children

    def __hash__(self):
        return hash(tuple([self.__class__.__name__]) + self._children)

    def tokens(self):
        for child in self._children:
            for token in child.tokens():
                yield token


class And(GroupMixin, TreeElement):
    def __call__(self, context):
        return all(child(context) for child in self._children)


class Or(GroupMixin, TreeElement):
    def __call__(self, context):
        return any(child(context) for child in self._children)
