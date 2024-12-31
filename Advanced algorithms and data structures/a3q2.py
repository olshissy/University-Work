#Oliver Hiscoke 32461356

import sys

def tableau_simplex(objective_func, lhs_constraints, rhs_constraints, num_decisions, num_constraints):
    """
    Solves a linear programming problem using the Simplex method in tableau form 

    :param objective_func: Coefficients of the objective function to maximise
    :param lhs_constraints: Coefficients of the decision variables in the LHS of the constraints
    :param rhs_constraints: RHS values of the constraints
    :param num_decisions: The number of decision variables
    :param num_constraints: The number of constraints in the linear programming problem
    :return max_value: Maximum value of the objective function at the optimal solution
    :return solution: Values of the decision variables at the optimal solution 
    """

    # Build initial tableau
    tableau = []

    # Add slack variables to LHS of constraints
    for i in range(num_constraints):
        # Add the LHS, slack variables as 0 and RHS of the constraints to the row
        row = lhs_constraints[i] + [0] * num_constraints + [rhs_constraints[i]]

        # Update the required slack variable to 1
        row[num_decisions + i] = 1

        # Append to the tableau
        tableau.append(row)

    # Add slack variables to the objective function 
    tableau_header = [cj for cj in objective_func] + [0] * num_constraints  # RHS = 0 for objective row

    # All slack variables are considered non-basic to start
    non_basic_vars = list(range(num_decisions, num_decisions + num_constraints))

    #Loop until the optimal solution is reached 
    while True:

        #Calculate the zj and cj-zj values for the current iteration
        zj = calculate_zj(non_basic_vars, tableau, tableau_header, num_constraints, num_decisions)
        cj_zj = calculate_cj_zj(objective_func, zj, num_constraints, num_decisions)

        #When all cj-zj are 0 or less, no further improvements can be made. Terminate loop
        if all(c <= 0 for c in cj_zj):
             break
            
        #Entering variable is determined by the max positive value in cj-zj values
        entering = cj_zj.index(max(cj_zj))

        #Calculate the theta values to find the leaving variable 
        theta = []
        for i in range(num_constraints):
            
            #If the coefficient of the entering variable is positive 
            if tableau[i][entering] > 0:
                
                #Calculate RHS/entering variable coefficient 
                theta.append(tableau[i][-1] / tableau[i][entering])
           
            else:
                
                #If negative or 0, set theta to infinity
                theta.append(float('inf'))

        #The row with the smallest possible theta value leaves the basis 
        leaving = theta.index(min(theta))

        pivot_row = tableau[leaving] #The row that will pivot (leaving row)
        pivot_value = pivot_row[entering] #The pivot element 

        #Normalise the pivot row by dividing by the pivot element 
        tableau[leaving] = [x / pivot_value for x in pivot_row]

        #Update other rows in the tableau using the pivot row 
        for i in range(num_constraints):
             
             #For all rows except the pivot row 
             if i != leaving:
                
                #Factor to eliminate the entering variable from other rows
                row_factor = tableau[i][entering]
                
                #Perform row operation 
                tableau[i] = [tableau[i][j] - row_factor * tableau[leaving][j] for j in range(len(tableau[0]))]

        #Replace the leaving variable with the entering variable 
        non_basic_vars[leaving] = entering

    #Extract the solution from the final tableau
    solution = [0] * num_decisions
    
    for i in range(num_constraints):

        #If the non-basic variable is a decision variable
        if non_basic_vars[i] < num_decisions:
            
            #Set the solution to the RHS value 
            solution[non_basic_vars[i]] = tableau[i][-1]

    #Calculate the maximum value of the objective function
    max_value = sum(solution[i] * objective_func[i] for i in range(num_decisions))

    return max_value, solution
            



def calculate_zj(non_basic_vars, tableau, tableau_header, num_constraints, num_decisions):
        """
        Function used to calculate the values of Zj (dot product of two vectors)

        :param non_basic_vars: An array of indices indicating the positions of the non basic variables
        :param tableau: The current tableau
        :param tableau_header: The current state of the objective function
        :param num_constraints: The number of constraints in the linear problem
        :param num_decisions: The number of decisions in the linear problem 
        :return: An array of the Zj values 
        """

        zj = [0] * (num_decisions + num_constraints + 1)  # Extra space for RHS

        # Iterate through each column in the tableau (including RHS)
        for j in range(num_decisions + num_constraints + 1):

            zj[j] = sum(tableau[i][j] * tableau_header[non_basic_vars[i]] for i in range(num_constraints))
        
        return zj



def calculate_cj_zj(objective_func, zj, num_constraints, num_decisions):
        """
        Function used to calculate the values of Cj - Zj

        :param objective_func: The objective function of the linear problem
        :param zj: An array of the current Zj values
        :param num_constraints: The number of constraints in the linear problem
        :param num_decisions: The number of decisions in the linear problem 
        :return: An array of the Cj - Zj values 
        """
        
        # Ensure objective_func has zeros for slack variables if needed
        full_objective = objective_func + [0] * num_constraints
        
        return [(full_objective[j] - zj[j]) for j in range(num_decisions + num_constraints)]



def read_input_file(filename):
    """
    Function to read the data from an input file 

    :param filename: The name of the file being read
    :return: The relevant inputs to the tableau_simplex function
    """
    
    with open(filename, 'r') as file:
        lines = file.readlines()

    num_decisions = int(lines[1].strip())
    num_constraints = int(lines[3].strip())
    objective_func = list(map(int, lines[5].strip().split(',')))
    lhs_constraints = [list(map(int, line.strip().split(','))) for line in lines[7:7+num_constraints]]
    rhs_constraints = [int(lines[7 + num_constraints + i + 1].strip()) for i in range(num_constraints)]

    return objective_func, lhs_constraints, rhs_constraints, num_decisions, num_constraints



def write_output_file(filename, max_value, solution):
    """
    Function to write the output to a file 

    :param filename: The name of the file to write to 
    :param max_value: The max value obtained by tableau_simplex
    :param solution: The solution obtained by tableau_simplex
    """

    with open(filename, 'w') as file:
        file.write('# Optimal_Values_of_Decision_Variables\n')
        file.write(', '.join(map(str, solution)) + '\n')
        file.write('# Optimal_Value_of_Objective_Function\n')
        file.write(str(max_value) + "\n")


obj_func = [1,1]
lhs_constraints = [[1,2], [4,2], [-1,1]]
rhs_constraints = [4,12,1]
num_decisions = 2
num_constraints = 3

print(tableau_simplex(obj_func, lhs_constraints, rhs_constraints, num_decisions, num_constraints))

# if __name__ == "__main__":
    
#     input_filename = sys.argv[1]

#     try:
#         objective_func, lhs_constraints, rhs_constraints, num_decisions, num_constraints = read_input_file(input_filename)
#         max_value, solution = tableau_simplex(objective_func, lhs_constraints, rhs_constraints, num_decisions, num_constraints)

#         output_filename = "output_q2.txt"
#         write_output_file(output_filename, max_value, solution)

#     except Exception as e:
#         print("Error:", e)
