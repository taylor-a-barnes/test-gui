from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
        QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
        QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
        QVBoxLayout)
from PyQt5.QtCore import pyqtSlot
 
import sys
 
class Dialog(QDialog):
#    NumGridRows = 3
#    NumButtons = 4
 
    def __init__(self):
        super(Dialog, self).__init__()
        self.createFormGroupBox()
 
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
 
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
#        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
 
        self.setWindowTitle("Quantum ESPRESSO Input Form")

        #set the dimensions of the form
        self.setGeometry(10,10,500,500)
 
    def createFormGroupBox(self):
        self.formGroupBox = QGroupBox("Basic Information")

        #set GroupBox information
        #self.formGroupBox.setMaximumHeight(200)
        self.formGroupBox.setFixedHeight(200)
        #self.setContentsMargins(0,100,0,0)
        self.setContentsMargins(0,0,0,0)



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







        self.formGroupBox.setLayout(layout)



        button = QPushButton('Next', self)
        button.setToolTip('Proceed to the next input set.')
#        button.move(100,410)
        button.clicked.connect(self.on_click)
        layout.addRow(button)



    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')


 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = Dialog()
sys.exit(dialog.exec_())
