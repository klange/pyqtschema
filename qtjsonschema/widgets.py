"""
Widget definitions for JSON schema elements.
"""
from PyQt4 import QtCore, QtGui

class UnsupportedSchema(QtGui.QLabel):
    """
        Widget representation of an unsupported schema element.

        Presents a label noting the name of the element and its type.
        If the element is a reference, the reference name is listed instead of a type.
    """
    def __init__(self, name, schema, parent=None):
        self.name = name
        self.schema = schema
        self._type = schema.get("type", schema.get("$ref", "(?)"))
        QtGui.QLabel.__init__(self, "(Unsupported schema entry: %s, %s)" % (name, self._type), parent)
        self.setStyleSheet("QLabel { font-style: italic; }")

    def to_json_object(self):
        return "(unsupported)"

class JsonObject(QtGui.QGroupBox):
    """
        Widget representaiton of an object.

        Objects have properties, each of which is a widget of its own.
        We display these in a groupbox, which on most platforms will
        include a border.
    """
    def __init__(self, name, schema, parent=None):
        QtGui.QGroupBox.__init__(self, name, parent)
        self.name = name
        self.schema = schema
        self.vbox = QtGui.QVBoxLayout()
        self.vbox.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(self.vbox)
        self.setFlat(False)

        if "description" in schema:
            self.setToolTip(schema['description'])

        self.properties = {}

        if "properties" not in schema:
            label = QtGui.QLabel("Invalid object description (missing properties)", self)
            label.setStyleSheet("QLabel { color: red; }")
            self.vbox.addWidget(label)
        else:
            for k, v in schema['properties'].iteritems():
                widget = create_widget(k, v)
                self.vbox.addWidget(widget)
                self.properties[k] = widget

    def to_json_object(self):
        out = {}
        for k, v in self.properties.iteritems():
            out[k] = v.to_json_object()
        return out


class JsonString(QtGui.QWidget):
    """
        Widget representation of a string.

        Strings are text boxes with labels for names.
    """
    def __init__(self, name, schema, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.name = name
        self.schema = schema
        hbox = QtGui.QHBoxLayout()

        self.label = QtGui.QLabel(name)
        self.edit  = QtGui.QLineEdit()

        if "description" in schema:
            self.label.setToolTip(schema['description'])

        hbox.addWidget(self.label)
        hbox.addWidget(self.edit)

        self.setLayout(hbox)

    def to_json_object(self):
        return str(self.edit.text())


class JsonInteger(QtGui.QWidget):
    """
        Widget representation of an integer (SpinBox)
    """
    def __init__(self, name, schema, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.name = name
        self.schema = schema
        hbox = QtGui.QHBoxLayout()

        self.label = QtGui.QLabel(name)
        self.spin  = QtGui.QSpinBox()

        if "description" in schema:
            self.label.setToolTip(schema['description'])

        # TODO: min/max

        hbox.addWidget(self.label)
        hbox.addWidget(self.spin)

        self.setLayout(hbox)

    def to_json_object(self):
        return self.spin.value()


class JsonNumber(QtGui.QWidget):
    """
        Widget representation of a number (DoubleSpinBox)
    """
    def __init__(self, name, schema, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.name = name
        self.schema = schema
        hbox = QtGui.QHBoxLayout()

        self.label = QtGui.QLabel(name)
        self.spin  = QtGui.QDoubleSpinBox()

        if "description" in schema:
            self.label.setToolTip(schema['description'])

        # TODO: min/max

        hbox.addWidget(self.label)
        hbox.addWidget(self.spin)

        self.setLayout(hbox)

    def to_json_object(self):
        return self.spin.value()


class JsonArray(QtGui.QWidget):
    """
        Widget representation of an array.

        Arrays can contain multiple objects of a type, or
        they can contain objects of specific types.

        We include a label and button for adding types.
    """
    def __init__(self, name, schema, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.name = name
        self.schema = schema
        self.count = 0
        self.vbox = QtGui.QVBoxLayout()

        self.controls = QtGui.QHBoxLayout()

        label = QtGui.QLabel(name, self)
        label.setStyleSheet("QLabel { font-weight: bold; }")

        if "description" in schema:
            self.label.setToolTip(schema['description'])

        button = QtGui.QPushButton("Append Item", self)
        button.clicked.connect(self.click_add)

        self.controls.addWidget(label)
        self.controls.addWidget(button)

        self.vbox.addLayout(self.controls)

        self.setLayout(self.vbox)

    def click_add(self):
        # TODO: Support array for "items"
        # TODO: Support additionalItems
        if "items" in self.schema:
            obj = create_widget("Item #%d" % (self.count,), self.schema['items'], self)
            self.count += 1
            self.vbox.addWidget(obj)

    def to_json_object(self):
        out = []
        for i in range(1, self.vbox.count()):
            widget = self.vbox.itemAt(i).widget()
            if "to_json_object" in dir(widget):
                out.append(widget.to_json_object())
        return out


class JsonBoolean(QtGui.QCheckBox):
    """
        Widget representing a boolean (CheckBox)
    """
    def __init__(self, name, schema, parent=None):
        QtGui.QCheckBox.__init__(self, name, parent)
        self.name = name
        self.schema = schema

        if "description" in schema:
            self.setToolTip(schema['description'])

    def to_json_object(self):
        return bool(self.isChecked())


def create_widget(name, schema, parent=None):
    """
        Create the appropriate widget for a given schema element.
    """
    if "type" not in schema:
        return UnsupportedSchema(name, schema, parent)

    if schema['type'] == "object":
        return JsonObject(name, schema, parent)
    elif schema['type'] == "string":
        return JsonString(name, schema, parent)
    elif schema['type'] == "integer":
        return JsonInteger(name, schema, parent)
    elif schema['type'] == "array":
        return JsonArray(name, schema, parent)
    elif schema['type'] == "number":
        return JsonNumber(name, schema, parent)
    elif schema['type'] == "boolean":
        return JsonBoolean(name, schema, parent)

    # TODO: refs

    return UnsupportedSchema(name, schema, parent)


