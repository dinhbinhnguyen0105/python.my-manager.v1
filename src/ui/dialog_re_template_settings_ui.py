# Form implementation generated from reading ui file '/Volumes/KINGSTON/Dev/python/python.my-manager.v1/ui/dialog_re_template_settings.ui'
#
# Created by: PyQt6 UI code generator 6.8.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog_RETemplateSettings(object):
    def setupUi(self, Dialog_RETemplateSettings):
        Dialog_RETemplateSettings.setObjectName("Dialog_RETemplateSettings")
        Dialog_RETemplateSettings.resize(480, 443)
        Dialog_RETemplateSettings.setStyleSheet("#Dialog_RETemplateSettings{\n"
"  font-family: \"Courier New\";\n"
"  background-color: #FFFFFF;\n"
"}\n"
"QGroupBox {\n"
"  font-family: \"Courier New\";\n"
"  font-size: 13px;\n"
"  background-color: rgba(248, 249, 250, 1);\n"
"}\n"
"QLineEdit {\n"
"  padding: 4px 0;\n"
"  border: 1px solid #ced4da;\n"
"  border-radius: 8px;\n"
"  margin-left: 8px;\n"
"  padding-left: 4px;\n"
"  background-color: #FFFFFF;\n"
"  color:#212529;\n"
"}\n"
"QPlainTextEdit {\n"
"    background-color: #FFFFFF;\n"
"  color:#212529;\n"
"}\n"
"QLabel {\n"
"  font-family: \"Courier New\";\n"
"  font-size: 13px;\n"
"  color: rgb(90, 93, 97);\n"
"}\n"
"QRadioButton {\n"
"  font-family: \"Courier New\";\n"
"  font-size: 13px;\n"
"  color: #212529;\n"
"}\n"
"QComboBox {\n"
"  font-family: \"Courier New\";\n"
"  font-size: 13px;\n"
"  color: #212529;\n"
"}\n"
"QPushButton {\n"
"  color: #212529;\n"
"}\n"
"\n"
"")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(Dialog_RETemplateSettings)
        self.verticalLayout_7.setContentsMargins(8, 8, 8, 8)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.dialog_container = QtWidgets.QWidget(parent=Dialog_RETemplateSettings)
        self.dialog_container.setObjectName("dialog_container")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.dialog_container)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.options_container = QtWidgets.QGroupBox(parent=self.dialog_container)
        self.options_container.setTitle("")
        self.options_container.setObjectName("options_container")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.options_container)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.title_radio = QtWidgets.QRadioButton(parent=self.options_container)
        self.title_radio.setObjectName("title_radio")
        self.horizontalLayout.addWidget(self.title_radio)
        self.description_radio = QtWidgets.QRadioButton(parent=self.options_container)
        self.description_radio.setObjectName("description_radio")
        self.horizontalLayout.addWidget(self.description_radio)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.verticalLayout_5.addWidget(self.options_container)
        self.description_container = QtWidgets.QWidget(parent=self.dialog_container)
        self.description_container.setObjectName("description_container")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.description_container)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.description_label = QtWidgets.QLabel(parent=self.description_container)
        self.description_label.setObjectName("description_label")
        self.verticalLayout_4.addWidget(self.description_label)
        self.description_input = QtWidgets.QPlainTextEdit(parent=self.description_container)
        self.description_input.setObjectName("description_input")
        self.verticalLayout_4.addWidget(self.description_input)
        self.verticalLayout_3.addLayout(self.verticalLayout_4)
        self.verticalLayout_5.addWidget(self.description_container)
        self.title_container = QtWidgets.QWidget(parent=self.dialog_container)
        self.title_container.setObjectName("title_container")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.title_container)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.title_label = QtWidgets.QLabel(parent=self.title_container)
        self.title_label.setStyleSheet("margin: 0; padding-left: 4px;")
        self.title_label.setObjectName("title_label")
        self.verticalLayout.addWidget(self.title_label)
        self.title_input = QtWidgets.QLineEdit(parent=self.title_container)
        self.title_input.setObjectName("title_input")
        self.verticalLayout.addWidget(self.title_input)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_5.addWidget(self.title_container)
        self.button_container = QtWidgets.QGroupBox(parent=self.dialog_container)
        self.button_container.setTitle("")
        self.button_container.setObjectName("button_container")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.button_container)
        self.horizontalLayout_4.setContentsMargins(8, 8, 8, 8)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.create_btn = QtWidgets.QPushButton(parent=self.button_container)
        self.create_btn.setObjectName("create_btn")
        self.gridLayout.addWidget(self.create_btn, 1, 0, 1, 1)
        self.delete_btn = QtWidgets.QPushButton(parent=self.button_container)
        self.delete_btn.setEnabled(True)
        self.delete_btn.setObjectName("delete_btn")
        self.gridLayout.addWidget(self.delete_btn, 1, 1, 1, 1)
        self.options_combobox = QtWidgets.QComboBox(parent=self.button_container)
        self.options_combobox.setObjectName("options_combobox")
        self.gridLayout.addWidget(self.options_combobox, 0, 0, 1, 2)
        self.horizontalLayout_4.addLayout(self.gridLayout)
        self.verticalLayout_5.addWidget(self.button_container)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_5.addItem(spacerItem)
        self.tableView = QtWidgets.QTableView(parent=self.dialog_container)
        self.tableView.setObjectName("tableView")
        self.verticalLayout_5.addWidget(self.tableView)
        self.verticalLayout_6.addLayout(self.verticalLayout_5)
        self.verticalLayout_7.addWidget(self.dialog_container)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=Dialog_RETemplateSettings)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_7.addWidget(self.buttonBox)

        self.retranslateUi(Dialog_RETemplateSettings)
        self.buttonBox.accepted.connect(Dialog_RETemplateSettings.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog_RETemplateSettings.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog_RETemplateSettings)

    def retranslateUi(self, Dialog_RETemplateSettings):
        _translate = QtCore.QCoreApplication.translate
        Dialog_RETemplateSettings.setWindowTitle(_translate("Dialog_RETemplateSettings", "Dialog"))
        self.title_radio.setText(_translate("Dialog_RETemplateSettings", "Title"))
        self.description_radio.setText(_translate("Dialog_RETemplateSettings", "Description"))
        self.description_label.setText(_translate("Dialog_RETemplateSettings", " Description"))
        self.title_label.setText(_translate("Dialog_RETemplateSettings", "Title"))
        self.create_btn.setText(_translate("Dialog_RETemplateSettings", "Add new"))
        self.delete_btn.setText(_translate("Dialog_RETemplateSettings", "Delete"))
