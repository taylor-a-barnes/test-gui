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

        #list of all associated group boxes
        self.group_boxes = []

        #inside of the main layout is a scroll area
        self.scroll_area = QScrollArea(self.central_widget)
        self.scroll_area.setWidgetResizable(True)
        self.main_layout.addWidget(self.scroll_area)

        #inside of the scroll area is another widget that will contain everything else
        self.boxes_widget = QWidget()
        self.boxes_layout = QVBoxLayout(self.boxes_widget)

        #create the box for basic information
        basic_box = self.create_box('basic')
        self.boxes_layout.addWidget(basic_box)


        self.scroll_area.setWidget(self.boxes_widget)
        self.setLayout(self.main_layout)

        #set the dimensions of the form
#        self.setGeometry(10,10,500,500)
 

    def create_box(self,group_name):

        group_box = InputBox(group_name)

        group_box.initialize_widgets()

        group_box.setLayout(group_box.layout)
        
        self.group_boxes.append(group_box)

        return group_box

    def on_window_update(self):

        print("Window Updating")

        for group_box in self.group_boxes:
            group_box.update_layout()






#not included:
#nat
#ntyp
#london, xdm
#ortho_para

#probably shouldn't include:
#title
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
 
    def __init__(self, group_name):
        self.group_name = group_name
        self.label = self.group_name + " Information"

        super(QGroupBox, self).__init__(self.label)
        
        self.layout = QFormLayout()



        #self.layout.setSpacing(0)


        self.widgets = []

        self.input_file = input_file

        #conditions under which this group box should be shown
        self.show_conditions = []


    def initialize_widgets(self):
        """
        Add GUI elements for each of the input parameters associated with self.group_name
        """

        #for w in self.widgets:
        #    self.layout.removeWidget(w)

        #reset any widgets
        #NOTE: need to check whether this clears memory correctly
        #self.widgets = []
        
        #self.layout = QFormLayout()

        #start with a fresh layout
#        self.clear_layout()

        print("start of initialize_widgets")
        print(self.window())
        
        if self.group_name == 'basic':
            self.create_basic_box()
        elif self.group_name == 'cell':
            self.create_cell_box()
        elif self.group_name == 'hubbard':
            self.create_hubbard_box()
        elif self.group_name == 'system':
            self.create_system_box()
        elif self.group_name == 'vdw':
            self.create_vdw_box()
        elif self.group_name == 'md':
            self.create_md_box()
        elif self.group_name == 'magnetization':
            self.create_magnetization_box()
        elif self.group_name == 'noncollinear':
            self.create_noncollinear_box()
        elif self.group_name == 'efield':
            self.create_efield_box()
        elif self.group_name == 'monopole':
            self.create_monopole_box()
        elif self.group_name == 'kpoint':
            self.create_kpoint_box()
        elif self.group_name == 'electrons':
            self.create_electrons_box()
        elif self.group_name == 'ions':
            self.create_ions_box()
        elif self.group_name == 'cell dynamics':
            self.create_celld_box()
        elif self.group_name == 'print':
            self.create_print_box()
        else:
            raise LookupError('Group name not recognized: ' + str(self.group_name))

        self.apply_layout()
        self.update_layout()

        print("end of initialize_widgets")
        print(self.window())

    def apply_layout(self):
        for w in self.widgets:

            try:
                if w.label:
                    self.layout.addRow( w.label, w.widget )
                else:
                    self.layout.addRow( w.widget )
                print("HERE")

            except AttributeError: #legacy code - delete when possible
                try: #check if the widget has a label
                    self.layout.addRow( w.label, w)
                except AttributeError:
                    self.layout.addRow( w )

            w.shown = True

    def clear_layout(self):
        """
        Remove all objects from layout
        """

        for i in reversed( range( self.layout.count() ) ):
            w = self.layout.itemAt(i).widget()
            self.layout.removeWidget( w )
            #w.setParent( None )
            w.deleteLater()

        self.widgets = []

    def update_layout(self):
        
        for w in self.widgets:

            should_show = self.check_show_conditions(w)

            if should_show and not w.shown:
                w.set_visible(True)

            elif not should_show and w.shown:
                w.set_visible(False)

    def check_show_conditions(self, widget):

        show = True

        for condition in widget.show_conditions:
            if self.evaluate_condition(condition) == False:
                show = False

        return show

    def evaluate_condition(self, condition):
        
        try:
        
            #evaluate this condition
            try:
                input = input_file.inputs[ condition[0] ]
            except KeyError:
                input = None

            if input == condition[2]:
                return True
            else:
                return False

        except TypeError: #the condition must be a list of conditions
            
            #evaluate each condition in the list
            c1 = self.evaluate_condition(condition[0])
            c2 = self.evaluate_condition(condition[2])
            
            if condition[1] == "or":
                #print("HERE: " + str(c1) + " " + str(c2) + " " + str(c1 or c2))
                return (c1 or c2)

            elif condition[1] == "and":
                return (c1 and c2)

    def create_basic_box(self):
        group_box = self

        #title
#        widget = InputText( group_box, input_name="title" )
#        widget.label = QLabel("Title:")
#        widget.setToolTip('Enter a title for the calculation.\nThis has no impact on the results.')
#        widget.textChanged.connect( widget.on_text_changed )
#        self.widgets.append(widget)

        #calculation
        widget = InputField( group_box, "combo", label_name = "Calculation:", input_name = "calculation")
        widget.add_combo_choice( "SCF (Self-Consistent Field)", "scf" )
        widget.add_combo_choice( "NSCF (Non-Self-Consistent Field)", "nscf" ) #replace with maximum_iterations?
        widget.add_combo_choice( "Bands", "bands" ) #how is this different from NSCF?
        widget.add_combo_choice( "Geometry Relaxation", "relax" ) #note: includes vc-relax
        widget.add_combo_choice( "Molecular Dynamics", "md" ) #note: includes vc-md

        #tot_charge
        widget = InputField( group_box, "text", label_name = "Charge:", input_name = "tot_charge")

        #ecutwfc
        widget = InputField( group_box, "text", label_name = "ecutwfc:", input_name = "ecutwfc")

        #GUI_exx_corr (custom)
        widget = InputField( group_box, "combo", label_name = "Exchange Correction:", input_name = "GUI_exx_corr")
        widget.add_combo_choice( "None", "none" )
        widget.add_combo_choice( "DFT+U", "dft+u" )
        widget.add_combo_choice( "DFT+U+J", "dft+u+j" )
        widget.add_combo_choice( "Hybrid Functional", "hybrid" )

        #vdw_corr
        widget = InputField( group_box, "combo", label_name = "Van der Waals Correction:", input_name = "vdw_corr")
        widget.add_combo_choice( "None", "none" )
        widget.add_combo_choice( "Grimme-D2", "grimme-d2" )
        widget.add_combo_choice( "Tkatchenko-Scheffler", "tkatchenko-scheffler" )
        widget.add_combo_choice( "XDM", "xdm" )

        widget = InputField( group_box, "button", input_name = "Next")

        group_box.next_group_box = 'cell'

    #--------------------------------------------------------#
    # Cell Inputs
    #--------------------------------------------------------#
    def create_cell_box(self):
        group_box = self

        #ibrav
        widget = InputField( group_box, "combo", label_name = "Lattice Type:", input_name = "ibrav")
        widget.add_combo_choice( "Custom", "0" )
        widget.add_combo_choice( "Simple Cubic", "1" )
        widget.add_combo_choice( "Face-Centered Cubic", "2" )
        widget.add_combo_choice( "Body-Centered Cubic", "3" )
        widget.add_combo_choice( "Hexagonal and Trigonal P", "4" )
        widget.add_combo_choice( "Trigonal R, 3-fold axis c", "5" )
        widget.add_combo_choice( "Trigonal R, 3-fold axis <111>", "-5" )
        widget.add_combo_choice( "Tetragonal P", "6" )
        widget.add_combo_choice( "Tetragonal I", "7" )
        widget.add_combo_choice( "Orthorhombic P", "8" )
        widget.add_combo_choice( "Base-Centered Orthorhombic", "9" )
        widget.add_combo_choice( "Face-Centered Orthorhombic", "10" )
        widget.add_combo_choice( "Body-Centered Orthorhombic", "11" )
        widget.add_combo_choice( "Monoclinic P, unique axis c", "12" )
        widget.add_combo_choice( "Monoclinic P, unique axis b", "-12" )
        widget.add_combo_choice( "Base-Centered Monoclinic", "13" )
        widget.add_combo_choice( "Triclinic", "14" )
        
        #v1
        widget = InputField( group_box, "text", label_name = "v1:", input_name = "v1")

        #v2
        widget = InputField( group_box, "text", label_name = "v2:", input_name = "v2")

        #v3
        widget = InputField( group_box, "text", label_name = "v3:", input_name = "v3")

        #assume_isolated
        widget = InputField( group_box, "combo", label_name = "Cell Periodicity:", input_name = "assume_isolated")
        widget.add_combo_choice( "Periodic", "none" )
        widget.add_combo_choice( "ESM (Effective Screening Medium)", "esm" )
        widget.add_combo_choice( "Vacuum (Makov-Payne Method)", "makov-payne" )
        widget.add_combo_choice( "Vacuum (Martyna-Tuckerman Method)", "martyna-tuckerman" )

        #esm_bc
        widget = InputField( group_box, "combo", label_name = "ESM Boundary Conditions:", input_name = "esm_bc")
        widget.add_combo_choice( "Periodic", "pbc" )
        widget.add_combo_choice( "Vacuum-Slab-Vacuum", "bc1" )
        widget.add_combo_choice( "Metal-Slab-Metal", "bc2" )
        widget.add_combo_choice( "Vacuum-Slab-Metal", "bc3" )
        widget.show_conditions.append( ["assume_isolated","==","esm"] )

        #esm_w
        widget = InputField( group_box, "text", label_name = "Effective Screening Region Offset:", input_name = "esm_w")
        widget.show_conditions.append( ["assume_isolated","==","esm"] )

        #esm_efield
        widget = InputField( group_box, "text", label_name = "ESM Electric Field (Ry/a.u.):", input_name = "esm_efield")
        widget.show_conditions.append( ["assume_isolated","==","esm"] )
        widget.show_conditions.append( ["esm_bc","==","bc2"] )

        #esm_nfit
        widget = InputField( group_box, "text", label_name = "Number of ESM Grid Points:", input_name = "esm_nfit")
        widget.show_conditions.append( ["assume_isolated","==","esm"] )

        widget = InputField( group_box, "button", input_name = "Next")

        group_box.next_group_box = 'system'


        


    #--------------------------------------------------------#
    # System Inputs
    #--------------------------------------------------------#
    def create_system_box(self):
        group_box = self

        #input_dft
        widget = InputCombo( group_box, "input_dft" )
        widget.addItem("BLYP", userData = "blyp")
        widget.addItem("PBE", userData = "pbe")
        widget.addItem("PBE0", userData = "pbe0")
        widget.addItem("HSE", userData = "hse")
        widget.label = QLabel("DFT Functional:")
        widget.currentIndexChanged.connect( widget.on_index_changed )
        widget.show_conditions.append( ["GUI_exx_corr","==","hybrid"] )
        self.widgets.append(widget)

        #etot_conv_thr
        widget = InputText( group_box, input_name="etot_conv_thr" )
        widget.label = QLabel("Energy Convergence:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #forc_conv_thr
        widget = InputText( group_box, input_name="forc_conv_thr" )
        widget.label = QLabel("Force Convergence:")
        widget.textChanged.connect( widget.on_text_changed )
        widget.show_conditions.append( ["calculation","==","relax"] )
        self.widgets.append(widget)

        #nstep
        widget = InputText( group_box, input_name="nstep" )
        widget.label = QLabel("Maximum Relaxation Steps:")
        widget.textChanged.connect( widget.on_text_changed )
        widget.show_conditions.append( ["calculation","==","relax"] )
        self.widgets.append(widget)

        #nstep
        widget = InputText( group_box, input_name="nstep" )
        widget.label = QLabel("Number of Timesteps:")
        widget.textChanged.connect( widget.on_text_changed )
        #widget.show_conditions.append( [ ["calculation","==","relax"], "or", ["calculation","==","md"] ] )
        widget.show_conditions.append( ["calculation","==","md"] )
        self.widgets.append(widget)

        #nbnd
        widget = InputText( group_box, input_name="nbnd" )
        widget.label = QLabel("Number of Bands:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #tot_magnetization
        widget = InputText( group_box, input_name="tot_magnetization" )
        widget.label = QLabel("tot_magnetization:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #ecutrho
        widget = InputText( group_box, input_name="ecutrho" )
        widget.label = QLabel("ecutrho:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #nr1, nr2, and nr3
        #nr1s, nr2s, and nr3s

        #occupations
        widget = InputCombo( group_box, "occupations" )
        widget.addItem("Gaussian Smearing", userData = "smearing")
        widget.addItem("Tetrahedron (Bloechl Method)", userData = "tetrahedra")
        widget.addItem("Tetrahedron (Linear Method)", userData = "tetrahedra_lin")
        widget.addItem("Tetrahedron (Kawamura Method)", userData = "tetrahedra_opt")
        widget.addItem("Fixed", userData = "fixed")
        widget.addItem("Custom", userData = "from_input")
        widget.label = QLabel("occupations:")
        widget.currentIndexChanged.connect( widget.on_index_changed )
        self.widgets.append(widget)

#NOTE: for occupations, default to 'smearing', unless doing DOS or phonons, in which case use 'tetrahedra_opt' - the Kawamura Method
        
        #smearing
        widget = InputCombo( group_box, "smearing" )
        widget.addItem("Ordinary Gaussian", userData = "gaussian")
        widget.addItem("Methfessel-Paxton", userData = "methfessel-paxton")
        widget.addItem("Marzari-Vanderbilt", userData = "marzari-vanderbilt")
        widget.addItem("Fermi-Dirac", userData = "Fermi-Dirac")
        widget.label = QLabel("Smearing Method:")
        widget.currentIndexChanged.connect( widget.on_index_changed )
        self.widgets.append(widget)
        
#NOTE: default to Marzari-Vanderbilt 'cold smearing'

        #degauss
        widget = InputText( group_box, input_name="degauss" )
        widget.label = QLabel("degauss:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

#NOTE: degauss has suggested values of 0.06-0.10 Ry

        #nspin
        widget = InputCombo( group_box, "nspin" )
        widget.addItem("Non-Polarized", userData = "1")
        widget.addItem("Spin-Polarized", userData = "2")
        widget.addItem("Noncollinear Spin-Polarized", userData = "4")
        widget.label = QLabel("Spin Polarization:")
        widget.currentIndexChanged.connect( widget.on_index_changed )
        self.widgets.append(widget)

        #exx_fraction
        widget = InputText( group_box, input_name="exx_fraction" )
        widget.label = QLabel("exx_fraction:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #ecutfock
        widget = InputText( group_box, input_name="ecutfock" )
        widget.label = QLabel("ecutfock:")
        widget.textChanged.connect( widget.on_text_changed )
        widget.show_conditions.append( ["GUI_exx_corr","==","hybrid"] )
        self.widgets.append(widget)

        #screening_parameter
        widget = InputText( group_box, input_name="screening_parameter" )
        widget.label = QLabel("screening_parameter:")
        widget.textChanged.connect( widget.on_text_changed )
        widget.show_conditions.append( ["GUI_exx_corr","==","hybrid"] )
        self.widgets.append(widget)

        #exxdiv_treatment
        widget = InputText( group_box, input_name="exxdiv_treatment" )
        widget.label = QLabel("exxdiv_treatment:")
        widget.textChanged.connect( widget.on_text_changed )
        widget.show_conditions.append( ["GUI_exx_corr","==","hybrid"] )
        self.widgets.append(widget)

        #x_gamma_extrapolation
        widget = InputText( group_box, input_name="x_gamma_extrapolation" )
        widget.label = QLabel("x_gamma_extrapolation:")
        widget.textChanged.connect( widget.on_text_changed )
        widget.show_conditions.append( ["GUI_exx_corr","==","hybrid"] )
        self.widgets.append(widget)

        #ecutvcut
        widget = InputText( group_box, input_name="ecutvcut" )
        widget.label = QLabel("ecutvcut:")
        widget.textChanged.connect( widget.on_text_changed )
        widget.show_conditions.append( ["GUI_exx_corr","==","hybrid"] )
        self.widgets.append(widget)

        #nqx1, nqx2, nqx3
        widget = InputText( group_box, input_name="nqx1" )
        widget.label = QLabel("nqx1, nqx2, nqx3:")
        widget.textChanged.connect( widget.on_text_changed )
        widget.show_conditions.append( ["GUI_exx_corr","==","hybrid"] )
        self.widgets.append(widget)




        



        button = InputButton(self, 'Next')
        button.setToolTip('Proceed to the next input set.')
        button.clicked.connect(group_box.on_click)
        self.widgets.append(button)

        group_box.next_group_box = 'hubbard'


    #--------------------------------------------------------#
    # Hubbard Inputs
    #--------------------------------------------------------#
    def create_hubbard_box(self):
        group_box = self

        #lda_plus_u
        widget = InputCheck( group_box, input_name="lda_plus_u")
        widget.label = QLabel("DFT+U:")
        widget.stateChanged.connect( widget.on_state_changed )
        self.widgets.append(widget)

#NOTE: Instead of having a checkbox, just turn DFT+U on if a non-zero U is applied to any species

        #lda_plus_u_kind
        widget = InputCheck( group_box, input_name="lda_plus_u_kind")
        widget.label = QLabel("DFT+U+J:")
        widget.stateChanged.connect( widget.on_state_changed )
        self.widgets.append(widget)

#NOTE: Instead of having a checkbox, just turn DFT+U+J on if a non-zero J is applied to any species

        #U_projection_type
        widget = InputCombo( group_box, "U_projection_type" )
        widget.addItem("Atomic", userData = "atomic")
        widget.addItem("Ortho-Atomic", userData = "ortho-atomic")
        widget.addItem("Norm-Atomic", userData = "norm-atomic")
        widget.addItem("File", userData = "file")
        widget.addItem("Pseudo", userData = "pseudo")
        widget.label = QLabel("U Projection Type:")
        widget.currentIndexChanged.connect( widget.on_index_changed )
        self.widgets.append(widget)

        #starting_ns_eigenvalue(m,ispin,l)
        widget = InputCheck( group_box, input_name="starting_ns_eigenvalue")
        widget.label = QLabel("starting_ns_eigenvalue:")
        widget.stateChanged.connect( widget.on_state_changed )
        self.widgets.append(widget)

        #--------------------------------------------------------#
        # Per-species information
        #--------------------------------------------------------#

        #Hubbard_U
        widget = InputCheck( group_box, input_name="U")
        widget.label = QLabel("U:")
        widget.stateChanged.connect( widget.on_state_changed )
        self.widgets.append(widget)

        #Hubbard_J0
        widget = InputCheck( group_box, input_name="J0")
        widget.label = QLabel("J0:")
        widget.stateChanged.connect( widget.on_state_changed )
        self.widgets.append(widget)

        #Hubbard_alpha
        widget = InputCheck( group_box, input_name="alpha")
        widget.label = QLabel("alpha:")
        widget.stateChanged.connect( widget.on_state_changed )
        self.widgets.append(widget)

        #Hubbard_beta
        widget = InputCheck( group_box, input_name="beta")
        widget.label = QLabel("beta:")
        widget.stateChanged.connect( widget.on_state_changed )
        self.widgets.append(widget)

        #Hubbard_J
        widget = InputCheck( group_box, input_name="J")
        widget.label = QLabel("J:")
        widget.stateChanged.connect( widget.on_state_changed )
        self.widgets.append(widget)

        button = InputButton(self, 'Next')
        button.setToolTip('Proceed to the next input set.')
        button.clicked.connect(group_box.on_click)
        self.widgets.append(button)


        group_box.next_group_box = 'vdw'




    #--------------------------------------------------------#
    # VdW Inputs
    #--------------------------------------------------------#
    def create_vdw_box(self):
        group_box = self

        #london_rcut
        widget = InputText( group_box, input_name="london_rcut" )
        widget.label = QLabel("london_rcut:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #ts_vdw_econv_thr
        widget = InputText( group_box, input_name="ts_vdw_econv_thr" )
        widget.label = QLabel("ts_vdw_econv_thr:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #ts_vdw_isolated
        widget = InputText( group_box, input_name="ts_vdw_isolated" )
        widget.label = QLabel("ts_vdw_isolated:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #london_s6
        widget = InputText( group_box, input_name="london_s6" )
        widget.label = QLabel("london_s6:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #xdm_a1
        widget = InputText( group_box, input_name="xdm_a1" )
        widget.label = QLabel("xdm_a1:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #xdm_a2
        widget = InputText( group_box, input_name="xdm_a2" )
        widget.label = QLabel("xdm_a2:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #--------------------------------------------------------#
        # Per-species information
        #--------------------------------------------------------#

        #london_c6
        widget = InputText( group_box, input_name="london_c6" )
        widget.label = QLabel("london_c6:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #london_rvdw
        widget = InputText( group_box, input_name="london_rvdw" )
        widget.label = QLabel("london_rvdw:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)


        button = InputButton(self, 'Next')
        button.setToolTip('Proceed to the next input set.')
        button.clicked.connect(group_box.on_click)
        self.widgets.append(button)


        group_box.next_group_box = 'md'



    #--------------------------------------------------------#
    # MD Inputs
    #--------------------------------------------------------#
    def create_md_box(self):
        group_box = self

        #dt
        widget = InputText( group_box, input_name="dt" )
        widget.label = QLabel("dt:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        button = InputButton(self, 'Next')
        button.setToolTip('Proceed to the next input set.')
        button.clicked.connect(group_box.on_click)
        self.widgets.append(button)

        group_box.next_group_box = 'magnetization'




    #--------------------------------------------------------#
    # Magnetization Inputs
    #--------------------------------------------------------#
    def create_magnetization_box(self):
        group_box = self

        #starting_spin_angle
        widget = InputCheck( group_box, input_name="starting_spin_angle")
        widget.label = QLabel("starting_spin_angle:")
        widget.stateChanged.connect( widget.on_state_changed )
        self.widgets.append(widget)

        #constrainted_magnetization
        widget = InputCombo( group_box, "constrained_magnetization" )
        widget.addItem("None", userData = "none")
        widget.addItem("Total", userData = "total")
        widget.addItem("Atomic", userData = "atomic")
        widget.addItem("Total Direction", userData = "total_direction")
        widget.addItem("Atomic Direction", userData = "atomic_direction") 
        widget.label = QLabel("constrained_magnetization:")
        widget.currentIndexChanged.connect( widget.on_index_changed )
        self.widgets.append(widget)

        #fixed_magnetization
        widget = InputText( group_box, input_name="fixed_magnetization" )
        widget.label = QLabel("fixed_magnetization:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #lambda
        widget = InputText( group_box, input_name="lambda" )
        widget.label = QLabel("lambda:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #report
        widget = InputText( group_box, input_name="report" )
        widget.label = QLabel("report:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #--------------------------------------------------------#
        # Per-species information
        #--------------------------------------------------------#

        #starting_magnetization
        widget = InputText( group_box, input_name="starting_magnetization" )
        widget.label = QLabel("starting_magnetization:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        button = InputButton(self, 'Next')
        button.setToolTip('Proceed to the next input set.')
        button.clicked.connect(group_box.on_click)
        self.widgets.append(button)

        group_box.next_group_box = 'noncollinear'



    #--------------------------------------------------------#
    # Noncollinear Inputs
    #--------------------------------------------------------#
    def create_noncollinear_box(self):
        group_box = self

        #lspinorb
        widget = InputCheck( group_box, input_name="lspinorb")
        widget.label = QLabel("lspinorb:")
        widget.stateChanged.connect( widget.on_state_changed )
        self.widgets.append(widget)
        
        #--------------------------------------------------------#
        # Per-species information
        #--------------------------------------------------------#

        #angle1
        widget = InputCheck( group_box, input_name="angle1")
        widget.label = QLabel("angle1:")
        widget.stateChanged.connect( widget.on_state_changed )
        self.widgets.append(widget)

        #angle2
        widget = InputCheck( group_box, input_name="angle2")
        widget.label = QLabel("angle2:")
        widget.stateChanged.connect( widget.on_state_changed )
        self.widgets.append(widget)

        button = InputButton(self, 'Next')
        button.setToolTip('Proceed to the next input set.')
        button.clicked.connect(group_box.on_click)
        self.widgets.append(button)

        group_box.next_group_box = 'efield'



    #--------------------------------------------------------#
    # Electric Field Inputs
    #--------------------------------------------------------#
    def create_efield_box(self):
        group_box = self

        #tefield
        widget = InputCheck( group_box, input_name="tefield")
        widget.label = QLabel("Saw-Like Electric Field:")
        widget.stateChanged.connect( widget.on_state_changed )
        self.widgets.append(widget)
                
        #edir
        widget = InputText( group_box, input_name="edir" )
        widget.label = QLabel("edir:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #emaxpos
        widget = InputText( group_box, input_name="emaxpos" )
        widget.label = QLabel("emaxpos:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #eopreg
        widget = InputText( group_box, input_name="eopreg" )
        widget.label = QLabel("eopreg:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #eamp
        widget = InputText( group_box, input_name="eamp" )
        widget.label = QLabel("eamp:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #dipfield
        widget = InputCheck( group_box, input_name="dipfield")
        widget.label = QLabel("Dipole Correction:")
        widget.stateChanged.connect( widget.on_state_changed )
        self.widgets.append(widget)

        #lefield
        widget = InputCheck( group_box, input_name="lefield")
        widget.label = QLabel("Homegeneous Electric Field:")
        widget.stateChanged.connect( widget.on_state_changed )
        self.widgets.append(widget)

        #efield
        widget = InputText( group_box, input_name="efield" )
        widget.label = QLabel("efield:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #efield_cart(3)
        widget = InputText( group_box, input_name="efield_cart" )
        widget.label = QLabel("efield_cart:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #efield_phase
        widget = InputCombo( group_box, "efield_phase" )
        widget.addItem("Read", userData = "read")
        widget.addItem("Write", userData = "write")
        widget.addItem("None", userData = "none")
        widget.label = QLabel("efield_phase:")
        widget.currentIndexChanged.connect( widget.on_index_changed )
        self.widgets.append(widget)

        #nberrycyc
        widget = InputText( group_box, input_name="nberrycyc" )
        widget.label = QLabel("nberrycyc:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #lorbm
        widget = InputCheck( group_box, input_name="lorbm")
        widget.label = QLabel("lorbm:")
        widget.stateChanged.connect( widget.on_state_changed )
        self.widgets.append(widget)

        #lberry
        widget = InputCheck( group_box, input_name="lberry")
        widget.label = QLabel("lberry:")
        widget.stateChanged.connect( widget.on_state_changed )
        self.widgets.append(widget)

        #gdir
        widget = InputCombo( group_box, "gdir" )
        widget.addItem("First Reciprocal Lattice Vector", userData = "1")
        widget.addItem("Second Reciprocal Lattice Vector", userData = "2")
        widget.addItem("Third Reciprocal Lattice Vector", userData = "3")
        widget.label = QLabel("gdir:")
        widget.currentIndexChanged.connect( widget.on_index_changed )
        self.widgets.append(widget)

        #nppstr
        widget = InputText( group_box, input_name="nppstr" )
        widget.label = QLabel("nppstr:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #lfcpopt
        widget = InputCheck( group_box, input_name="lfcpopt")
        widget.label = QLabel("lfcpopt:")
        widget.stateChanged.connect( widget.on_state_changed )
        self.widgets.append(widget)

        #fcp_mu
        widget = InputText( group_box, input_name="fcp_mu" )
        widget.label = QLabel("fcp_mu:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #monopole
        widget = InputCheck( group_box, input_name="monopole")
        widget.label = QLabel("monopole:")
        widget.stateChanged.connect( widget.on_state_changed )
        self.widgets.append(widget)

        button = InputButton(self, 'Next')
        button.setToolTip('Proceed to the next input set.')
        button.clicked.connect(group_box.on_click)
        self.widgets.append(button)

        group_box.next_group_box = 'monopole'


    #--------------------------------------------------------#
    # Monopole Inputs
    #--------------------------------------------------------#
    def create_monopole_box(self):
        group_box = self

        #zmon
        widget = InputText( group_box, input_name="zmon" )
        widget.label = QLabel("zmon:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #realxz
        widget = InputCheck( group_box, input_name="realxz")
        widget.label = QLabel("realxz:")
        widget.stateChanged.connect( widget.on_state_changed )
        self.widgets.append(widget)

        #block
        widget = InputCheck( group_box, input_name="block")
        widget.label = QLabel("block:")
        widget.stateChanged.connect( widget.on_state_changed )
        self.widgets.append(widget)

        #block_1
        widget = InputText( group_box, input_name="block_1" )
        widget.label = QLabel("block_1:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #block_2
        widget = InputText( group_box, input_name="block_2" )
        widget.label = QLabel("block_2:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #block_height
        widget = InputText( group_box, input_name="block_height" )
        widget.label = QLabel("block_height:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        button = InputButton(self, 'Next')
        button.setToolTip('Proceed to the next input set.')
        button.clicked.connect(group_box.on_click)
        self.widgets.append(button)

        group_box.next_group_box = 'kpoint'



    #--------------------------------------------------------#
    # K-Point Inputs
    #--------------------------------------------------------#
    def create_kpoint_box(self):
        group_box = self
        
        #nosym
        widget = InputText( group_box, input_name="nosym" )
        widget.label = QLabel("nosym:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #nosym_evc
        widget = InputText( group_box, input_name="nosym_evc" )
        widget.label = QLabel("nosym_evc:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #noinv
        widget = InputText( group_box, input_name="noinv" )
        widget.label = QLabel("noinv:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        button = InputButton(self, 'Next')
        button.setToolTip('Proceed to the next input set.')
        button.clicked.connect(group_box.on_click)
        self.widgets.append(button)

        group_box.next_group_box = 'electrons'
        


    #--------------------------------------------------------#
    # Electrons Inputs
    #--------------------------------------------------------#
    def create_electrons_box(self):
        group_box = self

        #electron_maxstep
        widget = InputText( group_box, input_name="electron_maxstep" )
        widget.label = QLabel("electron_maxstep:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #scf_must_converge
        widget = InputCheck( group_box, input_name="scf_must_converge")
        widget.label = QLabel("scf_must_converge:")
        widget.stateChanged.connect( widget.on_state_changed )
        self.widgets.append(widget)

        #conv_thr
        widget = InputCheck( group_box, input_name="conv_thr")
        widget.label = QLabel("conv_thr:")
        widget.stateChanged.connect( widget.on_state_changed )
        self.widgets.append(widget)

        #adaptive_thr
        widget = InputCheck( group_box, input_name="adaptive_thr")
        widget.label = QLabel("adaptive_thr:")
        widget.stateChanged.connect( widget.on_state_changed )
        self.widgets.append(widget)

        #conv_thr_init
        widget = InputCheck( group_box, input_name="conv_thr_init")
        widget.label = QLabel("conv_thr_init:")
        widget.stateChanged.connect( widget.on_state_changed )
        self.widgets.append(widget)

        #conv_thr_multi
        widget = InputCheck( group_box, input_name="conv_thr_multi")
        widget.label = QLabel("conv_thr_multi:")
        widget.stateChanged.connect( widget.on_state_changed )
        self.widgets.append(widget)

        #mixing_mode
        widget = InputCombo( group_box, "mixing_mode" )
        widget.addItem("Plain", userData = "plain")
        widget.addItem("TF", userData = "TF")
        widget.addItem("Local-TF", userData = "local_TF")
        widget.label = QLabel("mixing_mode:")
        widget.currentIndexChanged.connect( widget.on_index_changed )
        self.widgets.append(widget)

        #mixing_beta
        widget = InputText( group_box, input_name="mixing_beta" )
        widget.label = QLabel("mixing_beta:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #mixing_ndim
        widget = InputText( group_box, input_name="mixing_ndim" )
        widget.label = QLabel("mixing_ndim:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #mixing_fixed_ns
        widget = InputText( group_box, input_name="mixing_fixed_ns" )
        widget.label = QLabel("mixing_fixed_ns:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #diagonalization
        widget = InputCombo( group_box, "diagonalization" )
        widget.addItem("david", userData = "david")
        widget.addItem("cg", userData = "cg")
        widget.label = QLabel("diagonalization:")
        widget.currentIndexChanged.connect( widget.on_index_changed )
        self.widgets.append(widget)

        #diago_thr_init
        widget = InputText( group_box, input_name="diago_thr_init" )
        widget.label = QLabel("diago_thr_init:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #diago_cg_maxiter
        widget = InputText( group_box, input_name="diago_cg_maxiter" )
        widget.label = QLabel("diago_cg_maxiter:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #diago_david_ndim
        widget = InputText( group_box, input_name="diago_david_ndim" )
        widget.label = QLabel("diago_david_ndim:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #diago_full_acc
        widget = InputCheck( group_box, input_name="diago_full_acc")
        widget.label = QLabel("diago_full_acc:")
        widget.stateChanged.connect( widget.on_state_changed )
        self.widgets.append(widget)

        #startingpot
        widget = InputCombo( group_box, "startingpot" )
        widget.addItem("atomic", userData = "atomic")
        widget.addItem("file", userData = "file")
        widget.label = QLabel("startingpot:")
        widget.currentIndexChanged.connect( widget.on_index_changed )
        self.widgets.append(widget)

        #startingwfc
        widget = InputCombo( group_box, "startingwfc" )
        widget.addItem("atomic", userData = "atomic")
        widget.addItem("atomic+random", userData = "atomic+random")
        widget.addItem("random", userData = "random")
        widget.addItem("file", userData = "file")
        widget.label = QLabel("startingwfc:")
        widget.currentIndexChanged.connect( widget.on_index_changed )
        self.widgets.append(widget)

        #tqr
        widget = InputCheck( group_box, input_name="tqr")
        widget.label = QLabel("tqr:")
        widget.stateChanged.connect( widget.on_state_changed )
        self.widgets.append(widget)

        button = InputButton(self, 'Next')
        button.setToolTip('Proceed to the next input set.')
        button.clicked.connect(group_box.on_click)
        self.widgets.append(button)

        group_box.next_group_box = 'ions'



    #--------------------------------------------------------#
    # Ions Inputs
    #--------------------------------------------------------#
    def create_ions_box(self):
        group_box = self

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
        widget.label = QLabel("ion_dynamics:")
        widget.currentIndexChanged.connect( widget.on_index_changed )
        self.widgets.append(widget)

        #ion_positions
        widget = InputCombo( group_box, "ion_positions" )
        widget.addItem("default", userData = "default")
        widget.addItem("from_input", userData = "from_input")
        widget.label = QLabel("ion_positions:")
        widget.currentIndexChanged.connect( widget.on_index_changed )
        self.widgets.append(widget)

        #pot_extrapolation
        widget = InputCombo( group_box, "pot_extrapolation" )
        widget.addItem("None", userData = "none")
        widget.addItem("Atomic", userData = "atomic")
        widget.addItem("First-Order", userData = "first_order")
        widget.addItem("Second-Order", userData = "second_order")
        widget.label = QLabel("pot_extrapolation:")
        widget.currentIndexChanged.connect( widget.on_index_changed )
        self.widgets.append(widget)

        #wfc_extrapolation
        widget = InputCombo( group_box, "wfc_extrapolation" )
        widget.addItem("None", userData = "none")
        widget.addItem("First-Order", userData = "first_order")
        widget.addItem("Second-Order", userData = "second_order")
        widget.label = QLabel("wfc_extrapolation:")
        widget.currentIndexChanged.connect( widget.on_index_changed )
        self.widgets.append(widget)

        #remove_rigid_rot
        widget = InputCheck( group_box, input_name="remove_rigid_rot")
        widget.label = QLabel("remove_rigid_rot:")
        widget.stateChanged.connect( widget.on_state_changed )
        self.widgets.append(widget)

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
        widget.label = QLabel("Thermostat:")
        widget.currentIndexChanged.connect( widget.on_index_changed )
        self.widgets.append(widget)

        #tempw
        widget = InputText( group_box, input_name="tempw" )
        widget.label = QLabel("tempw:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #tolp
        widget = InputText( group_box, input_name="tolp" )
        widget.label = QLabel("tolp:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #delta_t
        widget = InputText( group_box, input_name="delta_t" )
        widget.label = QLabel("delta_t:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #nraise
        widget = InputText( group_box, input_name="nraise" )
        widget.label = QLabel("nraise:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #refold_pos
        widget = InputCheck( group_box, input_name="refold_pos")
        widget.label = QLabel("refold_pos:")
        widget.stateChanged.connect( widget.on_state_changed )
        self.widgets.append(widget)

        #upscale
        widget = InputText( group_box, input_name="upscale" )
        widget.label = QLabel("upscale:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #bfgs_ndim
        widget = InputText( group_box, input_name="bfgs_ndim" )
        widget.label = QLabel("bfgs_ndim:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #trust_radius_min
        widget = InputText( group_box, input_name="trust_radius_min" )
        widget.label = QLabel("trust_radius_min:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #trust_radius_ini
        widget = InputText( group_box, input_name="trust_radius_ini" )
        widget.label = QLabel("trust_radius_ini:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #w_1
        widget = InputText( group_box, input_name="w_1" )
        widget.label = QLabel("w_1:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #w_2
        widget = InputText( group_box, input_name="w_2" )
        widget.label = QLabel("w_2:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        button = InputButton(self, 'Next')
        button.setToolTip('Proceed to the next input set.')
        button.clicked.connect(group_box.on_click)
        self.widgets.append(button)

        group_box.next_group_box = 'cell dynamics'


    #--------------------------------------------------------#
    # Cell Dynamics Inputs
    #--------------------------------------------------------#
    def create_celld_box(self):
        group_box = self

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
        widget.label = QLabel("cell_dynamics:")
        widget.currentIndexChanged.connect( widget.on_index_changed )
        self.widgets.append(widget)

        #press
        widget = InputText( group_box, input_name="press" )
        widget.label = QLabel("press:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #wmass
        widget = InputText( group_box, input_name="wmass" )
        widget.label = QLabel("wmass:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #cell_factor
        widget = InputText( group_box, input_name="cell_factor" )
        widget.label = QLabel("cell_factor:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #press_conv_thr
        widget = InputText( group_box, input_name="press_conv_thr" )
        widget.label = QLabel("press_conv_thr:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

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
        widget.label = QLabel("cell_dofree:")
        widget.currentIndexChanged.connect( widget.on_index_changed )
        self.widgets.append(widget)

        button = InputButton(self, 'Next')
        button.setToolTip('Proceed to the next input set.')
        button.clicked.connect(group_box.on_click)
        self.widgets.append(button)

        group_box.next_group_box = 'print'



    #--------------------------------------------------------#
    # Print Inputs
    #--------------------------------------------------------#
    def create_print_box(self):
        group_box = self

        #disk_io
        widget = InputCombo( group_box, "disk_io" )
        widget.label = QLabel("Disk IO:")
        widget.addItem("High", userData = "high")
        widget.addItem("Medium", userData = "medium")
        widget.addItem("Low", userData = "low")
        widget.addItem("None", userData = "none")
        widget.currentIndexChanged.connect( widget.on_index_changed )
        self.widgets.append(widget)

        #verbosity
        widget = InputCheck( group_box, input_name="verbosity")
        widget.label = QLabel("Verbosity:")
        widget.stateChanged.connect( widget.on_state_changed )
        self.widgets.append(widget)

        #restart_mode
        widget = InputCheck( group_box, input_name="restart_mode")
        widget.label = QLabel("Restart:")
        widget.stateChanged.connect( widget.on_state_changed )
        self.widgets.append(widget)

        #wf_collect - just set to .true.
        widget = InputCheck( group_box, input_name="wf_collect")
        widget.label = QLabel("Collect Wavefunctions:")
        widget.stateChanged.connect( widget.on_state_changed )
        self.widgets.append(widget)

        #max_seconds
        widget = InputText( group_box, input_name="max_seconds" )
        widget.label = QLabel("Checkpoint Time (hrs):")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #iprint
        widget = InputText( group_box, input_name="iprint" )
        widget.label = QLabel("iprint:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #outdir
        widget = InputText( group_box, input_name="outdir" )
        widget.label = QLabel("Output Directory:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #wfcdir
        widget = InputText( group_box, input_name="wfcdir" )
        widget.label = QLabel("Scratch Directory:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #pseudo_dir
        widget = InputText( group_box, input_name="pseudo_dir" )
        widget.label = QLabel("Pseudopotential Directory:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #prefix
        widget = InputText( group_box, input_name="Prefix" )
        widget.label = QLabel("Prefix:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)

        #tstress
        widget = InputCheck( group_box, input_name="tstress")
        widget.label = QLabel("tstress:")
        widget.stateChanged.connect( widget.on_state_changed )
        self.widgets.append(widget)

        #tprnfor
        widget = InputCheck( group_box, input_name="tprnfor")
        widget.label = QLabel("Forces:")
        widget.stateChanged.connect( widget.on_state_changed )
        self.widgets.append(widget)

        #lkpoint_dir
        widget = InputText( group_box, input_name="lkpoint_dir" )
        widget.label = QLabel("lkpoint_dir:")
        widget.textChanged.connect( widget.on_text_changed )
        self.widgets.append(widget)


        button = InputButton(self, 'Next')
        button.setToolTip('Proceed to the next input set.')
        button.clicked.connect(group_box.on_click)
        self.widgets.append(button)

        group_box.next_group_box = '???'



    def on_update(self):

        print("Box updating")
        print(self)
        print(self.window())

        self.window().on_window_update()

        #self.update_layout()

    @pyqtSlot()
    def on_click(self):

        print('PyQt5 button click')

        #create the box for system information
        self.window().system_box = self.window().create_box(self.next_group_box)
        self.window().boxes_layout.addWidget(self.window().system_box)





class InputField():
    """
    This class represents a text box in the GUI
    """

    def __init__(self, parent_, type, label_name = None, input_name = None):

        self.type = type
        self.label_name = label_name
        self.input_name = input_name

        #is this widget currently being shown to the user?
        self.shown = False

        #conditions under which this text box should be shown
        self.show_conditions = []

        #list of all possible combo choices
        self.combo_choices = []

        self.group_box = parent_

        self.group_box.widgets.append(self)

        self.initialize_widget()

    def initialize_widget(self):

        if self.label_name:
            self.label = QLabel(self.label_name)
        else:
            self.label = None

        if self.type == "text":

            self.widget = InputText2(self.group_box, self.input_name)
            self.widget.textChanged.connect( self.widget.on_text_changed )

        elif self.type == "combo":

            self.widget = InputCombo2(self.group_box, self.input_name)
            self.widget.currentIndexChanged.connect( self.widget.on_index_changed )
            
        elif self.type == "check":
            
            self.widget = InputCheck2(self.group_box, self.input_name)
            self.widget.stateChanged.connect( self.widget.on_state_changed )

        elif self.type == "button":
            
            self.widget = InputButton2(self.group_box, self.input_name)
            self.widget.clicked.connect(self.group_box.on_click)
        
    def add_combo_choice(self, label, name):
        
        self.widget.currentIndexChanged.disconnect()
        self.widget.addItem( label, userData = name )
        self.widget.currentIndexChanged.connect( self.widget.on_index_changed )

        #self.combo_choices.append( (label,name) )
        self.combo_choices.append( (label,name) )


    def set_visible(self, visible):
        
        if visible:
            #create a new widget
            self.initialize_widget()
            self.shown = True

            #determine where this new row needs to be inserted
            index = self.group_box.widgets.index(self)

            if self.label:
                self.group_box.layout.insertRow( index, self.label, self.widget )
            else:
                self.group_box.layout.insertRow( index, self.widget )

            if self.type == "combo":
                #add all of the combo choices to the new widget
                temp_choices = [ self.combo_choices[i] for i in range(len(self.combo_choices)) ]
                self.combo_choices = []
                for combo_choice in temp_choices:
                    self.add_combo_choice(combo_choice[0],combo_choice[1])

        else:
            #delete this widget
            self.widget.deleteLater()
            self.widget = None
            self.shown = False
            if self.label:
                self.label.deleteLater()
                self.label = None
                


class InputText2(QLineEdit):
    """
    This class represents a text box in the GUI
    """

    def __init__(self, parent_, input_name = None):
        super(QLineEdit, self).__init__(parent = parent_)

        self.input_name = input_name

        #initialize the input text
        try:
            text = self.parent().input_file.inputs[self.input_name]
            self.setText(text)
        except KeyError:
            pass

    @pyqtSlot(str)
    def on_text_changed(self, string):
        
        self.parent().input_file.inputs[self.input_name] = string
        self.parent().on_update()

        #print(input_file.inputs)

class InputCombo2(QComboBox):
    """
    This class represents a drop-down box in the GUI
    """

    def __init__(self, parent_, input_name = None):
        super(QComboBox, self).__init__(parent = parent_)

        self.input_name = input_name

    @pyqtSlot(int)
    def on_index_changed(self, index):
        
        self.parent().input_file.inputs[self.input_name] = self.itemData(index)
        self.parent().on_update()

class InputCheck2(QCheckBox):
    """
    This class represents a check box in the GUI
    """

    def __init__(self, parent_, input_name = None):
        super(QCheckBox, self).__init__(parent = parent_)

        self.input_name = input_name

    @pyqtSlot(int)
    def on_state_changed(self, value):
        
        self.parent().input_file.inputs[self.input_name] = value
        self.parent().on_update()

class InputButton2(QPushButton):
    """
    This class represents a button in the GUI
    """

    def __init__(self, parent_, input_name = None):
        super(QPushButton, self).__init__(input_name, parent = parent_)

        self.input_name = input_name









class InputText(QLineEdit):
    """
    This class represents a text box in the GUI
    """

    def __init__(self, parent_, input_name = None):
        super(QLineEdit, self).__init__(parent = parent_)

        self.input_name = input_name

        #does this widget have a label widget?
        self.label = None

        #is this widget currently being shown to the user?
        self.shown = False

        #conditions under which this text box should be shown
        self.show_conditions = []

        #initialize the input text
        try:
            text = self.parent().input_file.inputs[self.input_name]
            self.setText(text)
        except KeyError:
            pass

    def set_visible(self, visible):
        #find my row
        #layout = self.parent().layout
        #pos = layout.getWidgetPosition(self)
        #print(pos)
        #print(pos[0])

        self.setVisible(visible)
        self.shown = visible
        
        if self.label:
            self.label.setVisible(visible)
            self.label.shown = visible

    @pyqtSlot(str)
    def on_text_changed(self, string):
        
        self.parent().input_file.inputs[self.input_name] = string
        self.parent().on_update()

        #print(input_file.inputs)







class InputCombo(QComboBox):
    """
    This class represents a drop-down box in the GUI
    """

    def __init__(self, parent_, input_name = None):
        super(QComboBox, self).__init__(parent = parent_)

        self.input_name = input_name

        #does this widget have a label widget?
        self.label = None

        #is this widget currently being shown to the user?
        self.shown = False

        #conditions under which this drop-down box should be shown
        self.show_conditions = []

    def set_visible(self, visible):
        self.setVisible(visible)
        self.shown = visible
        
        if self.label:
            self.label.setVisible(visible)
            self.label.shown = visible

    @pyqtSlot(int)
    def on_index_changed(self, index):
        
        self.parent().input_file.inputs[self.input_name] = self.itemData(index)
        self.parent().on_update()





class InputCheck(QCheckBox):
    """
    This class represents a check box in the GUI
    """

    def __init__(self, parent_, input_name = None):
        super(QCheckBox, self).__init__(parent = parent_)

        self.input_name = input_name

        #does this widget have a label widget?
        self.label = None

        #is this widget currently being shown to the user?
        self.shown = False

        #conditions under which this check box should be shown
        self.show_conditions = []

    def set_visible(self, visible):
        self.setVisible(visible)
        self.shown = visible
        
        if self.label:
            self.label.setVisible(visible)
            self.label.shown = visible

    @pyqtSlot(int)
    def on_state_changed(self, value):
        
        self.parent().input_file.inputs[self.input_name] = value
        self.parent().on_update()





class InputButton(QPushButton):
    """
    This class represents a button in the GUI
    """

    def __init__(self, parent_, input_name = None):
        super(QPushButton, self).__init__(input_name, parent = parent_)

        self.input_name = input_name

        #does this widget have a label widget?
        self.label = None

        #is this widget currently being shown to the user?
        self.shown = False

        #conditions under which this check box should be shown
        self.show_conditions = []

    def set_visible(self, visible):
        self.setVisible(visible)
        self.shown = visible
        
        if self.label:
            self.label.setVisible(visible)
            self.label.shown = visible

#    @pyqtSlot(int)
#    def on_state_changed(self, value):
#        
#        self.parent().input_file.inputs[self.input_name] = value
#        self.parent().on_update()






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
