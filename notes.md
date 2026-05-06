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
- 30/04 opérateurs binaires, exécution JIT
- 04/05 ajout des blocs, ajout des ifs
- 05/05 ajout des variables, (cli, yaml)
- 06/05
    - Besoin d'un block fonction pour appeller une, ArgOp (a renomer mais tkt)