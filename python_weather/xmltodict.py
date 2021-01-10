"""
WHO TF NEEDS XMLTODICT WHEN YOU HAVE THE FILE ITSELF
(file from the official repo of xml2dict python pypi package)
removed some functions to make it more "lightweight" i guess?
"""

from xml.parsers import expat
from xml.sax.saxutils import XMLGenerator
from xml.sax.xmlreader import AttributesImpl
from collections import OrderedDict
from inspect import isgenerator
from io import StringIO
_basestring = str
_unicode = str

class _DictSAXHandler(object):
    def __init__(self,
                 item_callback=lambda *args: True,
                 attr_prefix='@',
                 cdata_key='#text',
                 force_cdata=False,
                 cdata_separator='',
                 postprocessor=None,
                 dict_constructor=OrderedDict,
                 strip_whitespace=True,
                 namespace_separator=':',
                 namespaces=None,
                 comment_key='#comment'):
        self.path = []
        self.stack = []
        self.data = []
        self.item = None
        self.item_callback = lambda *a: True
        self.attr_prefix = attr_prefix
        self.cdata_key = cdata_key
        self.force_cdata = force_cdata
        self.cdata_separator = cdata_separator
        self.postprocessor = postprocessor
        self.dict_constructor = dict_constructor
        self.strip_whitespace = strip_whitespace
        self.namespace_separator = namespace_separator
        self.namespaces = namespaces
        self.namespace_declarations = OrderedDict()
        self.comment_key = comment_key

    def _build_name(self, full_name):
        if not self.namespaces:
            return full_name
        i = full_name.rfind(self.namespace_separator)
        if i == -1:
            return full_name
        namespace, name = full_name[:i], full_name[i+1:]
        try:
            short_namespace = self.namespaces[namespace]
        except KeyError:
            short_namespace = namespace
        if not short_namespace:
            return name
        else:
            return self.namespace_separator.join((short_namespace, name))

    def _attrs_to_dict(self, attrs):
        if isinstance(attrs, dict):
            return attrs
        return self.dict_constructor(zip(attrs[::2], attrs[1::2]))

    def startNamespaceDecl(self, prefix, uri):
        self.namespace_declarations[prefix or ''] = uri

    def startElement(self, full_name, attrs):
        name = self._build_name(full_name)
        attrs = self._attrs_to_dict(attrs)
        if attrs and self.namespace_declarations:
            attrs['xmlns'] = self.namespace_declarations
            self.namespace_declarations = OrderedDict()
        self.path.append((name, attrs or None))
        if len(self.path):
            self.stack.append((self.item, self.data))
            attr_entries = []
            for key, value in attrs.items():
                key = self.attr_prefix+self._build_name(key)
                entry = self.postprocessor(self.path, key, value) if self.postprocessor else (key, value)
                if entry:
                    attr_entries.append(entry)
            attrs = self.dict_constructor(attr_entries)
            self.item = attrs or None
            self.data = []

    def endElement(self, full_name):
        name = self._build_name(full_name)
        if not len(self.path):
            item = self.item
            if not item:
                item = None if not self.data else self.cdata_separator.join(self.data)
            
            if not self.item_callback(self.path, item):
                raise Exception("Parsing interrupted!")
        if len(self.stack):
            data = None if not self.data else self.cdata_separator.join(self.data)
            item = self.item
            self.item, self.data = self.stack.pop()
            if self.strip_whitespace and data:
                data = data.strip() or None
            if data and self.force_cdata and item is None:
                item = self.dict_constructor()
            if item:
                if data:
                    self.push_data(item, self.cdata_key, data)
                self.item = self.push_data(self.item, name, item)
            else:
                self.item = self.push_data(self.item, name, data)
        else:
            self.item = None
            self.data = []
        self.path.pop()

    def characters(self, data):
        if not self.data:
            self.data = [data]
        else:
            self.data.append(data)
    
    def push_data(self, item, key, data):
        if self.postprocessor:
            result = self.postprocessor(self.path, key, data)
            if not result:
                return item
            key, data = result
        if not item:
            item = self.dict_constructor()
        try:
            value = item[key]
            if isinstance(value, list):
                value.append(data)
            else:
                item[key] = [value, data]
        except KeyError:
            item[key] = data
        return item

def parse(xml_input, encoding='utf-8', expat=expat, namespace_separator=':', **kwargs):
    handler = _DictSAXHandler(namespace_separator=namespace_separator, **kwargs)
    xml_input = xml_input.encode(encoding)
    namespace_separator = None
    parser = expat.ParserCreate(
        encoding,
        namespace_separator
    )
    try:
        parser.ordered_attributes = True
    except AttributeError:
        # Jython's expat does not support ordered_attributes
        pass
    parser.StartNamespaceDeclHandler = handler.startNamespaceDecl
    parser.StartElementHandler = handler.startElement
    parser.EndElementHandler = handler.endElement
    parser.CharacterDataHandler = handler.characters
    parser.buffer_text = True
    try:
        # Attempt to disable DTD in Jython's expat parser (Xerces-J).
        feature = "http://apache.org/xml/features/disallow-doctype-decl"
        parser._reader.setFeature(feature, True)
    except AttributeError:
        # For CPython / expat parser.
        # Anything not handled ends up here and entities aren't expanded.
        parser.DefaultHandler = lambda x: None
        # Expects an integer return; zero means failure -> expat.ExpatError.
        parser.ExternalEntityRefHandler = lambda *x: 1
    parser.Parse(xml_input, True)
    return handler.item

def _process_namespace(name, namespaces, ns_sep=':', attr_prefix='@'):
    if not namespaces:
        return name
    try:
        ns, name = name.rsplit(ns_sep, 1)
    except ValueError:
        pass
    else:
        ns_res = namespaces.get(ns.strip(attr_prefix))
        name = '{}{}{}{}'.format(attr_prefix if ns.startswith(attr_prefix) else '', ns_res, ns_sep, name) if ns_res else name
    return name

def _emit(key, value, content_handler,
          attr_prefix='@',
          cdata_key='#text',
          depth=0,
          pretty=False,
          newl='\n',
          indent='\t',
          namespace_separator=':',
          namespaces=None,
          full_document=True,
          expand_iter=None):
    key = _process_namespace(key, namespaces, namespace_separator, attr_prefix)
    if (not hasattr(value, '__iter__')
            or isinstance(value, _basestring)
            or isinstance(value, dict)):
        value = [value]
    for index, v in enumerate(value):
        if full_document and (not depth) and index:
            raise ValueError('document with multiple roots')
        if not v:
            v = OrderedDict()
        elif isinstance(v, bool):
            v = _unicode('true') if v else _unicode('false')
        elif not isinstance(v, dict):
            v = OrderedDict(((expand_iter, v),)) if (expand_iter and hasattr(v, '__iter__') and not isinstance(v, _basestring)) else _unicode(v)
        if isinstance(v, _basestring):
            v = OrderedDict(((cdata_key, v),))
        cdata, attrs, children = OrderedDict(), None, []
        for ik, iv in v.items():
            if ik == cdata_key:
                cdata = iv
                continue
            if ik.startswith(attr_prefix):
                ik = _process_namespace(ik, namespaces, namespace_separator,
                                        attr_prefix)
                if ik == '@xmlns' and isinstance(iv, dict):
                    for k, v in iv.items():
                        attr = 'xmlns{}'.format(':{}'.format(k) if k else '')
                        attrs[attr] = _unicode(v)
                    continue
                if not isinstance(iv, _unicode):
                    iv = _unicode(iv)
                attrs[ik[len(attr_prefix):]] = iv
                continue
            children.append((ik, iv))
        if pretty: # wow so pretty
            content_handler.ignorableWhitespace(depth * indent)
        content_handler.startElement(key, AttributesImpl(attrs))
        if pretty and children:
            content_handler.ignorableWhitespace(newl)
        for child_key, child_value in children:
            _emit(child_key, child_value, content_handler,
                  attr_prefix, cdata_key, depth+1,
                  pretty, newl, indent, namespaces=namespaces,
                  namespace_separator=namespace_separator,
                  expand_iter=expand_iter)
        if cdata:
            content_handler.characters(cdata)
        if pretty and children:
            content_handler.ignorableWhitespace(depth * indent)
        content_handler.endElement(key)
        if pretty and depth:
            content_handler.ignorableWhitespace(newl)