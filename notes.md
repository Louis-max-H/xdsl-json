if {} then {} else {};

Version avec un block
{
    "type": "if",
    "then": {
        "type": "block",
        "content": ["machin"]
    }
}

Version sans block
{
    "type": "if",
    "then": [
        ["machin"]
    ]
}
=> Et appelle de codegen_block(self.then) plutôt que self.then.codegen()



Historique:
- 30/04
    - opérateurs binaires
    - exécution JIT
- 04/05
    - ajout des blocs
    - ajout des ifs
- 05/05
    - ajout des variables
    - cli, yaml
- 06/05
    - besoin d'un block fonction pour appeller list instructions
    - besoin typage des variables
    - différences SSAValues[Result] et SSAValue[Attribut]
    - mise à jour des types des blocks
    - (BaseValue, BaseReturn, BaseGeneric)
- 07/07
    - while
    - lowering to llvm
    - appeller depuis cpp
    - print (IA)
    - bug premier argument correspond au nombre de params
    - structures ??
