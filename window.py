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
        #basic_box = self.create_form_group_box()
        basic_box = self.create_box('basic')
        self.boxes_layout.addWidget(basic_box)


        #create the box for system information
        self.system_box = self.create_box("system")
        self.boxes_layout.addWidget(self.system_box)





        self.scroll_area.setWidget(self.boxes_widget)
        self.setLayout(self.main_layout)

        #set the dimensions of the form
#        self.setGeometry(10,10,500,500)
 

    def create_box(self,group_name):

#        group_box = QGroupBox("System Information")
        group_box = InputBox("System Information",self)

        #set group_box information
        #group_box.setFixedHeight(200)

        if group_name == 'basic':
            self.create_basic_box(group_box)
        elif group_name == 'system':
            self.create_system_box(group_box)
        else:
            raise LookupError('Group name not recognized')

        group_box.setLayout(group_box.layout)

        return group_box



    def create_basic_box(self,group_box):

        #title
        titleLineEdit = QLineEdit()
        titleLineEdit.setToolTip('Enter a title for the calculation.\nThis has no impact on the results.')
        group_box.layout.addRow(QLabel("Title:"), titleLineEdit)

        #calculation
        self.calculationComboBox = QComboBox()
        self.calculationComboBox.addItem("SCF (Self-Consistent Field)")
        self.calculationComboBox.addItem("NSCF (Non-Self-Consistent Field)") #replace with maximum_iterations?
        self.calculationComboBox.addItem("Bands") #how is this different from NSCF?
        self.calculationComboBox.addItem("Geometry Relaxation") #note: includes vc-relax
        self.calculationComboBox.addItem("Molecular Dynamics") #note: includes vc-md
        group_box.layout.addRow(QLabel("Calculation:"), self.calculationComboBox)

        #verbosity
        group_box.layout.addRow(QLabel("Verbose:"), QCheckBox())

        #restart_mode
        group_box.layout.addRow(QLabel("Restart:"), QCheckBox())

        #wf_collect - just set to .true.
        group_box.layout.addRow(QLabel("Collect Wavefunctions:"), QCheckBox())

        button = QPushButton('Next', self)
        button.setToolTip('Proceed to the next input set.')
        button.clicked.connect(group_box.on_click)
        group_box.layout.addRow(button)

        group_box.next_group_box = 'system'


        


    #--------------------------------------------------------#
    # System Inputs
    #--------------------------------------------------------#
    def create_system_box(self,group_box):

        #nstep
        titleLineEdit = QLineEdit()
        titleLineEdit.setToolTip('Enter a title for the calculation.\nThis has no impact on the results.')
        group_box.layout.addRow(QLabel("nstep:"), titleLineEdit)


        button = QPushButton('Next', self)
        button.setToolTip('Proceed to the next input set.')
        button.clicked.connect(group_box.on_click)
        group_box.layout.addRow(button)

        group_box.next_group_box = 'data'










class InputBox(QGroupBox):
 
    def __init__(self,name,parent):
        super(QGroupBox, self).__init__(name,parent)
        
        self.layout = QFormLayout()
        self.parent = parent

    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')

        #create the box for system information
        self.parent.system_box = self.parent.create_box(self.next_group_box)
        self.parent.boxes_layout.addWidget(self.parent.system_box)
        



 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = Dialog()
sys.exit(dialog.exec_())
