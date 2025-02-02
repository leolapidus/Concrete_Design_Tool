"""This module only contains the Assembler class.
"""


class Assembler(object):
    """An Assembler helps to generate system matrices/vectors from elements.

    Attributes
    ----------
    dofs : list
        List of all dofs in the system. The Dofs with dirichlet constraints are at the end.
    dof_indices : dict
        Dictionary containing the index of each dof. The index is equal to the position of the dof
        in the dofs-list.
    dof_count : int
        Total number of dofs.
    free_dof_count : int
        Number of dofs without dirichlet constraints.
    fixed_dof_count : int
        Number of dofs with dirichlet constraints.
    element_freedom_table : list
        List with tuples containing the elements and the coresponding dof indices.
    """

    def __init__(self, model):
        """Create a new Assembler

        Parameters
        ----------
        model : Model
            Model to assemble.
        """

        # --- dof indices

        processed_dofs = set()

        free_dofs = list()
        fixed_dofs = list()

        for element in model.elements:
            for dof in element.dofs:
                if dof in processed_dofs:
                    continue
                else:
                    processed_dofs.add(dof)

                if dof in model.dirichlet_conditions:
                    fixed_dofs.append(dof)
                else:
                    free_dofs.append(dof)

        dofs = free_dofs + fixed_dofs

        dof_indices = {dof: index for index, dof in enumerate(dofs)}


        # --- element freedom table

        element_freedom_table = list()

        for element in model.elements:
            indices = [dof_indices[dof] for dof in element.dofs]

            element_freedom_table.append((element, indices))


        # --- store

        self.dofs = dofs
        self.dof_indices = dof_indices
        self.dof_count = len(dofs)
        self.free_dof_count = len(free_dofs)
        self.fixed_dof_count = len(fixed_dofs)
        self.element_freedom_table = element_freedom_table

    def index_of_dof(self, dof):
        """Get the index of the given dof.

        Parameters
        ----------
        dof : object
            Dof at the index.

        Returns
        -------
        index : int
            Index of the given dof.
        """
        return self.dof_indices[dof]

    def dof_at_index(self, index):
        """Get the dof at the given index.

        Parameters
        ----------
        index : int
            Index of the dof.

        Returns
        -------
        dof : object
            Dof at the given index.
        """
        return self.dofs[index]

    

    @property
    def free_dofs(self):
        """Get a list with the unconstrained dofs

        Returns
        -------
        free_dofs : list
            List with the unconstrained dofs
        """
        return self.dofs[:self.free_dof_count]

    def assemble_matrix(self, system_matrix, calculate_element_matrix):
        """Assemble element matrices into a system matrix.

        Parameters
        ----------
        system_matrix : ndarray
            System matrix to store the results. The results are added to the existing values.
        calculate_element_matrix : function Element -> ndarray
            Function to calculate the element matrix.
        """
        for element, indices in self.element_freedom_table:
            element_matrix = calculate_element_matrix(element)

            if element_matrix is None:
                continue

            for element_row, system_row in enumerate(indices):
                for element_col, system_col in enumerate(indices):
                    value = element_matrix[element_row, element_col]
                    system_matrix[system_row, system_col] += value

    def assemble_vector(self, system_vector, calculate_element_vector):
        """Assemble element vectors into a system vector.

        Parameters
        ----------
        system_vector : ndarray
            System vector to store the results. The results are added to the existing values.
        calculate_element_vector : function Element -> ndarray
            Function to calculate the element vector.
        """
        for element, indices in self.element_freedom_table:
            element_vector = calculate_element_vector(element)

            if element_vector is None:
                continue

            for element_row, system_row in enumerate(indices):
                system_vector[system_row] += element_vector[element_row]


    