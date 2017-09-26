from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
        QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
        QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QScrollArea, QSpinBox, 
        QTextEdit, QVBoxLayout, QWidget)
from PyQt5.QtCore import pyqtSlot
 
import sys
 
class Dialog(QDialog):
 
    def __init__(self):
        super(Dialog, self).__init__()



        self.central_widget = QWidget()

        self.setWindowTitle("Quantum ESPRESSO Input Form")
 
        self.main_layout = QVBoxLayout(self.central_widget)


        #inside of the main layout is a scroll area
        self.scroll_area = QScrollArea(self.central_widget)
        self.scroll_area.setWidgetResizable(True)
        self.main_layout.addWidget(self.scroll_area)

        #inside of the scroll area is another widget that will contain everything else
        self.boxes_widget = QWidget()
        self.boxes_layout = QVBoxLayout(self.boxes_widget)






        #create the box for basic information
        basic_box = self.create_form_group_box()
        self.boxes_layout.addWidget(basic_box)


        #create the box for system information
        self.system_box = self.create_system_box()
        self.boxes_layout.addWidget(self.system_box)





        self.scroll_area.setWidget(self.boxes_widget)
        self.setLayout(self.main_layout)

        #set the dimensions of the form
#        self.setGeometry(10,10,500,500)
 
    def create_form_group_box(self):
        group_box = QGroupBox("Basic Information")

        #set GroupBox information
        #self.formGroupBox.setMaximumHeight(200)
        group_box.setFixedHeight(200)
        #self.setContentsMargins(0,100,0,0)
        #self.setContentsMargins(0,start_y,0,0)



        layout = QFormLayout()


#        self.formGroupBox.setFlat(False)



        #title
        titleLineEdit = QLineEdit()
        titleLineEdit.setToolTip('Enter a title for the calculation.\nThis has no impact on the results.')
        layout.addRow(QLabel("Title:"), titleLineEdit)
#        layout.addRow(QLabel("Calculation:"), QComboBox())
#        layout.addRow(QLabel("Age:"), QSpinBox())

        #calculation
        self.calculationComboBox = QComboBox()
        self.calculationComboBox.addItem("SCF (Self-Consistent Field)")
        self.calculationComboBox.addItem("NSCF (Non-Self-Consistent Field)") #replace with maximum_iterations?
        self.calculationComboBox.addItem("Bands") #how is this different from NSCF?
        self.calculationComboBox.addItem("Geometry Relaxation") #note: includes vc-relax
        self.calculationComboBox.addItem("Molecular Dynamics") #note: includes vc-md
        layout.addRow(QLabel("Calculation:"), self.calculationComboBox)

        #verbosity
        layout.addRow(QLabel("Verbose:"), QCheckBox())

        #restart_mode
        layout.addRow(QLabel("Restart:"), QCheckBox())

        #wf_collect - just set to .true.
        layout.addRow(QLabel("Collect Wavefunctions:"), QCheckBox())







        group_box.setLayout(layout)



        button = QPushButton('Next', self)
        button.setToolTip('Proceed to the next input set.')
        button.clicked.connect(self.on_click)
        layout.addRow(button)

        return group_box





    def create_system_box(self):
        group_box = QGroupBox("System Information")

        #set group_box information
        #group_box.setFixedHeight(200)

        layout = QFormLayout()



        #--------------------------------------------------------#
        # System Inputs
        #--------------------------------------------------------#

        #nstep
        titleLineEdit = QLineEdit()
        titleLineEdit.setToolTip('Enter a title for the calculation.\nThis has no impact on the results.')
        layout.addRow(QLabel("nstep:"), titleLineEdit)




        button = QPushButton('Next', self)
        button.setToolTip('Proceed to the next input set.')
        button.clicked.connect(self.on_click)
        layout.addRow(button)




        group_box.setLayout(layout)




        return group_box







    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')

        #create the box for system information
        self.system_box = self.create_system_box()
        self.boxes_layout.addWidget(self.system_box)


 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = Dialog()
sys.exit(dialog.exec_())
