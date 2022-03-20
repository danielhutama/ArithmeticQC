# ArithmeticQC
Dan's reconfigurable quantum computing library of arithmetic functions.

Work in progress. Components will be cast into Python classes later in development. 

Goal: Shor's algorithm with 7n+1 qubits, where n = ceil(log2(N)). N is the semiprime integer to be factored. This follows Vlatko Vedral's gate descriptions for component modules. 

Project roadmap:

19-03-2022   |   CARRY

19-03-2022   |   SUM

20-03-2022   |   ADDER

TBD          |   MOD ADDER

TBD          |   CTRL-MULT MOD

TBD          |   MOD EXP



ADDER gate currently supports reconfigurability for number of qubits n. Based on the bitsize of N, the ADDER gate implementation programmatically generates the appropriate amount of SUM and CARRY components. 

ADDER: |a>|b>|0> --> |a>|a+b>|0>

