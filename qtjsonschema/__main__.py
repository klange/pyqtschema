#!/usr/bin/env python
"""
pyqtschema - Python Qt JSON Schema Tool

Generate a dynamic Qt form representing a JSON Schema.
Filling the form will generate JSON.
"""

from PyQt4 import QtCore, QtGui

from qtjsonschema.widgets import create_widget

class MainWindow(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setWindowTitle("PyQtSchema")

        # Menu bar
        # File
        #  Open
        #  Save
        #  --
        #  Close

        self.menu = QtGui.QMenuBar(self)
        self.file_menu = self.menu.addMenu("&File")

        _action_open = QtGui.QAction("&Open Schema", self)
        _action_open.triggered.connect(self._handle_open)

        _action_save = QtGui.QAction("&Save", self)
        _action_save.triggered.connect(self._handle_save)

        _action_quit = QtGui.QAction("&Close", self)
        _action_quit.triggered.connect(self._handle_quit)

        self.file_menu.addAction(_action_open)
        self.file_menu.addAction(_action_save)
        self.file_menu.addSeparator()
        self.file_menu.addAction(_action_quit)

        # Scrollable region for schema form
        self.content_region = QtGui.QScrollArea(self)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.menu)
        vbox.addWidget(self.content_region)
        vbox.setContentsMargins(0,0,0,0)

        hbox = QtGui.QHBoxLayout()
        hbox.setContentsMargins(0,0,0,0)
        hbox.addLayout(vbox)

        self.setLayout(hbox)

    def process_schema(self, schema):
        """
            Load a schema and create the root element.
        """
        import json
        import collections
        with open(schema) as f:
            _schema = json.loads(f.read(), object_pairs_hook=collections.OrderedDict)

        if "title" in _schema:
            self.setWindowTitle("%s - PyQtSchema" % _schema["title"])

        self.content_region.setWidget(create_widget(_schema.get("title", "(root)"), _schema))
        self.content_region.setWidgetResizable(True)

    def _handle_open(self):
        # Open JSON Schema
        schema = QtGui.QFileDialog.getOpenFileName(self, 'Open Schema', filter="JSON Schema (*.schema *.json)")
        if schema:
            self.process_schema(schema)

    def _handle_save(self):
        # Save JSON output
        import json
        obj = self.content_region.widget().to_json_object()
        outfile = QtGui.QFileDialog.getSaveFileName(self, 'Save JSON', filter="JSON (*.json)")
        if outfile:
            with open(outfile, 'w') as f:
                f.write(json.dumps(obj))

    def _handle_quit(self):
        # TODO: Check if saved?
        self.close()


if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())
