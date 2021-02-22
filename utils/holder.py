class AttributeHolder(object):
    def __repr__(self):
        type_name = type(self).__name__
        arg_strings = []
        star_args = {}
        for name, value in sorted(self.__dict__.items()):
            if name.isidentifier():
                arg_strings.append('%s=%r' % (name, value))
            else:
                star_args[name] = value
        if star_args:
            arg_strings.append('**%s' % repr(star_args))
        return '%s(%s)' % (type_name, ', '.join(arg_strings))
