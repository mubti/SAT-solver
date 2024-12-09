# SAT Solver pro problém "Longest circuit" #

_Longest circuit_ je problém určení existence kružnice délky _k_ v neorientovaném grafu _G_.

### Kódování do CNF ###

Všechny hrany na vstupu se očíslují a označí se jako prvovýroky. pokud je _i_-tý prvovýrok pravdivý, 
znamená to, že _i_-tá hrana patří do kružnice velikosti minimálně _k_.
Kódování do CNF probíhá v několika krocích. Nejprve zapíšu, že žádný vrchol nemůže mít
v kružnici přesně jednu hranu. Tím program určí, že každý vrchol buď nebude mít v kružnici žádnou hranu, 
nebo bude mít v kružnici 2 a více hran.

Druhý krok algorimu omezí počet hran u každého vrcholu na maximálně 2.

Třetí krok zpracuje dané číslo _k_, což je minimální počet hran na hledané kružnici.

Bohužel se mi nepodařilo vytvořit klauzule, které by se staraly o to, aby se nenašly
2 různé disjunktní kružnice. Pokud se najdou disjunktní kružnice, jejichž součet hran je k, vrátí program
kladnou odpověď, i když by někdy měl vrátit zápornou.


### Uživatelská dokumentace ###

Program je psaný na procesoru architektury ARM64.
Pokud budete mít problém program spustit, zkuste si stáhnout
[glucose](https://github.com/audemard/glucose/) SAT solver a vyměnit soubor
glucose.syrup v adresáři programu.


Vstup přímá program v souboru. Standardní název souboru je input.in. 
Na první řádce je počet hran n, na řádkách 2 - n + 1 jsou vždy 2 vrcholy. Na poslední řádce
(= n+2) je poté číslo k, neboli délka hledané kružnice

Chování programu lze ovlivnit pomocí přepínačů. Seznam podporovaných přepínačů:

| Přepínač     | funkce                                               | výchozí hodnota |
|--------------|------------------------------------------------------|-----------------|
| -i, --input  | změna vstupního souboru                              | input.in        |
| -o, --output | změna souboru, do kterého se zapisuje DIMACS CNF     | formula.cnf     |
| -v, --verb   | změna podrobnosti podaných informací od SAT solveru  | 1               |
| -s, --solver | nastavení vlastního solveru                          | glucose.syrup   |


### Příklady ###

1) malý příklad, který lze vyřešit.
```
5
1 2
2 3
3 4
4 1
1 3
4

```

Tento graf je čtverec s jednou úhlopříčkou. Hledáme v grafu cyklus velikosti 4.

2) malý příklad, který nelze vyřešit
```
4
2 3
3 4
4 1
1 3
4

```

Tento graf je trojúhelník s připojeným jedním bodem pomocí jedné hrany. V grafu znovu hedáme
cyklus velikosti 4. V grafu ale žádný takovýto cyklus není.

3) netriviální, dlouho trvající příklad.

Protože se CNF generuje na základě poćtu hran a dělá se mnoho kombinací
tak se prgram hodně zpomalí, pokud mu dáme úplný graf. Proto vytvořil graf 
K7. Tento úkol je triviální pro člověka, ale program nad ním přemýšlí opravdu dlouho. 



