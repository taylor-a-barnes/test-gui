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

        self.boxes_layout.addWidget(group_box)

        group_box.update_visibility()

        #if the new group box is not visible, create the next one
        if not group_box.shown:
            self.create_box(group_box.next_group_box)

        return group_box

    def on_window_update(self):

        #print("Window Updating")

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
        self.shown = True


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

        #print("start of initialize_widgets")
        #print(self.window())
        
        if self.group_name == 'basic':
            self.create_basic_box()
        elif self.group_name == 'cell':
            self.create_cell_box()
        elif self.group_name == 'hubbard':
            self.create_hubbard_box()
            self.show_conditions.append( [ ["GUI_exx_corr","==","dft+u"], 
                                           "or", ["GUI_exx_corr","==","dft+u+j"] ] )
        elif self.group_name == 'system':
            self.create_system_box()
        elif self.group_name == 'vdw':
            self.create_vdw_box()
            self.show_conditions.append( [ [ ["vdw_corr","==","grimme-d2"], "or",
                                           ["vdw_corr","==","tkatchenko-scheffler"] ], "or",
                                           ["vdw_corr","==","xdm"] ])
        elif self.group_name == 'md':
            self.create_md_box()
            self.show_conditions.append( ["calculation","==","md"] )
        elif self.group_name == 'magnetization':
            self.create_magnetization_box()
            self.show_conditions.append( [ ["nspin","==","2"], 
                                           "or", ["nspin","==","4"] ] )
        elif self.group_name == 'noncollinear':
            self.create_noncollinear_box()
            self.show_conditions.append( ["nspin","==","4"] )
        elif self.group_name == 'efield':
            self.create_efield_box()
            self.show_conditions.append( [ ["GUI_efield_type","==","tefield"], 
                                           "or", ["GUI_efield_type","==","lefield"] ] )
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

        #print("end of initialize_widgets")
        #print(self.window())

    def update_visibility(self):

        #if this group should not be shown, hide it and then initialize the next box
        should_show = self.check_show_conditions(self)

        if should_show:
            self.setVisible(True)
            self.shown = True
        else:
            self.setVisible(False)
            self.shown = False
            #self.window().create_box(self.next_group_box)

    def apply_layout(self):

        for w in self.widgets:

            try:
                if w.label:
                    self.layout.addRow( w.label, w.widget )
                else:
                    self.layout.addRow( w.widget )

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

        self.update_visibility()
        
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

            if condition[1] == "==":

                if input == condition[2]:
                    return True
                else:
                    return False

            elif condition[1] == "!=":

                if input == condition[2]:
                    return False
                else:
                    return True


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
        widget = InputField( group_box, "text", label_name = "System Charge:", input_name = "tot_charge")

        #ecutwfc
        widget = InputField( group_box, "text", label_name = "ecutwfc:", input_name = "ecutwfc")

        #GUI_exx_corr (custom)
        widget = InputField( group_box, "combo", label_name = "Exchange Correction:", input_name = "GUI_exx_corr")
        widget.add_combo_choice( "None", "none" )
        widget.add_combo_choice( "LDA+U", "dft+u" )
        widget.add_combo_choice( "LDA+U+J", "dft+u+j" )
        widget.add_combo_choice( "Hybrid Functional", "hybrid" )

        #vdw_corr
        widget = InputField( group_box, "combo", label_name = "Van der Waals Correction:", input_name = "vdw_corr")
        widget.add_combo_choice( "None", "none" )
        widget.add_combo_choice( "Grimme-D2", "grimme-d2" )
        widget.add_combo_choice( "Tkatchenko-Scheffler", "tkatchenko-scheffler" )
        widget.add_combo_choice( "XDM", "xdm" )

        #nspin
        widget = InputField( group_box, "combo", label_name = "Spin Polarization:", input_name = "nspin")
        widget.add_combo_choice( "None", "1" )
        widget.add_combo_choice( "Spin-Polarized", "2" )
        widget.add_combo_choice( "Noncollinear Spin-Polarized", "4" )

        #GUI_efield_type
        widget = InputField( group_box, "combo", label_name = "Electric Field:", input_name = "GUI_efield_type")
        widget.add_combo_choice( "None", "none" )
        widget.add_combo_choice( "Saw-Like", "tefield" )
        widget.add_combo_choice( "Homogeneous", "lefield" )

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

        #GUI_variable_cell
        widget = InputField( group_box, "check", label_name = "Cell Relaxation:", input_name = "GUI_variable_cell")
        widget.show_conditions.append( ["calculation","==","relax"] )

        #GUI_variable_cell
        widget = InputField( group_box, "check", label_name = "Cell Dynamics:", input_name = "GUI_variable_cell")
        widget.show_conditions.append( ["calculation","==","md"] )

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
        widget = InputField( group_box, "combo", label_name = "DFT Functional:", input_name = "input_dft")
        widget.add_combo_choice( "BLYP", "blyp" )
        widget.add_combo_choice( "PBE", "pbe" )
        widget.add_combo_choice( "PBE0", "pbe0" )
        widget.add_combo_choice( "HSE", "hse" )
        widget.show_conditions.append( ["GUI_exx_corr","==","hybrid"] )

        #etot_conv_thr
        widget = InputField( group_box, "text", label_name = "Energy Convergence:", input_name = "etot_conv_thr")

        #forc_conv_thr
        widget = InputField( group_box, "text", label_name = "Force Convergence:", input_name = "forc_conv_thr")
        widget.show_conditions.append( ["calculation","==","relax"] )

        #nstep
        widget = InputField( group_box, "text", label_name = "Maximum Relaxation Steps:", input_name = "nstep")
        widget.show_conditions.append( ["calculation","==","relax"] )

        #nstep
        widget = InputField( group_box, "text", label_name = "Number of Timesteps:", input_name = "nstep")
        widget.show_conditions.append( ["calculation","==","md"] )

        #nbnd
        widget = InputField( group_box, "text", label_name = "Number of Bands:", input_name = "nbnd")

        #tot_magnetization
        widget = InputField( group_box, "text", label_name = "tot_magnetization:", input_name = "tot_magnetization")

        #ecutrho
        widget = InputField( group_box, "text", label_name = "ecutrho:", input_name = "ecutrho")

        #nr1, nr2, and nr3
        #nr1s, nr2s, and nr3s

        #occupations
        widget = InputField( group_box, "combo", label_name = "occupations:", input_name = "occupations")
        widget.add_combo_choice( "Gaussian Smearing", "smearing" )
        widget.add_combo_choice( "Tetrahedron (Bloechl Method)", "tetrahedra" )
        widget.add_combo_choice( "Tetrahedron (Linear Method)", "tetrahedra_lin" )
        widget.add_combo_choice( "Tetrahedron (Kawamura Method)", "tetrahedra_opt" )
        widget.add_combo_choice( "Fixed", "fixed" )
        widget.add_combo_choice( "Custom", "from_input" )

#NOTE: for occupations, default to 'smearing', unless doing DOS or phonons, in which case use 'tetrahedra_opt' - the Kawamura Method
        
        #smearing
        widget = InputField( group_box, "combo", label_name = "Smearing Method:", input_name = "smearing")
        widget.add_combo_choice( "Ordinary Gaussian", "gaussian" )
        widget.add_combo_choice( "Methfessel-Paxton", "methfessel-paxton" )
        widget.add_combo_choice( "Marzari-Vanderbilt", "marzari-vanderbilt" )
        widget.add_combo_choice( "Fermi-Dirac", "Fermi-Dirac" )
        
#NOTE: default to Marzari-Vanderbilt 'cold smearing'

        #degauss
        widget = InputField( group_box, "text", label_name = "degauss:", input_name = "degauss")

#NOTE: degauss has suggested values of 0.06-0.10 Ry

        #exx_fraction
        widget = InputField( group_box, "text", label_name = "exx_fraction:", input_name = "exx_fraction")
        widget.show_conditions.append( ["GUI_exx_corr","==","hybrid"] )

        #ecutfock
        widget = InputField( group_box, "text", label_name = "ecutfock:", input_name = "ecutfock")
        widget.show_conditions.append( ["GUI_exx_corr","==","hybrid"] )

        #screening_parameter
        widget = InputField( group_box, "text", label_name = "screening_parameter:", input_name = "screening_parameter")
        widget.show_conditions.append( ["GUI_exx_corr","==","hybrid"] )

        #exxdiv_treatment
        widget = InputField( group_box, "text", label_name = "exxdiv_treatment:", input_name = "exxdiv_treatment")
        widget.show_conditions.append( ["GUI_exx_corr","==","hybrid"] )

        #x_gamma_extrapolation
        widget = InputField( group_box, "text", label_name = "x_gamma_extrapolation:", input_name = "x_gamma_extrapolation")
        widget.show_conditions.append( ["GUI_exx_corr","==","hybrid"] )

        #ecutvcut
        widget = InputField( group_box, "text", label_name = "ecutvcut:", input_name = "ecutvcut")
        widget.show_conditions.append( ["GUI_exx_corr","==","hybrid"] )

        #nqx1, nqx2, nqx3
        widget = InputField( group_box, "text", label_name = "nqx1, nqx2, nqx3:", input_name = "nqx1")
        widget.show_conditions.append( ["GUI_exx_corr","==","hybrid"] )




        widget = InputField( group_box, "button", input_name = "Next")

        group_box.next_group_box = 'hubbard'


    #--------------------------------------------------------#
    # Hubbard Inputs
    #--------------------------------------------------------#
    def create_hubbard_box(self):
        group_box = self

        #lda_plus_u
        widget = InputField( group_box, "check", label_name = "DFT+U:", input_name = "lda_plus_u")

#NOTE: Instead of having a checkbox, just turn DFT+U on if a non-zero U is applied to any species

        #lda_plus_u_kind
        widget = InputField( group_box, "check", label_name = "DFT+U+J:", input_name = "lda_plus_u_kind")

#NOTE: Instead of having a checkbox, just turn DFT+U+J on if a non-zero J is applied to any species

        #U_projection_type
        widget = InputField( group_box, "combo", label_name = "U Projection Type:", input_name = "U_projection_type")
        widget.add_combo_choice( "Atomic", "atomic" )
        widget.add_combo_choice( "Ortho-Atomic", "ortho-atomic" )
        widget.add_combo_choice( "Norm-Atomic", "norm-atomic" )
        widget.add_combo_choice( "File", "file" )
        widget.add_combo_choice( "Pseudo", "pseudo" )

        #starting_ns_eigenvalue(m,ispin,l)
        widget = InputField( group_box, "text", label_name = "starting_ns_eigenvalue:", input_name = "starting_ns_eigenvalue")

        #--------------------------------------------------------#
        # Per-species information
        #--------------------------------------------------------#

        #Hubbard_U
        widget = InputField( group_box, "text", label_name = "U:", input_name = "U")

        #Hubbard_J0
        widget = InputField( group_box, "text", label_name = "J0:", input_name = "J0")

        #Hubbard_alpha
        widget = InputField( group_box, "text", label_name = "alpha:", input_name = "alpha")

        #Hubbard_beta
        widget = InputField( group_box, "text", label_name = "beta:", input_name = "beta")

        #Hubbard_J
        widget = InputField( group_box, "text", label_name = "J:", input_name = "J")

        widget = InputField( group_box, "button", input_name = "Next")

        group_box.next_group_box = 'vdw'




    #--------------------------------------------------------#
    # VdW Inputs
    #--------------------------------------------------------#
    def create_vdw_box(self):
        group_box = self

        #london_rcut
        widget = InputField( group_box, "text", label_name = "london_rcut:", input_name = "london_rcut")

        #ts_vdw_econv_thr
        widget = InputField( group_box, "text", label_name = "ts_vdw_econv_thr:", input_name = "ts_vdw_econv_thr")

        #ts_vdw_isolated
        widget = InputField( group_box, "text", label_name = "ts_vdw_isolated:", input_name = "ts_vdw_isolated")

        #london_s6
        widget = InputField( group_box, "text", label_name = "london_s6:", input_name = "london_s6")

        #xdm_a1
        widget = InputField( group_box, "text", label_name = "xdm_a1:", input_name = "xdm_a1")

        #xdm_a2
        widget = InputField( group_box, "text", label_name = "xdm_a2:", input_name = "xdm_a2")

        #--------------------------------------------------------#
        # Per-species information
        #--------------------------------------------------------#

        #london_c6
        widget = InputField( group_box, "text", label_name = "london_c6:", input_name = "london_c6")

        #london_rvdw
        widget = InputField( group_box, "text", label_name = "london_rvdw:", input_name = "london_rvdw")

        widget = InputField( group_box, "button", input_name = "Next")

        group_box.next_group_box = 'md'



    #--------------------------------------------------------#
    # MD Inputs
    #--------------------------------------------------------#
    def create_md_box(self):
        group_box = self

        #dt
        widget = InputField( group_box, "text", label_name = "Timestep:", input_name = "dt")

        #ion_dynamics
        widget = InputField( group_box, "combo", label_name = "ion_dynamics:", input_name = "ion_dynamics")
        widget.add_combo_choice( "verlet", "verlet" )
        widget.add_combo_choice( "langevin", "langevin" )
        widget.add_combo_choice( "langevin-smc", "langevin-smc" )
        widget.show_conditions.append( ["GUI_variable_cell","==",0] )

        #ion_dynamics
        widget = InputField( group_box, "combo", label_name = "ion_dynamics:", input_name = "ion_dynamics")
        widget.add_combo_choice( "beeman", "beeman" )
        widget.show_conditions.append( ["GUI_variable_cell","==",2] )


        widget = InputField( group_box, "button", input_name = "Next")

        group_box.next_group_box = 'magnetization'




    #--------------------------------------------------------#
    # Magnetization Inputs
    #--------------------------------------------------------#
    def create_magnetization_box(self):
        group_box = self

        #starting_spin_angle
        widget = InputField( group_box, "check", label_name = "starting_spin_angle:", input_name = "starting_spin_angle")

        #constrainted_magnetization
        widget = InputField( group_box, "combo", label_name = "Magnetization Constraint:", input_name = "constrained_magnetization")
        widget.add_combo_choice( "None", "none" )
        widget.add_combo_choice( "Total", "total" )
        widget.add_combo_choice( "Atomic", "atomic" )
        widget.add_combo_choice( "Total Direction", "total_direction" )
        widget.add_combo_choice( "Atomic Direction", "atomic_direction" )

        #fixed_magnetization
        widget = InputField( group_box, "text", label_name = "fixed_magnetization:", input_name = "fixed_magnetization")

        #lambda
        widget = InputField( group_box, "text", label_name = "lambda:", input_name = "lambda")

        #report
        widget = InputField( group_box, "text", label_name = "report:", input_name = "report")

        #--------------------------------------------------------#
        # Per-species information
        #--------------------------------------------------------#

        #starting_magnetization
        widget = InputField( group_box, "text", label_name = "starting_magnetization:", input_name = "starting_magnetization")

        widget = InputField( group_box, "button", input_name = "Next")

        group_box.next_group_box = 'noncollinear'



    #--------------------------------------------------------#
    # Noncollinear Inputs
    #--------------------------------------------------------#
    def create_noncollinear_box(self):
        group_box = self

        #lspinorb
        widget = InputField( group_box, "check", label_name = "lspinorb:", input_name = "lspinorb")
        
        #--------------------------------------------------------#
        # Per-species information
        #--------------------------------------------------------#

        #angle1
        widget = InputField( group_box, "text", label_name = "angle1:", input_name = "angle1")

        #angle2
        widget = InputField( group_box, "text", label_name = "angle2:", input_name = "angle2")

        widget = InputField( group_box, "button", input_name = "Next")

        group_box.next_group_box = 'efield'



    #--------------------------------------------------------#
    # Electric Field Inputs
    #--------------------------------------------------------#
    def create_efield_box(self):
        group_box = self

        #tefield
        widget = InputField( group_box, "check", label_name = "Saw-Like Electric Field:", input_name = "tefield")
                
        #edir
        widget = InputField( group_box, "text", label_name = "edir:", input_name = "edir")

        #emaxpos
        widget = InputField( group_box, "text", label_name = "emaxpos:", input_name = "emaxpos")

        #eopreg
        widget = InputField( group_box, "text", label_name = "eopreg:", input_name = "eopreg")

        #eamp
        widget = InputField( group_box, "text", label_name = "eamp:", input_name = "eamp")

        #dipfield
        widget = InputField( group_box, "check", label_name = "Dipole Correction:", input_name = "dipfield")

        #lefield
        widget = InputField( group_box, "check", label_name = "Homogeneous Electric Field:", input_name = "lefield")

        #efield
        widget = InputField( group_box, "text", label_name = "efield:", input_name = "efield")

        #efield_cart(3)
        widget = InputField( group_box, "text", label_name = "efield_cart:", input_name = "efield_cart")

        #efield_phase
        widget = InputField( group_box, "combo", label_name = "efield_phase:", input_name = "efield_phase")
        widget.add_combo_choice( "Read", "read" )
        widget.add_combo_choice( "Write", "write" )
        widget.add_combo_choice( "None", "none" )

        #nberrycyc
        widget = InputField( group_box, "text", label_name = "nberrycyc:", input_name = "nberrycyc")

        #lorbm
        widget = InputField( group_box, "check", label_name = "lorbm:", input_name = "lorbm")

        #lberry
        widget = InputField( group_box, "check", label_name = "lberry:", input_name = "lberry")

        #gdir
        widget = InputField( group_box, "combo", label_name = "gdir:", input_name = "gdir")
        widget.add_combo_choice( "First Reciprocal Lattice Vector", "1" )
        widget.add_combo_choice( "First Reciprocal Lattice Vector", "2" )
        widget.add_combo_choice( "First Reciprocal Lattice Vector", "3" )

        #nppstr
        widget = InputField( group_box, "text", label_name = "nppstr:", input_name = "nppstr")

        #lfcpopt
        widget = InputField( group_box, "check", label_name = "lfcpopt:", input_name = "lfcpopt")

        #fcp_mu
        widget = InputField( group_box, "text", label_name = "fcp_mu:", input_name = "fcp_mu")

        #monopole
        widget = InputField( group_box, "check", label_name = "monopole:", input_name = "monopole")

        widget = InputField( group_box, "button", input_name = "Next")

        group_box.next_group_box = 'monopole'


    #--------------------------------------------------------#
    # Monopole Inputs
    #--------------------------------------------------------#
    def create_monopole_box(self):
        group_box = self

        #zmon
        widget = InputField( group_box, "text", label_name = "zmon:", input_name = "zmon")

        #realxz
        widget = InputField( group_box, "check", label_name = "realxz:", input_name = "realxz")

        #block
        widget = InputField( group_box, "check", label_name = "block:", input_name = "block")

        #block_1
        widget = InputField( group_box, "text", label_name = "block_1:", input_name = "block_1")

        #block_2
        widget = InputField( group_box, "text", label_name = "block_2:", input_name = "block_2")

        #block_height
        widget = InputField( group_box, "text", label_name = "block_height:", input_name = "block_height")

        widget = InputField( group_box, "button", input_name = "Next")

        group_box.next_group_box = 'kpoint'



    #--------------------------------------------------------#
    # K-Point Inputs
    #--------------------------------------------------------#
    def create_kpoint_box(self):
        group_box = self
        
        #nosym
        widget = InputField( group_box, "text", label_name = "nosym:", input_name = "nosym")

        #nosym_evc
        widget = InputField( group_box, "text", label_name = "nosym_evc:", input_name = "nosym_evc")

        #noinv
        widget = InputField( group_box, "text", label_name = "noinv:", input_name = "noinv")

        widget = InputField( group_box, "button", input_name = "Next")

        group_box.next_group_box = 'electrons'
        


    #--------------------------------------------------------#
    # Electrons Inputs
    #--------------------------------------------------------#
    def create_electrons_box(self):
        group_box = self

        #electron_maxstep
        widget = InputField( group_box, "text", label_name = "electron_maxstep:", input_name = "electron_maxstep")

        #scf_must_converge
        widget = InputField( group_box, "check", label_name = "scf_must_converge:", input_name = "scf_must_converge")

        #conv_thr
        widget = InputField( group_box, "text", label_name = "conv_thr:", input_name = "conv_thr")

        #adaptive_thr
        widget = InputField( group_box, "check", label_name = "adaptive_thr:", input_name = "adaptive_thr")

        #conv_thr_init
        widget = InputField( group_box, "text", label_name = "conv_thr_init:", input_name = "conv_thr_init")

        #conv_thr_multi
        widget = InputField( group_box, "text", label_name = "conv_thr_multi:", input_name = "conv_thr_multi")

        #mixing_mode
        widget = InputField( group_box, "combo", label_name = "mixing_mode:", input_name = "mixing_mode")
        widget.add_combo_choice( "Plain", "plain" )
        widget.add_combo_choice( "TF", "TF" )
        widget.add_combo_choice( "Local-TF", "local-TF" )

        #mixing_beta
        widget = InputField( group_box, "text", label_name = "mixing_beta:", input_name = "mixing_beta")

        #mixing_ndim
        widget = InputField( group_box, "text", label_name = "mixing_ndim:", input_name = "mixing_ndim")

        #mixing_fixed_ns
        widget = InputField( group_box, "text", label_name = "mixing_fixed_ns:", input_name = "mixing_fixed_ns")

        #diagonalization
        widget = InputField( group_box, "combo", label_name = "diagonalization:", input_name = "diagonalization")
        widget.add_combo_choice( "david", "david" )
        widget.add_combo_choice( "cg", "cg" )

        #diago_thr_init
        widget = InputField( group_box, "text", label_name = "diago_thr_init:", input_name = "diago_thr_init")

        #diago_cg_maxiter
        widget = InputField( group_box, "text", label_name = "diago_cg_maxiter:", input_name = "diago_cg_maxiter")

        #diago_david_ndim
        widget = InputField( group_box, "text", label_name = "diago_david_ndim:", input_name = "diago_david_ndim")

        #diago_full_acc
        widget = InputField( group_box, "text", label_name = "diago_full_acc:", input_name = "diago_full_acc")

        #startingpot
        widget = InputField( group_box, "combo", label_name = "startingpot:", input_name = "startingpot")
        widget.add_combo_choice( "atomic", "atomic" )
        widget.add_combo_choice( "file", "file" )

        #startingwfc
        widget = InputField( group_box, "combo", label_name = "startingwfc:", input_name = "startingwfc")
        widget.add_combo_choice( "atomic", "atomic" )
        widget.add_combo_choice( "atomic+random", "atomic+random" )
        widget.add_combo_choice( "random", "random" )
        widget.add_combo_choice( "file", "file" )

        #tqr
        widget = InputField( group_box, "check", label_name = "tqr:", input_name = "tqr")

        widget = InputField( group_box, "button", input_name = "Next")

        group_box.next_group_box = 'ions'



    #--------------------------------------------------------#
    # Ions Inputs NOTE: ONLY FOR RELAXATION CALCULATIONS
    #--------------------------------------------------------#
    def create_ions_box(self):
        group_box = self

        #ion_dynamics
        widget = InputField( group_box, "combo", label_name = "ion_dynamics:", input_name = "ion_dynamics")
        widget.add_combo_choice( "bfgs", "bfgs" )
        widget.add_combo_choice( "damp", "damp" )

        #ion_positions
#        widget = InputField( group_box, "combo", label_name = "ion_positions:", input_name = "ion_positions")
#        widget.add_combo_choice( "default", "default" )
#        widget.add_combo_choice( "from_input", "from_input" )

        #pot_extrapolation
        widget = InputField( group_box, "combo", label_name = "Potential Extrapolation:", input_name = "pot_extrapolation")
        widget.add_combo_choice( "None", "none" )
        widget.add_combo_choice( "Atomic", "atomic" )
        widget.add_combo_choice( "First-Order", "first_order" )
        widget.add_combo_choice( "Second-Order", "first_order" )

        #wfc_extrapolation
        widget = InputField( group_box, "combo", label_name = "Wavefunction Extrapolation:", input_name = "wfc_extrapolation")
        widget.add_combo_choice( "None", "none" )
        widget.add_combo_choice( "First-Order", "first_order" )
        widget.add_combo_choice( "Second-Order", "first_order" )

        #remove_rigid_rot
        widget = InputField( group_box, "check", label_name = "remove_rigid_rot:", input_name = "remove_rigid_rot")
        widget.show_conditions.append( ["assume_isolated","!=","none"] )

        #ion_temperature
        widget = InputField( group_box, "combo", label_name = "ion_temperature:", input_name = "ion_temperature")
        widget.add_combo_choice( "rescaling", "rescaling" )
        widget.add_combo_choice( "rescale-v", "rescale-v" )
        widget.add_combo_choice( "rescale-T", "rescale-T" )
        widget.add_combo_choice( "reduce-T", "reduce-T" )
        widget.add_combo_choice( "berendsen", "berendsen" )
        widget.add_combo_choice( "andersen", "andersen" )
        widget.add_combo_choice( "initial", "initial" )
        widget.add_combo_choice( "not_controlled", "not_controlled" )

        #tempw
        widget = InputField( group_box, "text", label_name = "tempw:", input_name = "tempw")

        #tolp
        widget = InputField( group_box, "text", label_name = "tolp:", input_name = "tolp")

        #delta_t
        widget = InputField( group_box, "text", label_name = "delta_t:", input_name = "delta_t")

        #nraise
        widget = InputField( group_box, "text", label_name = "nraise:", input_name = "nraise")

        #refold_pos
        widget = InputField( group_box, "check", label_name = "refold_pos:", input_name = "refold_pos")

        #upscale
        widget = InputField( group_box, "text", label_name = "upscale:", input_name = "upscale")

        #bfgs_ndim
        widget = InputField( group_box, "text", label_name = "bfgs_ndim:", input_name = "bfgs_ndim")

        #trust_radius_min
        widget = InputField( group_box, "text", label_name = "trust_radius_min:", input_name = "trust_radius_min")

        #trust_radius_ini
        widget = InputField( group_box, "text", label_name = "trust_radius_ini:", input_name = "trust_radius_ini")

        #w_1
        widget = InputField( group_box, "text", label_name = "w_1:", input_name = "w_1")

        #w_2
        widget = InputField( group_box, "text", label_name = "w_2:", input_name = "w_2")

        widget = InputField( group_box, "button", input_name = "Next")

        group_box.next_group_box = 'cell dynamics'


    #--------------------------------------------------------#
    # Cell Dynamics Inputs
    #--------------------------------------------------------#
    def create_celld_box(self):
        group_box = self

        #cell_dynamics
        widget = InputField( group_box, "combo", label_name = "cell_dynamics:", input_name = "cell_dynamics")
        widget.add_combo_choice( "none", "none" )
        widget.add_combo_choice( "sd", "sd" )
        widget.add_combo_choice( "damp-pr", "damp-pr" )
        widget.add_combo_choice( "damp-w", "damp-w" )
        widget.add_combo_choice( "bfgs", "bfgs" )
        widget.add_combo_choice( "none", "none" )
        widget.add_combo_choice( "pr", "pr" )
        widget.add_combo_choice( "w", "w" )

        #press
        widget = InputField( group_box, "text", label_name = "press:", input_name = "press")

        #wmass
        widget = InputField( group_box, "text", label_name = "wmass:", input_name = "wmass")

        #cell_factor
        widget = InputField( group_box, "text", label_name = "cell_factor:", input_name = "cell_factor")

        #press_conv_thr
        widget = InputField( group_box, "text", label_name = "press_conv_thr:", input_name = "press_conv_thr")

        #cell_dofree
        widget = InputField( group_box, "combo", label_name = "cell_dofree:", input_name = "cell_dofree")
        widget.add_combo_choice( "all", "all" )
        widget.add_combo_choice( "x", "x" )
        widget.add_combo_choice( "y", "y" )
        widget.add_combo_choice( "z", "z" )
        widget.add_combo_choice( "xy", "xy" )
        widget.add_combo_choice( "xz", "xz" )
        widget.add_combo_choice( "yz", "yz" )
        widget.add_combo_choice( "xyz", "xyz" )
        widget.add_combo_choice( "shape", "shape" )
        widget.add_combo_choice( "volume", "volume" )
        widget.add_combo_choice( "2Dxy", "2Dxy" )
        widget.add_combo_choice( "2Dshape", "2Dshape" )

        widget = InputField( group_box, "button", input_name = "Next")

        group_box.next_group_box = 'print'



    #--------------------------------------------------------#
    # Print Inputs
    #--------------------------------------------------------#
    def create_print_box(self):
        group_box = self

        #disk_io
        widget = InputField( group_box, "combo", label_name = "disk_io:", input_name = "disk_io")
        widget.add_combo_choice( "High", "high" )
        widget.add_combo_choice( "Medium", "medium" )
        widget.add_combo_choice( "Low", "low" )
        widget.add_combo_choice( "None", "none" )

        #verbosity
        widget = InputField( group_box, "check", label_name = "Verbosity:", input_name = "verbosity")

        #restart_mode
        widget = InputField( group_box, "check", label_name = "restart_mode:", input_name = "restart_mode")

        #wf_collect - just set to .true.
        widget = InputField( group_box, "check", label_name = "wf_collect:", input_name = "wf_collect")

        #max_seconds
        widget = InputField( group_box, "text", label_name = "Checkpoint Time (hrs):", input_name = "max_seconds")

        #iprint
        widget = InputField( group_box, "text", label_name = "iprint:", input_name = "iprint")

        #outdir
        widget = InputField( group_box, "text", label_name = "Output Directory:", input_name = "outdir")

        #wfcdir
        widget = InputField( group_box, "text", label_name = "Scratch Directory:", input_name = "wfcdir")

        #pseudo_dir
        widget = InputField( group_box, "text", label_name = "Pseudopotential Directory:", input_name = "pseudo_dir")

        #prefix
        widget = InputField( group_box, "text", label_name = "Prefix:", input_name = "prefix")

        #tstress
        widget = InputField( group_box, "check", label_name = "tstress:", input_name = "tstress")

        #tprnfor
        widget = InputField( group_box, "check", label_name = "tprnfor:", input_name = "tprnfor")

        #lkpoint_dir
        widget = InputField( group_box, "check", label_name = "lkpoint_dir:", input_name = "lkpoint_dir")

        widget = InputField( group_box, "button", input_name = "Next")

        group_box.next_group_box = '???'



    def on_update(self):

        #print("Box updating")
        #print(self)
        #print(self.window())

        self.window().on_window_update()

        #self.update_layout()

    @pyqtSlot()
    def on_click(self):

        #print('PyQt5 button click')

        #create the next group box
        self.window().create_box(self.next_group_box)





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

        self.initialize_value()

    def initialize_widget(self):

        if self.label_name:
            self.label = QLabel(self.label_name)
        else:
            self.label = None

        if self.type == "text":

            self.widget = InputText(self.group_box, self.input_name)
            self.widget.textChanged.connect( self.widget.on_text_changed )

        elif self.type == "combo":

            self.widget = InputCombo(self.group_box, self.input_name)
            self.widget.currentIndexChanged.connect( self.widget.on_index_changed )
            
        elif self.type == "check":
            
            self.widget = InputCheck(self.group_box, self.input_name)
            self.widget.stateChanged.connect( self.widget.on_state_changed )

        elif self.type == "button":
            
            self.widget = InputButton(self.group_box, self.input_name)
            self.widget.clicked.connect(self.group_box.on_click)

    def initialize_value(self):

        if self.type == "text":

            self.group_box.input_file.inputs[self.input_name] = ""

        elif self.type == "combo":

            pass #must wait until an item is added before initializing this value
            
        elif self.type == "check":

            self.group_box.input_file.inputs[self.input_name] = 0
            
        elif self.type == "button":

            pass
        
    def add_combo_choice(self, label, name):
        
        self.widget.currentIndexChanged.disconnect()
        self.widget.addItem( label, userData = name )
        self.widget.currentIndexChanged.connect( self.widget.on_index_changed )

        #self.combo_choices.append( (label,name) )
        self.combo_choices.append( (label,name) )


        #if this is the first choice, initialize the value associated with this widget
        if len(self.combo_choices) == 1:

            self.group_box.input_file.inputs[self.input_name] = self.widget.itemData(0)



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
                


class InputText(QLineEdit):
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

class InputCombo(QComboBox):
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

class InputCheck(QCheckBox):
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

class InputButton(QPushButton):
    """
    This class represents a button in the GUI
    """

    def __init__(self, parent_, input_name = None):
        super(QPushButton, self).__init__(input_name, parent = parent_)

        self.input_name = input_name











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
