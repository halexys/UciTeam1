# Beginner / This will make you ANGRy


+ Library that allows to create symbolic variables: claripy
+ Argument length: 0x24 (36), dado las comparaciones de las funciones dbg.main(6 caracteres) + db.check_part1(6 caracteres) + dbg.check_part2(6 caracteres) + dbg.check_part3(18 caracteres) = 36
+ Hex value of first printable character: 0x20 (SPACE), inicio del rango de caracteres a usar
+ Hex value of last printable character: 0x7e (~), final del rango de caracteres a usar
+ Success condition: state.posix.dumps(1) (salida estandar de angr) y return b'Success!' porque es la string que usa el binario al salir todo bien
+ Fail condition state.posix.dumps(1) (salida estandar de angr) y return b'Fail!' porque es la string que usa el binario al salir algo mal
+ Evaluation of a symbolic expression: solver.eval(a,b) 

Script arreglado para encontrar la bandera usando angr

``` python
import angr
import claripy

# Crear un proyecto de angr
project = angr.Project('angry', auto_load_libs=False)

# Definir la longitud del argumento
argument_length = 0x24

# Crear una variable simbólica del tamaño del argumento, cada carácter es de 8 bits
argument = claripy.BVS('argument', 8 * argument_length)

# Definir el estado inicial con el argumento simbólico
# Añadir opciones para eliminar advertencias molestas de angr
initial_state = project.factory.entry_state(
    args=['./angry', argument],
    add_options={
        angr.options.SYMBOL_FILL_UNCONSTRAINED_MEMORY,
        angr.options.SYMBOL_FILL_UNCONSTRAINED_REGISTERS
    }
)

# Restringir cada byte de la entrada para que sea un carácter imprimible
for byte in argument.chop(8):
    initial_state.solver.add(byte >= 0x20)  # Valor hexadecimal del primer carácter imprimible
    initial_state.solver.add(byte <= 0x7e)  # Valor hexadecimal del último carácter imprimible

# Definir la condición de éxito
def is_successful(state):
    stdout_output = state.posix.dumps(1)  # Salida estándar
    return b'Success!' in stdout_output  # Mensaje que indica éxito

# Definir la condición de fallo
def should_abort(state):
    stdout_output = state.posix.dumps(1)  # Salida estándar
    return b'Fail!' in stdout_output  # Mensaje que indica fallo

# Definir el gestor de simulación
simgr = project.factory.simulation_manager(initial_state)

# Explorar el binario buscando una solución
print("Explorando...")
simgr.explore(find=is_successful, avoid=should_abort)

# Comprobar si se encontró una solución
if simgr.found:
    solution_state = simgr.found[0]
    solution = solution_state.solver.eval(argument, cast_to=bytes)  # Evaluación de una expresión simbólica
    print(f"Found the solution: {solution.decode()}")
else:
    print("Could not find the solution.")
```

`flag{Rev3rsIng_Is_e4si3r_uz1nG_angr}`
