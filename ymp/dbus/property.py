from abc import ABCMeta, abstractclassmethod
from collections.abc import Hashable
from enum import Enum
import dbus.service


def PropertyInterface(*INTERFACE_NAMES):
    class _PropertyInterface(dbus.service.Object):
        @dbus.service.method(
            dbus.PROPERTIES_IFACE,
            in_signature='ss', out_signature='v'
        )
        def Get(self, interface_name, property_name):
            properties = self.GetAll(interface_name)
            if property_name in properties:
                return properties[property_name]

            raise dbus.exceptions.DBusException(
                'The "{}" object does not have a property "{}"'
                .format(self.__class__.__name__, property_name)
            )

        @dbus.service.method(
            dbus.PROPERTIES_IFACE,
            in_signature='s', out_signature='a{sv}'
        )
        def GetAll(self, interface_name):
            if interface_name in INTERFACE_NAMES:
                return self.get_all_properties(interface_name)

            raise dbus.exceptions.DBusException(
                'The "{}" object does not implement the "{}" interface'
                .format(self.__class__.__name__, interface_name)
            )

        @dbus.service.method(dbus.PROPERTIES_IFACE, in_signature='ssv')
        def Set(self, interface_name, property_name, new_value):
            self.PropertiesChanged(
                interface_name, {property_name: new_value}, []
            )

        @dbus.service.signal(dbus.PROPERTIES_IFACE, signature='sa{sv}as')
        def PropertiesChanged(self, interface_name,
                              changed_properties, invalidated_properties):
            if interface_name not in INTERFACE_NAMES:
                self.properties_changed(
                    interface_name, changed_properties, invalidated_properties
                )

            raise dbus.exceptions.DBusException(
                'The "{}" object does not implement the "{}" interface'
                .format(self.__class__.__name__, interface_name)
            )

        @abstractclassmethod
        def get_all_properties(self, interface_name):
            raise NotImplementedError()

        @abstractclassmethod
        def properties_changed(self, interface_name, changed_properties, invalidated_properties):
            raise NotImplementedError()

    return _PropertyInterface


class PropertyType(Enum):
    read_only = 0b01
    write_only = 0b10
    read_write = 0b11


class PropertyList(object):
    def __init__(self):
        self.properties = set()

    def add_property(self, name, value, ptype):
        if name in self.properties:
            raise ValueError('Property "{}" already exists'.format(name))

        self.properties.add(Property(name, value, ptype))

    def set_property(self, name, value):
        if name not in self.properties:
            raise KeyError('Property "{}" does not exist'.format(name))

        self.properties.get(name).set(value)

    def get_property(self, name, value):
        if name not in self.properties:
            raise KeyError('Property "{}" does not exist'.format(name))

        return self.properties.get(name).get()

    def get_all_properties(self):
        ret = dict()
        for p in self.properties:
            if p.can_read:
                ret[p.name] = p.get()

        return ret

    def properties_changed(self, changed_properties, invalidated_properties):
        for name, value in changed_properties.items():
            self.set_property(name, value)

        for name in invalidated_properties:
            if name not in self.properties:
                raise KeyError('Property "{}" does not exist'.format(name))
            self.properties.get(name).valid = False


class Property(Hashable):
    def __init__(self, name, value, ptype):
        self._name = name
        self.value = value
        self._ptype = ptype
        self.valid = True

    def set(self, value):
        if self._ptype == PropertyType.read_only:
            raise ValueError(
                'Property "{}" cannot be written'.format(self._name)
            )

        self.value = value
        self.valid = True

    def get(self):
        if self._ptype == PropertyType.write_only:
            raise ValueError(
                'Property "{}" cannnot be read'.format(self._name)
            )

        if not self.valid:
            raise ValueError('Property "{}" is invalid'.format(self._name))

        return self.value

    @property
    def name(self):
        return self._name

    @property
    def ptype(self):
        return self._ptype

    @property
    def can_read(self):
        return self._ptype in \
            (PropertyType.read_only, PropertyType.read_write)

    @property
    def can_write(self):
        return self._ptype in \
            (PropertyType.write_only, PropertyType.read_write)

    def __hash__(self):
        return hash(self._name)

    def __eq__(self, other):
        return isinstance(other, Property) and other.name == self._name
