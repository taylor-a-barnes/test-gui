"""
Simple GUI for Quantum ESPRESSO
"""

from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
        QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
        QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QScrollArea, QSpinBox, 
        QTextEdit, QVBoxLayout, QWidget )
from PyQt5.QtCore import (pyqtSlot)
 
import sys
 
class Dialog(QDialog):
 
    def __init__(self, input_file):
        super(Dialog, self).__init__()

        self.input_file = input_file


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
        #self.system_box = self.create_box("system")
        #self.boxes_layout.addWidget(self.system_box)





        self.scroll_area.setWidget(self.boxes_widget)
        self.setLayout(self.main_layout)

        #set the dimensions of the form
#        self.setGeometry(10,10,500,500)
 

    def create_box(self,group_name):

#        group_box = QGroupBox("System Information")
        name = group_name + " Information"
        group_box = InputBox(name)

        #set group_box information
        #group_box.setFixedHeight(200)

        if group_name == 'basic':
            self.create_basic_box(group_box)
        elif group_name == 'cell':
            self.create_cell_box(group_box)
        elif group_name == 'system':
            self.create_system_box(group_box)
        elif group_name == 'print':
            self.create_print_box(group_box)
        else:
            raise LookupError('Group name not recognized')

        group_box.setLayout(group_box.layout)

        return group_box



    def create_basic_box(self,group_box):

        #title
        widget = InputText( group_box, input_name="title" )
        widget.setToolTip('Enter a title for the calculation.\nThis has no impact on the results.')
        group_box.layout.addRow(QLabel("Title:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #calculation
        widget = InputCombo( group_box, "calculation" )
        widget.addItem("SCF (Self-Consistent Field)", userData = "scf")
        widget.addItem("NSCF (Non-Self-Consistent Field)", userData = "nscf") #replace with maximum_iterations?
        widget.addItem("Bands", userData = "bands") #how is this different from NSCF?
        widget.addItem("Geometry Relaxation", userData = "relax") #note: includes vc-relax
        widget.addItem("Molecular Dynamics", userData = "md") #note: includes vc-md
        group_box.layout.addRow(QLabel("Calculation:"), widget)
        widget.currentIndexChanged.connect( widget.on_index_changed )

        #verbosity
        widget = InputCheck( group_box, input_name="verbosity")
        group_box.layout.addRow(QLabel("Verbosity:"), widget)
        widget.stateChanged.connect( widget.on_state_changed )

        #restart_mode
        widget = InputCheck( group_box, input_name="restart_mode")
        group_box.layout.addRow(QLabel("Restart:"), widget)
        widget.stateChanged.connect( widget.on_state_changed )

        #wf_collect - just set to .true.
        widget = InputCheck( group_box, input_name="wf_collect")
        group_box.layout.addRow(QLabel("Collect Wavefunctions:"), widget)
        widget.stateChanged.connect( widget.on_state_changed )

        #max_seconds
        widget = InputText( group_box, input_name="max_seconds" )
        group_box.layout.addRow(QLabel("Checkpoint Time (hrs):"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #etot_conv_thr
        widget = InputText( group_box, input_name="etot_conv_thr" )
        group_box.layout.addRow(QLabel("Energy Convergece:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #force_conv_thr
        widget = InputText( group_box, input_name="force_conv_thr" )
        group_box.layout.addRow(QLabel("Force Convergece:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #disk_io
        widget = InputCombo( group_box, "disk_io" )
        widget.addItem("High", userData = "high")
        widget.addItem("Medium", userData = "medium")
        widget.addItem("Low", userData = "low")
        widget.addItem("None", userData = "none")
        group_box.layout.addRow(QLabel("Disk IO:"), widget)
        widget.currentIndexChanged.connect( widget.on_index_changed )

        button = QPushButton('Next', self)
        button.setToolTip('Proceed to the next input set.')
        button.clicked.connect(group_box.on_click)
        group_box.layout.addRow(button)

        group_box.next_group_box = 'cell'




    #--------------------------------------------------------#
    # Cell Inputs
    #--------------------------------------------------------#
    def create_cell_box(self,group_box):



        #ibrav
        widget = InputCombo( group_box, "ibrav" )
        widget.addItem("Custom", userData = "0")
        widget.addItem("Simple Cubic", userData = "1")
        widget.addItem("Face-Centered Cubic", userData = "2")
        widget.addItem("Body-Centered Cubic", userData = "3")
        widget.addItem("Hexagonal and Trigonal P", userData = "4")
        widget.addItem("Trigonal R, 3-fold axis c", userData = "5")
        widget.addItem("Trigonal R, 3-fold axis <111>", userData = "-5")
        widget.addItem("Tetragonal P", userData = "6")
        widget.addItem("Tetragonal I", userData = "7")
        widget.addItem("Orthorhombic P", userData = "8")
        widget.addItem("Base-Centered Orthorhombic", userData = "9")
        widget.addItem("Face-Centered Orthorhombic", userData = "10")
        widget.addItem("Body-Centered Orthorhombic", userData = "11")
        widget.addItem("Monoclinic P, unique axis c", userData = "12")
        widget.addItem("Monoclinic P, unique axis b", userData = "-12")
        widget.addItem("Base-Centered Monoclinic", userData = "13")
        widget.addItem("Triclinic", userData = "14")
        group_box.layout.addRow(QLabel("Lattice Type:"), widget)
        widget.currentIndexChanged.connect( widget.on_index_changed )
        
        #v1
        widget = InputText( group_box, input_name="v1" )
        group_box.layout.addRow(QLabel("v1:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #v2
        widget = InputText( group_box, input_name="v2" )
        group_box.layout.addRow(QLabel("v2:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #v3
        widget = InputText( group_box, input_name="v3" )
        group_box.layout.addRow(QLabel("v3:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #assume_isolated
        widget = InputCombo( group_box, "assume_isolated" )
        widget.addItem("None", userData = "none")
        widget.addItem("ESM (Effective Screening Medium)", userData = "esm")
        widget.addItem("Makov-Payne", userData = "makov-payne")
        widget.addItem("Martyna-Tuckerman", userData = "martyna-tuckerman")
        group_box.layout.addRow(QLabel("assume_isolated:"), widget)
        widget.currentIndexChanged.connect( widget.on_index_changed )

        #esm_bc
        widget = InputCombo( group_box, "esm_bc" )
        widget.addItem("Periodic", userData = "pbc")
        widget.addItem("Vacuum-Slab-Vacuum", userData = "bc1")
        widget.addItem("Metal-Slab-Metal", userData = "bc2")
        widget.addItem("Vacuum-Slab-Metal", userData = "bc3")
        group_box.layout.addRow(QLabel("esm_bc:"), widget)
        widget.currentIndexChanged.connect( widget.on_index_changed )

        #esm_w
        widget = InputText( group_box, input_name="esm_w" )
        group_box.layout.addRow(QLabel("esm_w:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #esm_nfit
        widget = InputText( group_box, input_name="esm_nfit" )
        group_box.layout.addRow(QLabel("esm_nfit:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

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
        widget = InputText( group_box, input_name="nstep" )
        group_box.layout.addRow(QLabel("nstep:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #nbnd
        widget = InputText( group_box, input_name="nbnd" )
        group_box.layout.addRow(QLabel("Number of Bands:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #tot_charge
        widget = InputText( group_box, input_name="tot_charge" )
        group_box.layout.addRow(QLabel("Charge:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #tot_magnetization
        widget = InputText( group_box, input_name="tot_magnetization" )
        group_box.layout.addRow(QLabel("tot_magnetization:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #ecutwfc
        widget = InputText( group_box, input_name="ecutwfc" )
        group_box.layout.addRow(QLabel("ecutwfc:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #ecutrho
        widget = InputText( group_box, input_name="ecutrho" )
        group_box.layout.addRow(QLabel("ecutrho:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #nr1, nr2, and nr3
        #nr1s, nr2s, and nr3s

        #ecutfock
        widget = InputText( group_box, input_name="ecutfock" )
        group_box.layout.addRow(QLabel("ecutfock:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #occupations
        widget = InputCombo( group_box, "occupations" )
        widget.addItem("Gaussian Smearing", userData = "smearing")
        widget.addItem("Tetrahedron (Bloechl Method)", userData = "tetrahedra")
        widget.addItem("Tetrahedron (Linear Method)", userData = "tetrahedra_lin")
        widget.addItem("Tetrahedron (Kawamura Method)", userData = "tetrahedra_opt")
        widget.addItem("Fixed", userData = "fixed")
        widget.addItem("Custom", userData = "from_input")
        group_box.layout.addRow(QLabel("occupations:"), widget)
        widget.currentIndexChanged.connect( widget.on_index_changed )

#NOTE: for occupations, default to 'smearing', unless doing DOS or phonons, in which case use 'tetrahedra_opt' - the Kawamura Method
        
        #smearing
        widget = InputCombo( group_box, "smearing" )
        widget.addItem("Ordinary Gaussian", userData = "gaussian")
        widget.addItem("Methfessel-Paxton", userData = "methfessel-paxton")
        widget.addItem("Marzari-Vanderbilt", userData = "marzari-vanderbilt")
        widget.addItem("Fermi-Dirac", userData = "Fermi-Dirac")
        group_box.layout.addRow(QLabel("Smearing Method:"), widget)
        widget.currentIndexChanged.connect( widget.on_index_changed )
        
#NOTE: default to Marzari-Vanderbilt 'cold smearing'

        #degauss
        widget = InputText( group_box, input_name="degauss" )
        group_box.layout.addRow(QLabel("degauss:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

#NOTE: degauss has suggested values of 0.06-0.10 Ry

        #nspin
        widget = InputCombo( group_box, "nspin" )
        widget.addItem("Non-Polarized", userData = "1")
        widget.addItem("Spin-Polarized", userData = "2")
        widget.addItem("Noncollinear Spin-Polarized", userData = "4")
        group_box.layout.addRow(QLabel("Spin Polarization:"), widget)
        widget.currentIndexChanged.connect( widget.on_index_changed )

        #input_dft
        widget = InputCombo( group_box, "input_dft" )
        widget.addItem("BLYP", userData = "blyp")
        widget.addItem("PBE", userData = "pbe")
        widget.addItem("PBE0", userData = "pbe0")
        widget.addItem("HSE", userData = "hse")
        group_box.layout.addRow(QLabel("DFT Functional:"), widget)
        widget.currentIndexChanged.connect( widget.on_index_changed )

        #exx_fraction
        widget = InputText( group_box, input_name="exx_fraction" )
        group_box.layout.addRow(QLabel("exx_fraction:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #screening_parameter
        widget = InputText( group_box, input_name="screening_parameter" )
        group_box.layout.addRow(QLabel("screening_parameter:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #exxdiv_treatment
        widget = InputText( group_box, input_name="exxdiv_treatment" )
        group_box.layout.addRow(QLabel("exxdiv_treatment:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #x_gamma_extrapolation
        widget = InputText( group_box, input_name="x_gamma_extrapolation" )
        group_box.layout.addRow(QLabel("x_gamma_extrapolation:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #ecutvcut
        widget = InputText( group_box, input_name="ecutvcut" )
        group_box.layout.addRow(QLabel("ecutvcut:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #nqx1, nqx2, nqx3
        widget = InputText( group_box, input_name="nqx1" )
        group_box.layout.addRow(QLabel("nqx1, nqx2, nqx3:"), widget)
        widget.textChanged.connect( widget.on_text_changed )




        
        #--------------------------------------------------------#
        # Per-species information
        #--------------------------------------------------------#

        #starting_magnetization
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("starting_magnetization:"), widget)



        button = QPushButton('Next', self)
        button.setToolTip('Proceed to the next input set.')
        button.clicked.connect(group_box.on_click)
        group_box.layout.addRow(button)

        group_box.next_group_box = 'print'


    #--------------------------------------------------------#
    # Hubbard Inputs
    #--------------------------------------------------------#
    def create_hubbard_box(self,group_box):

        #lda_plus_u
        widget = InputCheck( group_box, input_name="lda_plus_u")
        group_box.layout.addRow(QLabel("DFT+U:"), widget)
        widget.stateChanged.connect( widget.on_state_changed )

#NOTE: Instead of having a checkbox, just turn DFT+U on if a non-zero U is applied to any species

        #lda_plus_u_kind
        widget = InputCheck( group_box, input_name="lda_plus_u_kind")
        group_box.layout.addRow(QLabel("DFT+U+J:"), widget)
        widget.stateChanged.connect( widget.on_state_changed )

#NOTE: Instead of having a checkbox, just turn DFT+U+J on if a non-zero J is applied to any species

        #U_projection_type
        widget = InputCombo( group_box, "U_projection_type" )
        widget.addItem("Atomic", userData = "atomic")
        widget.addItem("Ortho-Atomic", userData = "ortho-atomic")
        widget.addItem("Norm-Atomic", userData = "norm-atomic")
        widget.addItem("File", userData = "file")
        widget.addItem("Pseudo", userData = "pseudo")
        group_box.layout.addRow(QLabel("DFT Functional:"), widget)
        widget.currentIndexChanged.connect( widget.on_index_changed )

        #starting_ns_eigenvalue(m,ispin,l)
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("starting_ns_eigenvalue:"), widget)

        #--------------------------------------------------------#
        # Per-species information
        #--------------------------------------------------------#

        #Hubbard_U
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("U:"), widget)

        #Hubbard_J0
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("J0:"), widget)

        #Hubbard_alpha
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("alpha:"), widget)

        #Hubbard_beta
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("beta:"), widget)

        #Hubbard_J
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("J:"), widget)




    #--------------------------------------------------------#
    # VdW Inputs
    #--------------------------------------------------------#
    def create_vdw_box(self,group_box):

        #vdw_corr
        widget = InputCombo( group_box, "vdw_corr" )
        widget.addItem("None", userData = "none") #NOTE: This is not a default setting
        widget.addItem("Grimme-D2", userData = "grimme-d2")
        widget.addItem("Tkatchenko-Scheffler", userData = "tkatchenko-scheffler")
        widget.addItem("XDM", userData = "xdm")
        group_box.layout.addRow(QLabel("Van der Waals Correction:"), widget)
        widget.currentIndexChanged.connect( widget.on_index_changed )

        #london_rcut
        widget = InputText( group_box, input_name="london_rcut" )
        group_box.layout.addRow(QLabel("london_rcut:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #ts_vdw_econv_thr
        widget = InputText( group_box, input_name="ts_vdw_econv_thr" )
        group_box.layout.addRow(QLabel("ts_vdw_econv_thr:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #ts_vdw_isolated
        widget = InputText( group_box, input_name="ts_vdw_isolated" )
        group_box.layout.addRow(QLabel("ts_vdw_isolated:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #london_s6
        widget = InputText( group_box, input_name="london_s6" )
        group_box.layout.addRow(QLabel("london_s6:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #xdm_a1
        widget = InputText( group_box, input_name="xdm_a1" )
        group_box.layout.addRow(QLabel("xdm_a1:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #xdm_a2
        widget = InputText( group_box, input_name="xdm_a2" )
        group_box.layout.addRow(QLabel("xdm_a2:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #--------------------------------------------------------#
        # Per-species information
        #--------------------------------------------------------#

        #london_c6
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("london_c6:"), widget)

        #london_rvdw
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("london_rvdw:"), widget)



    #--------------------------------------------------------#
    # MD Inputs
    #--------------------------------------------------------#
    def create_md_box(self,group_box):

        #dt
        widget = InputText( group_box, input_name="dt" )
        group_box.layout.addRow(QLabel("Timestep:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        button = QPushButton('Next', self)
        button.setToolTip('Proceed to the next input set.')
        button.clicked.connect(group_box.on_click)
        group_box.layout.addRow(button)

        group_box.next_group_box = 'print'




    #--------------------------------------------------------#
    # Magnetization Inputs
    #--------------------------------------------------------#
    def create_efield_box(self,group_box):

         #starting_spin_angle
        widget = InputCheck( group_box, input_name="starting_spin_angle")
        group_box.layout.addRow(QLabel("starting_spin_angle:"), widget)
        widget.stateChanged.connect( widget.on_state_changed )

        #constrainted_magnetization
        widget = InputCombo( group_box, "constrained_magnetization" )
        widget.addItem("None", userData = "none")
        widget.addItem("Total", userData = "total")
        widget.addItem("Atomic", userData = "atomic")
        widget.addItem("Total Direction", userData = "total_direction")
        widget.addItem("Atomic Direction", userData = "atomic_direction")
        group_box.layout.addRow(QLabel("constrained_magnetization:"), widget)
        widget.currentIndexChanged.connect( widget.on_index_changed )

        #fixed_magnetization
        widget = InputText( group_box, input_name="fixed_magnetization" )
        group_box.layout.addRow(QLabel("fixed_magnetization:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #lambda
        widget = InputText( group_box, input_name="lambda" )
        group_box.layout.addRow(QLabel("lambda:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #report
        widget = InputText( group_box, input_name="report" )
        group_box.layout.addRow(QLabel("report:"), widget)
        widget.textChanged.connect( widget.on_text_changed )



    #--------------------------------------------------------#
    # Noncollinear Inputs
    #--------------------------------------------------------#
    def create_noncollinear_box(self,group_box):

        #lspinorb
        widget = InputCheck( group_box, input_name="lspinorb")
        group_box.layout.addRow(QLabel("lspinorb:"), widget)
        widget.stateChanged.connect( widget.on_state_changed )
        
        #--------------------------------------------------------#
        # Per-species information
        #--------------------------------------------------------#

        #angle1
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("angle1:"), widget)

        #angle2
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("angle2:"), widget)


    #--------------------------------------------------------#
    # Electric Field Inputs
    #--------------------------------------------------------#
    def create_efield_box(self,group_box):

        #tefield
        widget = InputCheck( group_box, input_name="tefield")
        group_box.layout.addRow(QLabel("Saw-Like Electric Field:"), widget)
        widget.stateChanged.connect( widget.on_state_changed )
                
        #edir
        widget = InputText( group_box, input_name="edir" )
        group_box.layout.addRow(QLabel("edir:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #emaxpos
        widget = InputText( group_box, input_name="emaxpos" )
        group_box.layout.addRow(QLabel("emaxpos:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #eopreg
        widget = InputText( group_box, input_name="eopreg" )
        group_box.layout.addRow(QLabel("eopreg:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #eamp
        widget = InputText( group_box, input_name="eamp" )
        group_box.layout.addRow(QLabel("eamp:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #dipfield
        widget = InputCheck( group_box, input_name="dipfield")
        group_box.layout.addRow(QLabel("Dipole Correction:"), widget)
        widget.stateChanged.connect( widget.on_state_changed )

        #lefield
        widget = InputCheck( group_box, input_name="lefield")
        group_box.layout.addRow(QLabel("Homogeneous Electric Field:"), widget)
        widget.stateChanged.connect( widget.on_state_changed )

        #efield
        widget = InputText( group_box, input_name="efield" )
        group_box.layout.addRow(QLabel("efield:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #efield_cart(3)
        widget = InputText( group_box, input_name="efield_cart" )
        group_box.layout.addRow(QLabel("efield_cart:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #efield_phase
        widget = InputCombo( group_box, "efield_phase" )
        widget.addItem("Read", userData = "read")
        widget.addItem("Write", userData = "write")
        widget.addItem("None", userData = "none")
        group_box.layout.addRow(QLabel("efield_phase:"), widget)
        widget.currentIndexChanged.connect( widget.on_index_changed )

        #nberrycyc
        widget = InputText( group_box, input_name="nberrycyc" )
        group_box.layout.addRow(QLabel("nberrycyc:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #lorbm
        widget = InputCheck( group_box, input_name="lorbm")
        group_box.layout.addRow(QLabel("lorbm:"), widget)
        widget.stateChanged.connect( widget.on_state_changed )

        #lberry
        widget = InputCheck( group_box, input_name="lberry")
        group_box.layout.addRow(QLabel("lberry:"), widget)
        widget.stateChanged.connect( widget.on_state_changed )

        #gdir
        widget = InputCombo( group_box, "gdir" )
        widget.addItem("First Reciprocal Lattice Vector", userData = "1")
        widget.addItem("Second Reciprocal Lattice Vector", userData = "2")
        widget.addItem("Third Reciprocal Lattice Vector", userData = "3")
        group_box.layout.addRow(QLabel("gdir:"), widget)
        widget.currentIndexChanged.connect( widget.on_index_changed )

        #nppstr
        widget = InputText( group_box, input_name="nppstr" )
        group_box.layout.addRow(QLabel("nppstr:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #lfcpopt
        widget = InputCheck( group_box, input_name="lfcpopt")
        group_box.layout.addRow(QLabel("lfcpopt:"), widget)
        widget.stateChanged.connect( widget.on_state_changed )

        #fcp_mu
        widget = InputText( group_box, input_name="fcp_mu" )
        group_box.layout.addRow(QLabel("fcp_mu:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #monopole
        widget = InputCheck( group_box, input_name="monopole")
        group_box.layout.addRow(QLabel("monopole:"), widget)
        widget.stateChanged.connect( widget.on_state_changed )

        button = QPushButton('Next', self)
        button.setToolTip('Proceed to the next input set.')
        button.clicked.connect(group_box.on_click)
        group_box.layout.addRow(button)

        group_box.next_group_box = 'print'


    #--------------------------------------------------------#
    # Monopole Inputs
    #--------------------------------------------------------#
    def create_monopole_box(self,group_box):
        
        #zmon
        widget = InputText( group_box, input_name="zmon" )
        group_box.layout.addRow(QLabel("zmon:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #realxz
        widget = InputCheck( group_box, input_name="realxz")
        group_box.layout.addRow(QLabel("realxz:"), widget)
        widget.stateChanged.connect( widget.on_state_changed )

        #block
        widget = InputCheck( group_box, input_name="block")
        group_box.layout.addRow(QLabel("block:"), widget)
        widget.stateChanged.connect( widget.on_state_changed )

        #block_1
        widget = InputText( group_box, input_name="block_1" )
        group_box.layout.addRow(QLabel("block_1:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #block_2
        widget = InputText( group_box, input_name="block_2" )
        group_box.layout.addRow(QLabel("block_2:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #block_height
        widget = InputText( group_box, input_name="block_height" )
        group_box.layout.addRow(QLabel("block_height:"), widget)
        widget.textChanged.connect( widget.on_text_changed )



    #--------------------------------------------------------#
    # K-Point Inputs
    #--------------------------------------------------------#
    def create_kpoint_box(self,group_box):
        
        #nosym
        widget = InputText( group_box, input_name="nosym" )
        group_box.layout.addRow(QLabel("nosym:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #nosym_evc
        widget = InputText( group_box, input_name="nosym_evc" )
        group_box.layout.addRow(QLabel("nosym_evc:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #noinv
        widget = InputText( group_box, input_name="noinv" )
        group_box.layout.addRow(QLabel("noinv:"), widget)
        widget.textChanged.connect( widget.on_text_changed )
        


    #--------------------------------------------------------#
    # Electrons Inputs
    #--------------------------------------------------------#
    def create_electrons_box(self,group_box):
        
        #electron_maxstep
        widget = InputText( group_box, input_name="electron_maxstep" )
        group_box.layout.addRow(QLabel("electron_maxstep:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #scf_must_converge
        widget = InputCheck( group_box, input_name="scf_must_converge")
        group_box.layout.addRow(QLabel("scf_must_converge:"), widget)
        widget.stateChanged.connect( widget.on_state_changed )

        #conv_thr
        widget = InputCheck( group_box, input_name="conv_thr")
        group_box.layout.addRow(QLabel("conv_thr:"), widget)
        widget.stateChanged.connect( widget.on_state_changed )

        #adaptive_thr
        widget = InputCheck( group_box, input_name="adaptive_thr")
        group_box.layout.addRow(QLabel("adaptive_thr:"), widget)
        widget.stateChanged.connect( widget.on_state_changed )

        #conv_thr_init
        widget = InputCheck( group_box, input_name="conv_thr_init")
        group_box.layout.addRow(QLabel("conv_thr_init:"), widget)
        widget.stateChanged.connect( widget.on_state_changed )

        #conv_thr_multi
        widget = InputCheck( group_box, input_name="conv_thr_multi")
        group_box.layout.addRow(QLabel("conv_thr_multi:"), widget)
        widget.stateChanged.connect( widget.on_state_changed )

        #mixing_mode
        widget = InputCombo( group_box, "mixing_mode" )
        widget.addItem("Plain", userData = "plain")
        widget.addItem("TF", userData = "TF")
        widget.addItem("Local-TF", userData = "local_TF")
        group_box.layout.addRow(QLabel("mixing_mode:"), widget)
        widget.currentIndexChanged.connect( widget.on_index_changed )

        #mixing_beta
        widget = InputText( group_box, input_name="mixing_beta" )
        group_box.layout.addRow(QLabel("mixing_beta:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #mixing_ndim
        widget = InputText( group_box, input_name="mixing_ndim" )
        group_box.layout.addRow(QLabel("mixing_ndim:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #mixing_fixed_ns
        widget = InputText( group_box, input_name="mixing_fixed_ns" )
        group_box.layout.addRow(QLabel("mixing_fixed_ns"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #diagonalization
        widget = InputCombo( group_box, "diagonalization" )
        widget.addItem("david", userData = "david")
        widget.addItem("cg", userData = "cg")
        group_box.layout.addRow(QLabel("diagonalization:"), widget)
        widget.currentIndexChanged.connect( widget.on_index_changed )

        #diago_thr_init
        widget = InputText( group_box, input_name="diago_thr_init" )
        group_box.layout.addRow(QLabel("diago_thr_init"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #diago_cg_maxiter
        widget = InputText( group_box, input_name="diago_cg_maxiter" )
        group_box.layout.addRow(QLabel("diago_cg_maxiter"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #diago_david_ndim
        widget = InputText( group_box, input_name="diago_david_ndim" )
        group_box.layout.addRow(QLabel("diago_david_ndim"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #diago_full_acc
        widget = InputCheck( group_box, input_name="diago_full_acc")
        group_box.layout.addRow(QLabel("diago_full_acc:"), widget)
        widget.stateChanged.connect( widget.on_state_changed )

        #startingpot
        widget = InputCombo( group_box, "startingpot" )
        widget.addItem("atomic", userData = "atomic")
        widget.addItem("file", userData = "file")
        group_box.layout.addRow(QLabel("startingpot:"), widget)
        widget.currentIndexChanged.connect( widget.on_index_changed )

        #startingwfc
        widget = InputCombo( group_box, "startingwfc" )
        widget.addItem("atomic", userData = "atomic")
        widget.addItem("atomic+random", userData = "atomic+random")
        widget.addItem("random", userData = "random")
        widget.addItem("file", userData = "file")
        group_box.layout.addRow(QLabel("startingwfc:"), widget)
        widget.currentIndexChanged.connect( widget.on_index_changed )

        #tqr
        widget = InputCheck( group_box, input_name="tqr")
        group_box.layout.addRow(QLabel("tqr:"), widget)
        widget.stateChanged.connect( widget.on_state_changed )



    #--------------------------------------------------------#
    # Ions Inputs
    #--------------------------------------------------------#
    def create_ions_box(self,group_box):

        #ion_dynamics
        widget = InputCombo( group_box, "ion_dynamics" )
        widget.addItem("bfgs", userData = "bfgs")
        widget.addItem("damp", userData = "damp")
        widget.addItem("verlet", userData = "verlet")
        widget.addItem("langevin", userData = "langevin")
        widget.addItem("langevin-dmc", userData = "langevin-dmc")
        widget.addItem("bfgs", userData = "bfgs")
        widget.addItem("damp", userData = "damp")
        widget.addItem("beeman", userData = "beeman")
        group_box.layout.addRow(QLabel("ion_dynamics:"), widget)
        widget.currentIndexChanged.connect( widget.on_index_changed )

        #ion_positions
        widget = InputCombo( group_box, "ion_positions" )
        widget.addItem("default", userData = "default")
        widget.addItem("from_input", userData = "from_input")
        group_box.layout.addRow(QLabel("ion_positions:"), widget)
        widget.currentIndexChanged.connect( widget.on_index_changed )

        #pot_extrapolation
        widget = InputCombo( group_box, "pot_extrapolation" )
        widget.addItem("None", userData = "none")
        widget.addItem("Atomic", userData = "atomic")
        widget.addItem("First-Order", userData = "first_order")
        widget.addItem("Second-Order", userData = "second_order")
        group_box.layout.addRow(QLabel("pot_extrapolation:"), widget)
        widget.currentIndexChanged.connect( widget.on_index_changed )

        #wfc_extrapolation
        widget = InputCombo( group_box, "wfc_extrapolation" )
        widget.addItem("None", userData = "none")
        widget.addItem("First-Order", userData = "first_order")
        widget.addItem("Second-Order", userData = "second_order")
        group_box.layout.addRow(QLabel("wfc_extrapolation:"), widget)
        widget.currentIndexChanged.connect( widget.on_index_changed )

        #remove_rigid_rot
        widget = InputCheck( group_box, input_name="remove_rigid_rot")
        group_box.layout.addRow(QLabel("remove_rigid_rot:"), widget)
        widget.stateChanged.connect( widget.on_state_changed )

        #ion_temperature
        widget = InputCombo( group_box, "ion_temperature" )
        widget.addItem("rescaling", userData = "rescaling")
        widget.addItem("rescale-v", userData = "rescale-v")
        widget.addItem("rescale-T", userData = "rescale-T")
        widget.addItem("reduce-T", userData = "reduce-T")
        widget.addItem("berendsen", userData = "berendsen")
        widget.addItem("andersen", userData = "andersen")
        widget.addItem("initial", userData = "initial")
        widget.addItem("not_controlled", userData = "not_controlled")
        group_box.layout.addRow(QLabel("Thermostat:"), widget)
        widget.currentIndexChanged.connect( widget.on_index_changed )

        #tempw
        widget = InputText( group_box, input_name="tempw" )
        group_box.layout.addRow(QLabel("tempw:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #tolp
        widget = InputText( group_box, input_name="tolp" )
        group_box.layout.addRow(QLabel("tolp:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #delta_t
        widget = InputText( group_box, input_name="delta_t" )
        group_box.layout.addRow(QLabel("delta_t:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #nraise
        widget = InputText( group_box, input_name="nraise" )
        group_box.layout.addRow(QLabel("nraise:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #refold_pos
        widget = InputCheck( group_box, input_name="refold_pos")
        group_box.layout.addRow(QLabel("refold_pos:"), widget)
        widget.stateChanged.connect( widget.on_state_changed )

        #upscale
        widget = InputText( group_box, input_name="upscale" )
        group_box.layout.addRow(QLabel("upscale:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #bfgs_ndim
        widget = InputText( group_box, input_name="bfgs_ndim" )
        group_box.layout.addRow(QLabel("bfgs_ndim:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #trust_radius_min
        widget = InputText( group_box, input_name="trust_radius_min" )
        group_box.layout.addRow(QLabel("trust_radius_min:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #trust_radius_ini
        widget = InputText( group_box, input_name="trust_radius_ini" )
        group_box.layout.addRow(QLabel("trust_radius_ini:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #w_1
        widget = InputText( group_box, input_name="w_1" )
        group_box.layout.addRow(QLabel("w_1:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #w_2
        widget = InputText( group_box, input_name="w_2" )
        group_box.layout.addRow(QLabel("w_2:"), widget)
        widget.textChanged.connect( widget.on_text_changed )


    #--------------------------------------------------------#
    # Cell Dynamics Inputs
    #--------------------------------------------------------#
    def create_celld_box(self,group_box):

        #cell_dynamics
        widget = InputCombo( group_box, "cell_dynamics" )
        widget.addItem("none", userData = "none")
        widget.addItem("sd", userData = "sd")
        widget.addItem("damp-pr", userData = "damp-pr")
        widget.addItem("damp-w", userData = "damp-w")
        widget.addItem("bfgs", userData = "bfgs")
        widget.addItem("none", userData = "none")
        widget.addItem("pr", userData = "pr")
        widget.addItem("w", userData = "w")
        group_box.layout.addRow(QLabel("cell_dynamics:"), widget)
        widget.currentIndexChanged.connect( widget.on_index_changed )

        #press
        widget = InputText( group_box, input_name="press" )
        group_box.layout.addRow(QLabel("press:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #wmass
        widget = InputText( group_box, input_name="wmass" )
        group_box.layout.addRow(QLabel("wmass:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #cell_factor
        widget = InputText( group_box, input_name="cell_factor" )
        group_box.layout.addRow(QLabel("cell_factor:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #press_conv_thr
        widget = InputText( group_box, input_name="press_conv_thr" )
        group_box.layout.addRow(QLabel("press_conv_thr:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #cell_dofree
        widget = InputCombo( group_box, "cell_dofree" )
        widget.addItem("all", userData = "all")
        widget.addItem("x", userData = "x")
        widget.addItem("y", userData = "y")
        widget.addItem("z", userData = "z")
        widget.addItem("xy", userData = "xy")
        widget.addItem("xz", userData = "xz")
        widget.addItem("yz", userData = "yz")
        widget.addItem("xyz", userData = "xyz")
        widget.addItem("shape", userData = "shape")
        widget.addItem("volume", userData = "volume")
        widget.addItem("2Dxy", userData = "2Dxy")
        widget.addItem("2Dshape", userData = "2Dshape")
        group_box.layout.addRow(QLabel("cell_dofree:"), widget)
        widget.currentIndexChanged.connect( widget.on_index_changed )



    #--------------------------------------------------------#
    # Print Inputs
    #--------------------------------------------------------#
    def create_print_box(self,group_box):

        #iprint
        widget = InputText( group_box, input_name="iprint" )
        group_box.layout.addRow(QLabel("iprint:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #outdir
        widget = InputText( group_box, input_name="outdir" )
        group_box.layout.addRow(QLabel("Output Directory:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #wfcdir
        widget = InputText( group_box, input_name="wfcdir" )
        group_box.layout.addRow(QLabel("Scratch Directory:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #pseudo_dir
        widget = InputText( group_box, input_name="pseudo_dir" )
        group_box.layout.addRow(QLabel("Pseudopotential Directory:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #prefix
        widget = InputText( group_box, input_name="Prefix" )
        group_box.layout.addRow(QLabel("Prefix:"), widget)
        widget.textChanged.connect( widget.on_text_changed )

        #tstress
        widget = InputCheck( group_box, input_name="tstress")
        group_box.layout.addRow(QLabel("tstress:"), widget)
        widget.stateChanged.connect( widget.on_state_changed )

        #tprnfor
        widget = InputCheck( group_box, input_name="tprnfor")
        group_box.layout.addRow(QLabel("Forces:"), widget)
        widget.stateChanged.connect( widget.on_state_changed )

        #lkpoint_dir
        widget = InputText( group_box, input_name="lkpoint_dir" )
        group_box.layout.addRow(QLabel("lkpoint_dir:"), widget)
        widget.textChanged.connect( widget.on_text_changed )


        button = QPushButton('Next', self)
        button.setToolTip('Proceed to the next input set.')
        button.clicked.connect(group_box.on_click)
        group_box.layout.addRow(button)

        group_box.next_group_box = '???'






#not included:
#nat
#ntyp
#london, xdm
#ortho_para

#probably shouldn't include:
#space_group, uniqueb, origin_choice, rhombohedral

#not sure where to place:
#no_t_rev
#force_symmorphic
#use_all_frac

#one_atom_occupations

#q2sigma, ecfixed, qcutz


class InputBox(QGroupBox):
    """
    This class represents a collection of input widgets that 
    correspond to a single type of input parameter
    """
 
    def __init__(self, name):
        super(QGroupBox, self).__init__(name)
        
        self.layout = QFormLayout()

    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')

        #create the box for system information
        self.window().system_box = self.window().create_box(self.next_group_box)
        self.window().boxes_layout.addWidget(self.window().system_box)




class InputText(QLineEdit):
    """
    This class represents a text box in the GUI
    """

    def __init__(self, parent_, input_name = None):
        super(QLineEdit, self).__init__(parent = parent_)

        self.input_name = input_name

    @pyqtSlot(str)
    def on_text_changed(self, string):
        
        input_file.inputs[self.input_name] = string
        #print(input_file.inputs)







class InputCombo(QComboBox):
    """
    This class represents a drop-down box in the GUI
    """

    def __init__(self, parent_, input_name = None):
        super(QComboBox, self).__init__(parent = parent_)

        self.input_name = input_name

    @pyqtSlot(int)
    def on_index_changed(self, index):
        
        input_file.inputs[self.input_name] = index





class InputCheck(QCheckBox):
    """
    This class represents a check box in the GUI
    """

    def __init__(self, parent_, input_name = None):
        super(QCheckBox, self).__init__(parent = parent_)

        self.input_name = input_name

    @pyqtSlot(int)
    def on_state_changed(self, value):
        
        input_file.inputs[self.input_name] = value






class QuantumEspressoInputFile():
    """
    This class holds all of the information associated with a QE input file
    """
 
    def __init__(self):

        self.inputs = {}

    def set_input(self, name, value):

        self.inputs[name] = value






 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    input_file = QuantumEspressoInputFile()
    dialog = Dialog(input_file)
sys.exit(dialog.exec_())
