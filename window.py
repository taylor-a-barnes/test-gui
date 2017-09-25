from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
        QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
        QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
        QVBoxLayout, QCheckBox)
from PyQt5.QtCore import pyqtSlot
 
import sys
 
class Dialog(QDialog):
 
    def __init__(self):
        super(Dialog, self).__init__()
        basic_box = self.create_form_group_box(start_y=0)
 
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
 
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(basic_box)
#        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
 
        self.setWindowTitle("Quantum ESPRESSO Input Form")

        print(str(self.height()))







        #set the dimensions of the form
#        self.setGeometry(10,10,500,500)
 
    def create_form_group_box(self,start_y):
        form_group_box = QGroupBox("Basic Information")

        #set GroupBox information
        #self.formGroupBox.setMaximumHeight(200)
        form_group_box.setFixedHeight(200)
        #self.setContentsMargins(0,100,0,0)
        self.setContentsMargins(0,start_y,0,0)



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







        form_group_box.setLayout(layout)



        button = QPushButton('Next', self)
        button.setToolTip('Proceed to the next input set.')
#        button.move(100,410)
        button.clicked.connect(self.on_click)
        layout.addRow(button)

        return form_group_box



    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')


 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = Dialog()
sys.exit(dialog.exec_())
