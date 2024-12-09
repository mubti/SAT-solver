import argparse
import sys
import subprocess


def invalid_input():
    print("Invalid input")
    sys.exit()

def read_input_file(filename):
    global edge_dictionary
    global circuit_length
    global vertices
    vertices = set()
    edge_number = 1 # 0 is for new line
    edge_dictionary = {}
    with open(filename, 'r') as f:
        number_of_edges = int(f.readline())
        for i in range(number_of_edges):
            vertices_string = f.readline().replace("\n", "")
            vertices_tuple = vertices_string.split(" ")
            if edge_dictionary.get((int(vertices_tuple[0]), int(vertices_tuple[1]))) is not None:
                invalid_input()
            if len(vertices_tuple) != 2:
                invalid_input()
            vertices.add(int(vertices_tuple[0]))
            vertices.add(int(vertices_tuple[1]))
            edge_dictionary.update({(int(vertices_tuple[0]), int(vertices_tuple[1])): edge_number})
            edge_number += 1
        circuit_length = int(f.readline())
    if circuit_length > number_of_edges:
        invalid_input()
    return number_of_edges

def get_neighbours(vertex: int):
    global edge_dictionary
    neighbours = []
    for edge in edge_dictionary.keys():
        if edge[0] == vertex or edge[1] == vertex:
            neighbours.append(edge_dictionary[edge])
    return neighbours

def get_subsets(number_of_edges: int, length_of_circuit: int):
    count = number_of_edges - length_of_circuit + 1
    partial_cnf = []
    clause = []
    for i in range(1, count + 1):
        clause.append(i)
    partial_cnf.append(clause)
    for i in range(count + 1, number_of_edges + 1):
        for subset in partial_cnf:
            if subset.count(i) == 1:
                continue
            for item in subset:
                new_subset = subset.copy()
                new_subset.append(i)
                new_subset.remove(item)
                new_subset.sort()
                if partial_cnf.count(new_subset) == 1:
                    continue
                partial_cnf.append(new_subset)
    return partial_cnf

def create_cnf(number_of_edges, circuit_length):
    # returns list of lists of integers
    cnf = []
    clause = []
    global edge_dictionary
    global length_of_circuit
    global vertices

    # minimum of 2 or none edges per vertex = for each vertex either none or at least 2 edges are in circuit
    for vertex in vertices:
        edges = get_neighbours(vertex)
        edges.sort()
        for i in edges:
            for j in edges:
                if i == j:
                    clause.append(-j)
                else:
                    clause.append(j)
            cnf.append(clause)
            clause = []

    # maximum of 2 edges per vertex = for each 3 edges by vertex there is at least one that is not in circuit
    clause = []
    for vertex in vertices:
        neighbours = get_neighbours(vertex)
        neighbours.sort()
        if len(neighbours) < 3:
            continue
        for i in range(2, len(neighbours)):
            for j in range(1, i):
                for k in range(j):
                    clause.append(-neighbours[i])
                    clause.append(-neighbours[j])
                    clause.append(-neighbours[k])

                    cnf.append(clause)
                    clause = []


    # circuit has minimum of k edges = for each e - k + 1 edges there is at least one that is in circuit
    subset = get_subsets(number_of_edges, circuit_length)
    for clause in subset:
        cnf.append(clause)

    return cnf



def call_solver(cnf, edge_number, output_name, solver_name, verbosity):
    # print CNF into formula.cnf in DIMACS format
    with open(output_name, "w") as file:
        file.write("p cnf " + str(edge_number) + " " + str(len(cnf)) + '\n')
        for clause in cnf:
            file.write(' '.join(str(lit) for lit in clause) + " 0\n")

    # call the solver and return the output
    return subprocess.run(['./' + solver_name, '-model', '-verb=' + str(verbosity) , output_name], stdout=subprocess.PIPE)


def print_result(result, edge_dictionary: dict):
    for line in result.stdout.decode('utf-8').split('\n'):
        # print the whole output of the SAT solver to stdout, so you can see the raw output for yourself
        print(line)

    # check the returned result
    if (result.returncode == 20):       # returncode for SAT is 10, for UNSAT is 20
        return

    # parse the model from the output of the solver
    # the model starts with 'v'
    model = []
    for line in result.stdout.decode('utf-8').split('\n'):
        # there might be more lines of the model, each starting with 'v'
        if line.startswith("v"):
            vars = line.split(" ")
            vars.remove("v")
            model.extend(int(v) for v in vars)
    # 0 is the end of the model, just ignore it
    model.remove(0)

    print()
    print("##################################################################")
    print("###########[ Human readable result of the tile puzzle ]###########")
    print("##################################################################")
    print()

    print("Circuit will use these edges:")

    readable_result = []

    for node in model:
        if node < 0:
            continue
        for key in edge_dictionary.keys():
            if edge_dictionary[key] == node:
                readable_result.append((key[0], key[1]))
    readable_result.sort()
    for edge in readable_result:
        print(edge)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i",
                        "--input",
                        default="input.in",
                        type=str,
                        help="name of the input file."
                        )
    parser.add_argument("-o",
                        "--output",
                        default="formula.cnf",
                        type=str,
                        help="name of file, where the cnf formula is stored."
                        )
    parser.add_argument("-s",
                        "--solver",
                        default="glucose-syrup",
                        type=str,
                        help="name of the SAT solver used.")
    parser.add_argument("-v",
                        "--verb",
                        default=1,
                        choices=[0, 1],
                        help="verbosity level of the SAT solver.")
    args = parser.parse_args()
    global circuit_length
    global edge_dictionary
    edge_number = read_input_file(args.input)
    cnf = create_cnf(edge_number, circuit_length)
    result = call_solver(cnf, edge_number, args.output, args.solver, args.verb)
    print_result(result, edge_dictionary)


