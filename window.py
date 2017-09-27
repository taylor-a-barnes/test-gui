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

        #max_seconds
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("Checkpoint Time (hrs):"), widget)

        #etot_conv_thr
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("Energy Convergence:"), widget)

        #force_conv_thr
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("Force Convergence:"), widget)

        #disk_io
        widget = QComboBox()
        widget.addItem('high')
        widget.addItem('medium')
        widget.addItem('low')
        widget.addItem('none')
        group_box.layout.addRow(QLabel("Disk IO:"), widget)

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
        widget = QComboBox()
        widget.addItem('Custom')
        widget.addItem('Simple Cubic')
        widget.addItem('Face-Centered Cubic')
        widget.addItem('Body-Centered Cubic')
        widget.addItem('Hexagonal and Trigonal P')
        widget.addItem('Trigonal R, 3-fold axis c')
        widget.addItem('Trigonal R, 3-fold axis <111>')
        widget.addItem('Tetragonal P')
        widget.addItem('Tetragonal I')
        widget.addItem('Orthorhombic P')
        widget.addItem('Base-Centered Orthorhombic')
        widget.addItem('Face-Centered Orthorhombic')
        widget.addItem('Body-Centered Orthorhombic')
        widget.addItem('Monoclinic P, unique axis c')
        widget.addItem('Monoclinic P, unique axis b')
        widget.addItem('Base-Centered Monoclinic')
        widget.addItem('Triclinic')
        group_box.layout.addRow(QLabel("Lattice Type"), widget)
        
        #v1
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("v1:"), widget)

        #v2
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("v2:"), widget)

        #v3
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("v3:"), widget)


        #assume_isolated
        widget = QComboBox()
        widget.addItem('none')
        widget.addItem('ESM (Effective Screening Medium)')
        widget.addItem('Makov-Payne')
        widget.addItem('Martyna-Tuckerman')
        group_box.layout.addRow(QLabel("assume_isolated:"), widget)

        #esm_bc
        widget = QComboBox()
        widget.addItem('Periodic')
        widget.addItem('Vacuum-Slab-Vacuum')
        widget.addItem('Metal-Slab-Metal')
        widget.addItem('Vacuum-Slab-Metal')
        group_box.layout.addRow(QLabel("esm_bc:"), widget)

        #esm_w
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("esm_w:"), widget)

        #esm_nfit
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("esm_nfit:"), widget)

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

        #nbnd
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("Number of Bands:"), widget)

        #tot_charge
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("Charge:"), widget)

        #tot_magnetization
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("tot_magnetization:"), widget)

        #ecutwfc
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("ecutwfc:"), widget)

        #ecutrho
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("ecutrho:"), widget)

        #nr1, nr2, and nr3
        #nr1s, nr2s, and nr3s

        #ecutfock
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("ecutfock:"), widget)

        #occupations
        widget = QComboBox()
        widget.addItem('Gaussian Smearing')
        widget.addItem('Tetrahedron (Bloechl Method)')
        widget.addItem('Tetrahedron (Linear Method)')
        widget.addItem('Tetrahedron (Kawamura Method)')
        widget.addItem('Fixed')
        widget.addItem('Custom')
        group_box.layout.addRow(QLabel("Lattice Type:"), widget)

#NOTE: for occupations, default to 'smearing', unless doing DOS or phonons, in which case use 'tetrahedra_opt' - the Kawamura Method
        
        #smearing
        widget = QComboBox()
        widget.addItem('Ordinary Gaussian')
        widget.addItem('Methfessel-Paxton')
        widget.addItem('Marzari-Vanderbilt')
        widget.addItem('Fermi-Dirac')
        group_box.layout.addRow(QLabel("Smearing Method:"), widget)
        
#NOTE: default to Marzari-Vanderbilt 'cold smearing'

        #degauss
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("degauss:"), widget)

#NOTE: degauss has suggested values of 0.06-0.10 Ry

        #nspin
        widget = QComboBox()
        widget.addItem('Non-Polarized')
        widget.addItem('Spin-Polarized')
        widget.addItem('Noncollinear Spin-Polarized')
        group_box.layout.addRow(QLabel("Spin Polarization:"), widget)

        #input_dft
        widget = QComboBox()
        widget.addItem('BLYP')
        widget.addItem('PBE')
        widget.addItem('PBE0')
        widget.addItem('HSE')
        group_box.layout.addRow(QLabel("DFT Functional:"), widget)

        #exx_fraction
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("exx_fraction:"), widget)

        #screening_parameter
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("screening_parameter:"), widget)

        #exxdiv_treatment
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("exxdiv_treatment:"), widget)

        #x_gamma_extrapolation
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("x_gamma_extrapolation:"), widget)

        #ecutvcut
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("ecutvcut:"), widget)

        #nqx1, nqx2, nqx3
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("nqx1, nqx2, nqx3:"), widget)




        
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
        group_box.layout.addRow(QLabel("DFT+U:"), QCheckBox())

#NOTE: Instead of having a checkbox, just turn DFT+U on if a non-zero U is applied to any species

        #lda_plus_u_kind
        group_box.layout.addRow(QLabel("DFT+U+J:"), QCheckBox())

#NOTE: Instead of having a checkbox, just turn DFT+U+J on if a non-zero J is applied to any species

        #U_projection_type
        widget = QComboBox()
        widget.addItem('atomic')
        widget.addItem('ortho-atomic')
        widget.addItem('norm-atomic')
        widget.addItem('file')
        widget.addItem('pseudo')
        group_box.layout.addRow(QLabel("DFT Functional:"), widget)

        #starting_ns_eigenvalue(m,ispin,l)
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("U:"), widget)

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

        #smearing
        widget = QComboBox()
        widget.addItem('None')
        widget.addItem('Grimme-D2')
        widget.addItem('Tkatchenko-Scheffler')
        widget.addItem('XDM')
        group_box.layout.addRow(QLabel("Van der Waals Correction:"), widget)

        #london_rcut
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("london_rcut:"), widget)

        #ts_vdw_econv_thr
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("ts_vdw_econv_thr:"), widget)

        #ts_vdw_isolated
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("ts_vdw_isolated:"), widget)

        #london_s6
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("london_s6:"), widget)

        #xdm_a1
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("xdm_a1:"), widget)

        #xdm_a2
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("xdm_a2:"), widget)

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
        titleLineEdit = QLineEdit()
        group_box.layout.addRow(QLabel("Timestep:"), titleLineEdit)


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
        group_box.layout.addRow(QLabel("starting_spin_angle:"), QCheckBox())

        #constrainted_magnetization
        widget = QComboBox()
        widget.addItem('none')
        widget.addItem('total')
        widget.addItem('atomic')
        widget.addItem('total_direction')
        widget.addItem('atomic_direction')
        group_box.layout.addRow(QLabel("constrained_magnetization:"), widget)

        #fixed_magnetization
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("fixed_magnetization:"), widget)

        #lambda
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("lambda:"), widget)

        #report
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("report:"), widget)



    #--------------------------------------------------------#
    # Noncollinear Inputs
    #--------------------------------------------------------#
    def create_noncollinear_box(self,group_box):

        #lspinorb
        group_box.layout.addRow(QLabel("lspinorb:"), QCheckBox())
        
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
        group_box.layout.addRow(QLabel("Saw-Like Electric Field:"), QCheckBox())
                
        #edir
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("edir:"), widget)

        #emaxpos
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("emaxpos:"), widget)

        #eopreg
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("eopreg:"), widget)

        #eamp
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("eamp:"), widget)

        #dipfield
        group_box.layout.addRow(QLabel("Dipole Correction:"), QCheckBox())

        #lefield
        group_box.layout.addRow(QLabel("Homogeneous Electric Field:"), QCheckBox())

        #efield
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("efield:"), widget)

        #efield_cart(3)
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("efield_cart:"), widget)

        #efield_phase
        widget = QComboBox()
        widget.addItem('read')
        widget.addItem('write')
        widget.addItem('none')
        group_box.layout.addRow(QLabel("efield_phase:"), widget)

        #nberrycyc
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("nberrycyc:"), widget)

        #lorbm
        group_box.layout.addRow(QLabel("lorbm:"), QCheckBox())

        #lberry
        group_box.layout.addRow(QLabel("lberry:"), QCheckBox())

        #gdir
        widget = QComboBox()
        widget.addItem('first reciprocal lattice vector')
        widget.addItem('second reciprocal lattice vector')
        widget.addItem('third reciprocal lattice vector')
        group_box.layout.addRow(QLabel("gdir:"), widget)

        #nppstr
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("nppstr:"), widget)

        #lfcpopt
        group_box.layout.addRow(QLabel("lfcpopt:"), QCheckBox())

        #fcp_mu
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("fcp_mu:"), widget)

        #monopole
        group_box.layout.addRow(QLabel("monopole:"), QCheckBox())

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
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("zmon:"), widget)

        #realxz
        group_box.layout.addRow(QLabel("realxz:"), QCheckBox())

        #block
        group_box.layout.addRow(QLabel("block:"), QCheckBox())

        #block_1
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("block_1:"), widget)

        #block_2
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("block_2:"), widget)

        #block_height
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("block_height:"), widget)



    #--------------------------------------------------------#
    # K-Point Inputs
    #--------------------------------------------------------#
    def create_kpoint_box(self,group_box):
        
        #nosym
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("nosym:"), widget)

        #nosym_evc
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("nosym_evc:"), widget)

        #noinv
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("noinv:"), widget)
        


    #--------------------------------------------------------#
    # Electrons Inputs
    #--------------------------------------------------------#
    def create_electrons_box(self,group_box):
        
        #electron_maxstep
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("electron_maxstep:"), widget)

        #scf_must_converge
        group_box.layout.addRow(QLabel("scf_must_converge:"), QCheckBox())

        #conv_thr
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("conv_thr:"), widget)

        #adaptive_thr
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("adaptive_thr:"), widget)

        #conv_thr_init
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("conv_thr_init:"), widget)

        #conv_thr_multi
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("conv_thr_multi:"), widget)

        #mixing_mode
        widget = QComboBox()
        widget.addItem('plain')
        widget.addItem('TF')
        widget.addItem('local-TF')
        group_box.layout.addRow(QLabel("mixing_mode:"), widget)

        #mixing_beta
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("mixing_beta:"), widget)

        #mixing_ndim
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("mixing_ndim:"), widget)

        #mixing_fixing_ns
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("mixing_fixing_ns:"), widget)

        #diagonalization
        widget = QComboBox()
        widget.addItem('david')
        widget.addItem('cg')
        group_box.layout.addRow(QLabel("Diagonalization:"), widget)

        #diago_thr_init
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("diago_thr_init:"), widget)

        #diago_cg_maxiter
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("diago_cg_maxiter:"), widget)

        #diago_david_ndim
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("diago_david_ndim:"), widget)

        #diago_full_acc
        group_box.layout.addRow(QLabel("diago_full_acc:"), QCheckBox())

        #startingpot
        widget = QComboBox()
        widget.addItem('atomic')
        widget.addItem('file')
        group_box.layout.addRow(QLabel("startingpot:"), widget)

        #startingwfc
        widget = QComboBox()
        widget.addItem('atomic')
        widget.addItem('atomic+random')
        widget.addItem('random')
        widget.addItem('file')
        group_box.layout.addRow(QLabel("startingwfc:"), widget)

        #tqr
        group_box.layout.addRow(QLabel("tqr:"), QCheckBox())



    #--------------------------------------------------------#
    # Ions Inputs
    #--------------------------------------------------------#
    def create_ions_box(self,group_box):

        #mixing_mode
        widget = QComboBox()
        widget.addItem('bfgs')
        widget.addItem('damp')
        widget.addItem('verlet')
        widget.addItem('langevin')
        widget.addItem('langevin-dmc')
        widget.addItem('bfgs')
        widget.addItem('damp')
        widget.addItem('beeman')
        group_box.layout.addRow(QLabel("ion_dynamics:"), widget)

        #ion_positions
        widget = QComboBox()
        widget.addItem('default')
        widget.addItem('from_input')
        group_box.layout.addRow(QLabel("ion_positions:"), widget)

        #pot_extrapolation
        widget = QComboBox()
        widget.addItem('none')
        widget.addItem('atomic')
        widget.addItem('first_order')
        widget.addItem('second_order')
        group_box.layout.addRow(QLabel("pot_extrapolation:"), widget)

        #wfc_extrapolation
        widget = QComboBox()
        widget.addItem('none')
        widget.addItem('first_order')
        widget.addItem('second_order')
        group_box.layout.addRow(QLabel("pot_extrapolation:"), widget)

        #remove_rigid_rot
        group_box.layout.addRow(QLabel("remove_rigid_rot:"), QCheckBox())

        #thermostat
        widget = QComboBox()
        widget.addItem('rescaling')
        widget.addItem('rescale-v')
        widget.addItem('rescale-T')
        widget.addItem('reduce-T')
        widget.addItem('berendsen')
        widget.addItem('andersen')
        widget.addItem('initial')
        widget.addItem('not_controlled')
        group_box.layout.addRow(QLabel("ion_temperature:"), widget)

        #tempw
        titleLineEdit = QLineEdit()
        group_box.layout.addRow(QLabel("tempw:"), titleLineEdit)

        #tolp
        titleLineEdit = QLineEdit()
        group_box.layout.addRow(QLabel("tolp:"), titleLineEdit)

        #delta_t
        titleLineEdit = QLineEdit()
        group_box.layout.addRow(QLabel("delta_t:"), titleLineEdit)

        #nraise
        titleLineEdit = QLineEdit()
        group_box.layout.addRow(QLabel("nraise:"), titleLineEdit)

        #refold_pos
        group_box.layout.addRow(QLabel("refold_pos:"), QCheckBox())

        #upscale
        titleLineEdit = QLineEdit()
        group_box.layout.addRow(QLabel("upscale:"), titleLineEdit)

        #bfgs_ndim
        titleLineEdit = QLineEdit()
        group_box.layout.addRow(QLabel("bfgs_ndim:"), titleLineEdit)

        #trust_radius_min
        titleLineEdit = QLineEdit()
        group_box.layout.addRow(QLabel("trust_radius_min:"), titleLineEdit)

        #trust_radius_ini
        titleLineEdit = QLineEdit()
        group_box.layout.addRow(QLabel("trust_radius_ini:"), titleLineEdit)

        #w_1
        titleLineEdit = QLineEdit()
        group_box.layout.addRow(QLabel("w_1:"), titleLineEdit)

        #w_2
        titleLineEdit = QLineEdit()
        group_box.layout.addRow(QLabel("w_2:"), titleLineEdit)


    #--------------------------------------------------------#
    # Cell Dynamics Inputs
    #--------------------------------------------------------#
    def create_celld_box(self,group_box):

        #thermostat
        widget = QComboBox()
        widget.addItem('none')
        widget.addItem('sd')
        widget.addItem('damp-pr')
        widget.addItem('damp-w')
        widget.addItem('bfgs')
        widget.addItem('none')
        widget.addItem('pr')
        widget.addItem('w')
        group_box.layout.addRow(QLabel("ion_temperature:"), widget)

        #press
        titleLineEdit = QLineEdit()
        group_box.layout.addRow(QLabel("press:"), titleLineEdit)

        #wmass
        titleLineEdit = QLineEdit()
        group_box.layout.addRow(QLabel("wmass:"), titleLineEdit)

        #cell_factor
        titleLineEdit = QLineEdit()
        group_box.layout.addRow(QLabel("cell_factor:"), titleLineEdit)

        #press_conv_thr
        titleLineEdit = QLineEdit()
        group_box.layout.addRow(QLabel("press_conv_thr:"), titleLineEdit)

        #cell_dofree
        widget = QComboBox()
        widget.addItem('all')
        widget.addItem('x')
        widget.addItem('y')
        widget.addItem('z')
        widget.addItem('xy')
        widget.addItem('xz')
        widget.addItem('yz')
        widget.addItem('xyz')
        widget.addItem('shape')
        widget.addItem('volume')
        widget.addItem('2Dxy')
        widget.addItem('2Dshape')
        group_box.layout.addRow(QLabel("cell_dofree:"), widget)



    #--------------------------------------------------------#
    # Print Inputs
    #--------------------------------------------------------#
    def create_print_box(self,group_box):

        #iprint
        titleLineEdit = QLineEdit()
        group_box.layout.addRow(QLabel("iprint:"), titleLineEdit)

        #outdir
        titleLineEdit = QLineEdit()
        group_box.layout.addRow(QLabel("Output Directory:"), titleLineEdit)

        #wfcdir
        titleLineEdit = QLineEdit()
        group_box.layout.addRow(QLabel("Scratch Directory:"), titleLineEdit)

        #pseudo_dir
        titleLineEdit = QLineEdit()
        group_box.layout.addRow(QLabel("Pseudopotential Directory:"), titleLineEdit)

        #prefix
        titleLineEdit = QLineEdit()
        group_box.layout.addRow(QLabel("Prefix:"), titleLineEdit)

        #tstress
        group_box.layout.addRow(QLabel("Stress:"), QCheckBox())

        #tprnfor
        group_box.layout.addRow(QLabel("Forces:"), QCheckBox())

        #lkpoint_dir
        widget = QLineEdit()
        group_box.layout.addRow(QLabel("lkpoint_dir:"), widget)


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

    def __init__(self, parent_, input_name = None):
        super(QLineEdit, self).__init__(parent = parent_)

        self.input_name = input_name

    @pyqtSlot(str)
    def on_text_changed(self, string):
        
        input_file.inputs[self.input_name] = string
        #print(input_file.inputs)







class QuantumEspressoInputFile():
 
    def __init__(self):

        self.inputs = {}

    def set_input(self, name, value):

        self.inputs[name] = value






 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    input_file = QuantumEspressoInputFile()
    dialog = Dialog(input_file)
sys.exit(dialog.exec_())
