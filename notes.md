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
    - besoin d'un block fonction *pour appeller list instructions*
    - besoin typage des variables *pour l'argument de la fonction*
    - mise à jour des types des blocks *car if et func ne sont pas du même dialect*
    - différences SSAValues[Result] et SSAValue[Attribut], *car block ne renvoie pas forcément de valeurs*
- 07/07
    - while *tester la modification de variables*
    - lowering to llvm
    - compilation en .s
    - appeller depuis cpp
    - print (IA)
- 11/07
    - structure
