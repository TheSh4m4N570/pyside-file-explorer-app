from functools import partial
from PySide6 import QtWidgets, QtCore, QtGui


class MainWindow(QtWidgets.QMainWindow):
    """
    Main Window is a class that represents the main window of a file explorer application. It inherits from QtWidgets.QMainWindow.

    **Attributes:**

    - `view_mode`: A class attribute that represents the view mode of the list view. By default, it is set to `QtWidgets.QListView.ViewMode.IconMode`.

    **Constructor:**

    - `__init__(self, ctx)`: Initializes the MainWindow object. It takes a single parameter `ctx` which represents the context of the application. It calls the constructor of the parent
    * class (`QtWidgets.QMainWindow`) and sets the window title to "Py Explorer". It also calls the `setup_ui()` and `create_file_model()` methods.

    **Methods:**

    - `setup_ui(self)`: Sets up the user interface of the main window. It creates various widgets, modifies their properties, creates the layout, adds the widgets to the layout, adds actions
    * to the toolbar, and sets up event handlers.

    - `create_widgets(self)`: Creates various widgets used in the main window such as `toolbar`, `tree_view`, `list_view`, `slider`, and `main_widget`.

    - `modify_widgets(self)`: Modifies the properties of the widgets. It sets the style sheet of the main window using the context resource "style.css", sets the view mode of the list view
    *, sets uniform item sizes, sets the icon size, enables sorting and alternating row colors for the tree view, and sets the section resize mode for the tree view header.

    - `create_layout(self)`: Creates the main layout for the main widget. It uses a horizontal layout (`QHBoxLayout`) and sets it as the main layout for the main widget.

    - `add_widgets_to_layouts(self)`: Adds the created widgets to the layouts. It adds the toolbar to the top tool bar area, adds the tree view, list view, and slider to the main layout
    *.

    - `setup_events(self)`: Sets up event handlers for various signals. It connects the `clicked`, `doubleClicked`, and `valueChanged` signals of the tree view, list view, and slider, respectively
    *, to their respective slots.

    - `change_icon_size(self, value)`: Slot method that changes the icon size of the list view based on the provided `value`.

    - `create_file_model(self)`: Creates a file model for the tree view and list view. It sets the root path of the model to the root path of the file system, and sets the same model and
    * root index for both tree view and list view.

    - `tree_view_clicked(self, index)`: Slot method that is called when a tree view item is clicked. If the clicked item is a directory, it sets the root index of the list view to the clicked
    * index. Otherwise, it sets the root index to the parent index of the clicked index.

    - `list_view_clicked(self, index)`: Slot method that is called when a list view item is clicked. It sets the current index of the tree view's selection model to the clicked index.

    - `list_view_double_clicked(self, index)`: Slot method that is called when a list view item is double clicked. It sets the root index of the list view to the double clicked index.

    - `add_actions_to_toolbar(self)`: Adds actions to the toolbar. It iterates over a list of locations and creates an action for each location. The action icons are set based on the context
    * resources and the action is connected to the `change_location` slot.

    - `change_location(self, location)`: Slot method that is called when a location action in the toolbar is triggered. It changes the root index of both tree view and list view to the specified
    * location.

    Note: This class assumes the presence of the `QtCore`, `QtGui`, and `QtWidgets` modules from the `PyQt5` library.
    """
    view_mode = QtWidgets.QListView.ViewMode.IconMode
    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx
        self.setWindowTitle('Py Explorer')
        self.setup_ui()
        self.create_file_model()

    def setup_ui(self):
        self.create_widgets()
        self.modify_widgets()
        self.create_layout()
        self.add_widgets_to_layouts()
        self.add_actions_to_toolbar()
        self.setup_events()

    def create_widgets(self):
        self.toolbar = QtWidgets.QToolBar()
        self.tree_view = QtWidgets.QTreeView()
        self.list_view = QtWidgets.QListView()
        self.slider = QtWidgets.QSlider()
        self.main_widget = QtWidgets.QWidget()

    def modify_widgets(self):
        css_file = self.ctx.get_resource("style.css")
        with open(css_file, "r") as f:
            self.setStyleSheet(f.read())

        self.list_view.setViewMode(self.view_mode)
        self.list_view.setUniformItemSizes(True)
        self.list_view.setIconSize(QtCore.QSize(48, 48))

        self.slider.setRange(48, 256)
        self.slider.setValue(48)

        self.tree_view.setSortingEnabled(True)
        self.tree_view.setAlternatingRowColors(True)
        self.tree_view.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

    def create_layout(self):
        self.main_layout = QtWidgets.QHBoxLayout(self.main_widget)
        self.setCentralWidget(self.main_widget)

    def add_widgets_to_layouts(self):
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolbar)
        self.main_layout.addWidget(self.tree_view)
        self.main_layout.addWidget(self.list_view)
        self.main_layout.addWidget(self.slider)

    def setup_events(self):
        self.tree_view.clicked.connect(self.tree_view_clicked)
        self.list_view.clicked.connect(self.list_view_clicked)
        self.list_view.doubleClicked.connect(self.list_view_double_clicked)
        self.slider.valueChanged.connect(self.change_icon_size)

    def change_icon_size(self, value):
        self.list_view.setIconSize(QtCore.QSize(value, value))


    def create_file_model(self):
        self.model = QtWidgets.QFileSystemModel()
        root_path = QtCore.QDir.rootPath()
        self.model.setRootPath(root_path)
        self.tree_view.setModel(self.model)
        self.list_view.setModel(self.model)
        self.list_view.setRootIndex(self.model.index(root_path))
        self.tree_view.setRootIndex(self.model.index(root_path))

    def tree_view_clicked(self, index):
        if self.model.isDir(index):
            self.list_view.setRootIndex(index)
        else:
            self.list_view.setRootIndex(index.parent())

    def list_view_clicked(self, index):
        self.tree_view.selectionModel().setCurrentIndex(index, QtCore.QItemSelectionModel.ClearAndSelect)

    def list_view_double_clicked(self, index):
        self.list_view.setRootIndex(index)


    def add_actions_to_toolbar(self):
        locations = ["home", "desktop", "documents", "movies", "pictures", "music"]
        for location in locations:
            icon = self.ctx.get_resource(f"{location}.svg")
            action = self.toolbar.addAction(QtGui.QIcon(icon), location.capitalize())
            action.triggered.connect(partial(self.change_location, location))


    def change_location(self, location):
        standard_path = QtCore.QStandardPaths()
        path = eval(f"standard_path.standardLocations(QtCore.QStandardPaths.{location.capitalize()}Location)")
        path = path[0]
        self.tree_view.setRootIndex(self.model.index(path))
        self.list_view.setRootIndex(self.model.index(path))