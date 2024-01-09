from cpme_api.api.feature.utils import fancy
from typing import Any, Union, List
import importlib


SWAGGER_TYPE = {
    'string': str,
    'number': (int, float),
    'boolean': bool,
}

PRIMITIVE_TYPES = (float, bool, bytes, int, str)

MODEL_MODULE = importlib.import_module('cpme_api.models')


def str_to_bool(name: str):
    if isinstance(name, bool):
        return None
    if name.lower() == 'true':
        return True
    elif name.lower() == 'false':
        return False
    return None


def eval_obj_structure(obj: dict, swagger_types: Union[str, dict], parent: str = ''):
    """
    Check if object and nested objects contains valid type assignment
    """
    # check reference object
    if isinstance(swagger_types, str):
        swagger_types = get_ref_object(swagger_types)
    if obj is None or obj == 'None':
        return None
    elif isinstance(obj, PRIMITIVE_TYPES):
        if isinstance(swagger_types, dict):
            raise ValueError(f"Invalid value {obj} expected record for {parent} of attributes {swagger_types}! ")
        st = SWAGGER_TYPE.get(swagger_types)
        if st is None:
            # TODO workaround for 'object'
            return None
        if st == bool:
            # check for boolean as string
            n_obj = str_to_bool(obj)
            if n_obj is not None:
                return True
        if not isinstance(obj, st):
            raise TypeError(
                f"Invalid type {type(obj)}[{obj}] of attribute `{parent}` expected type `{st}`")

    elif isinstance(obj, list):
        if swagger_types.startswith('list'):
            cls_name = getattr(MODEL_MODULE, swagger_types.lstrip('list[').rstrip(']'))
            inx = 0
            for sub_obj in obj:
                if cls_name.is_primitive():
                    eval_obj_structure(sub_obj, cls_name._primitive, f'{parent}/[{inx}]')
                else:
                    eval_obj_structure(sub_obj, cls_name.get_swagger_types(), f'{parent}/[{inx}]')
                inx += 1
        else:
            raise TypeError(
                f"Invalid type {type(obj)}[{obj}] of attribute `{parent}` expected type `list`")

    elif isinstance(obj, tuple):
        return tuple(eval_obj_structure(sub_obj)
                     for sub_obj in obj)

    if isinstance(obj, dict):
        for attr, val in obj.items():
            if not hasattr(swagger_types, "keys"):
                cls_name = getattr(MODEL_MODULE, swagger_types, None)
                if cls_name is None:
                    raise TypeError(f"Invalid value {val} with type {type(val)}. Expected type <XXX>")
                swagger_types = cls_name.get_swagger_types()
            if attr in swagger_types.keys():
                eval_obj_structure(val, swagger_types[attr], f'{parent}/{attr}')
            else:
                raise ValueError(f"Invalid attribute {attr} = {val} in {parent} expected {list(swagger_types.keys())}")


def check_swagger_type(s_type:str, val_obj: Any):
    """
    Check data type validation without nesting
    """
    if d_type := SWAGGER_TYPE.get(s_type):
        # primitive types
        return isinstance(val_obj, d_type)
    elif 'list' in s_type:
        # List object
        return isinstance(val_obj, list)
    else:
        # object
        cls_name = getattr(MODEL_MODULE, s_type)
        if hasattr(cls_name, 'is_array'):
            if cls_name.is_array:
                return check_swagger_type(cls_name.get_reference(), val_obj)
            else:
                raise TypeError(f"Missing reference in array class {cls_name.__name__}. Can not check {val_obj}")
        if hasattr(cls_name, '_primitive'):
            return check_swagger_type(cls_name._primitive, val_obj)
        else:
            return isinstance(val_obj, cls_name)


def check_list_type(cls_name, list_obj):
    for item in list_obj:
        res = isinstance(item, getattr(MODEL_MODULE, cls_name))
        if not res:
            return False
        if isinstance(item, BaseContent):
            item._check_type(item, cls_name)


def get_ref_object(cls_name:str):
    cls_ref = getattr(MODEL_MODULE, cls_name, None)
    if cls_ref is None:
        return cls_name
    if ref := cls_ref.get_reference():
        return ref
    return cls_name


class BaseContent(object):

    _check_data_flag = True

    _swagger_types = {}

    _default_values = {}

    _primary_keys = ()

    _required = []

    _object = ()

    _primitive = False

    _enum = []

    def __new__(cls, *args, **kwargs):
        if ref := cls._swagger_types.get('ref'):
            if ref.startswith('list'):
                class_name = getattr(MODEL_MODULE, ref.lstrip('list[').rstrip(']'))
                obj = class_name.__call__()
                return [obj]
            else:
                ValueError('reference object is not list!')
        return object.__new__(cls)
        # return super(cls).__new__(cls, *args, **kwargs)

    def __init__(self, **kwargs):
        self._check_reference()
        self._check_required()
        self._check_attribute(**kwargs)

    # def get_properties(self) -> List[str]:
    #    return [x.lstrip('_') for x in self.__dict__.keys()]

    @classmethod
    def get_required(cls):
        return cls._required

    @classmethod
    def get_properties(cls) -> List[str]:
        return list(cls._default_values.keys())

    @classmethod
    def get_enum(cls):
        return cls._enum

    @classmethod
    def is_primitive(cls, s_type: str = ''):
        if value := cls._primitive:
            if s_type and (value != s_type):
                return False
            return True
        return False

    @classmethod
    def is_array(cls):
        if cls._swagger_types.get('ref'):
            return True
        return False

    @classmethod
    def get_swagger_types(cls):
        if not cls._swagger_types and cls._object:
            return cls._object[0]
        return cls._swagger_types

    @classmethod
    def get_reference(cls):
        return cls._swagger_types.get('ref')

    def _check_reference(self):
        ref = self.__class__._swagger_types.pop('ref', ())
        if not ref:
            return
        print(ref)
        if ref.startswith('list'):
            # for list object reference to a data class
            cls_name = getattr(MODEL_MODULE, ref.lstrip('list[').rstrip(']'))
            obj = cls_name.__call__()
            obj.init_tree()
            self.__class__._object = (ref, [obj])

    def init_tree(self):
        """
        Method create full structure of nested objects with empty
        attributes.
        """
        for attr, s_type in self.__class__._swagger_types.items():
            # check reference object
            s_type = get_ref_object(s_type)
            if s_type in ['number', 'string', 'boolean']:
                continue
            elif s_type.startswith('list'):
                # list objects
                cls_name = getattr(MODEL_MODULE, s_type.lstrip('list[').rstrip(']'))
                obj = cls_name.__call__()
                obj = [obj]
                obj[0].init_tree()
            else:
                # dict object
                cls_name = getattr(MODEL_MODULE, s_type)
                if cls_name.is_primitive():
                    continue
                obj = cls_name.__call__()
                obj.init_tree()
            setattr(self, '_' + attr, obj)

    def _check_required(self):
        if not hasattr(self.__class__, 'required'):
            return
        if not self._check_data_flag:
            return
        ret = list(filter(lambda x: self.__dict__['_' + x] is None, self._required))
        if ret:
            raise ValueError(f"Invalid value for {','.join(ret)}, must not be `None`")

    def _check_attribute(self, **kwargs):
        for param, val in kwargs.items():
            if self._check_data_flag:
                if '_' + param not in self.__dict__.keys():
                    raise ValueError(f"Invalid attribute `{param}` = `{val}` for {self.__class__.__name__}")
                self._check_type(param, val)

            if val == '':
                val = None
            setattr(self, '_' + param, val)

    def _check_type(self, param: str, value: Any) -> None:
        if not self._check_data_flag:
            return
        s_type = self._swagger_types.get(param)
        if s_type is None:
            raise ValueError(f"Invalid attribute `{param}` = `{value}`. Defined = {list((self._default_values.keys()))}")
        if not check_swagger_type(s_type, value):
            raise TypeError(f"Invalid type {type(value)}[{value}] of attribute `{param}` expected type `{s_type}` in {self.__class__.__name__} entity")

    def _assign(self, attribute: str, value: Any):
        self._check_type(attribute, value)
        setattr(self, '_' + attribute, value)

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, self.__class__):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

    def to_dict(self, mock=False, data_validation=None) -> Union[dict, list]:
        """filter data model content into the simple dict. Ignore all None value parameters.
        The optional parameter check_body check data structure according to the YAML definition"""
        assert isinstance(mock, bool), "f mock parameter must be bool type!"
        assert (isinstance(mock, bool) or data_validation is None), "f data_validation parameter must be bool type!"
        check_flag = BaseContent._check_data_flag
        if data_validation is not None:
            check_flag = data_validation

        if self.__class__._object:
            # for list object reference to a data class
            obj_list = self.__class__._object[1]
            return list(map(lambda x: x.to_dict(mock, data_validation), obj_list))

        new_data = {}
        prop = {x.lstrip('_'): y for x, y in self.__dict__.items()}
        for key, val in prop.items():
            if val is None and mock is False:
                continue
            if isinstance(val, BaseContent):
                res = val.to_dict(mock, False)
                if res:
                    new_data[key] = res
            elif isinstance(val, list):
                for item in val:
                    if not hasattr(item, 'to_dict'):
                        if key not in new_data:
                            new_data[key] = list()
                        new_data[key].append(item)
                        continue
                    else:
                        res = item.to_dict(mock, False)
                    if res:
                        if key in new_data:
                            new_data[key].append(res)
                        elif isinstance(res, list):
                            # for list object reference to a data class
                            new_data[key] = res
                        else:
                            new_data[key] = [res]
            else:
                if mock:
                    default = self._default_values.get(key, val)
                    if default == 'object':
                        new_data[key] = self._get_instance_of_type(key)
                        continue
                    new_data[key] = self._default_values.get(key, val)
                else:
                    if data_validation:
                        self._check_type(key, val)
                    new_data[key] = val
        if check_flag:
            eval_obj_structure(new_data, self._swagger_types, parent=self.__class__.__name__)
        return new_data

    def _get_instance_of_type(self, attr: str):
        s_type = self._swagger_types.get(attr)
        if 'list' in s_type:
            return []
        else:
            return {}

    def fancy(self, mock=False, line_text=''):
        """User friendly printout representation of dict structure"""
        assert isinstance(mock, bool), "Invalid parameter. Must be [False or True]"
        fancy(self.to_dict(mock), line_text)

    def to_str(self):
        return str(self.to_dict(data_validation=False))

    def __repr__(self):
        return self.to_str()


def set_data_validation(state=False):
    """Enable or Disable all explicitly defined data structures"""
    BaseContent._check_data_flag = state
