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
    - faire des structure
        - attention au ABI *application binary interface*
        - getelementptr
    - etendre VarType, qui est une enum ... *creation AttributeType = StructType | VarType*
    - création d'une structure : génération de l'Attribute correspondant
    - accéder à un attribut
        - différence getelementptr et LoadOp.get(memref_val, [OpConst]) ????
        - memref.LoadOp se lower à llvm.getelementptr
        - memref.LoadOp accepte que des SSAValue, donc pas de 0, 1, 2... possible
        -> Utiliser memeref.SubviewOp.get(), finalement, on essaye LoadOp
- 12/05
    - On veut obtenir les types des variables sans toujours les préciser.
        - Si type est None, alors prendre le type existant dans variable heap
        - Sinon on genere le type depuis les infos données
            - Si basic type: On génère
            - Si structure : On cherche une définition
        - Crash si pas d'infos
    - Définir les attributs d'une structure
        - On ré-utilise notre structure de variable
        - Mais on ne veut pas "allouer" les attributs sur la heap
        - Finallement, on ne réutilise pas le code des variables
    - Comment gérer les accès aux attributs
        - Chaque type possède un get_attribute(str) pour accéder à un de ses attributs
            - Si struct, position de l'attribut parmis les attribus définis
            - Si array, indice de la valeur
            - Si variable, pas d'attribut, on crash
        - Besoin en lecture et en écriture
        - Besoin de savoir le type python de la variable xDSL
            - Le type xDSL s'obtient avec le type de la valeur affectée
            - Mais cette valeur est de type MLIR, l'information est perdue
            - Sauf si à la création de la variable, le type est sauvegardé ?
        - a.truc = 4 : Le RHS est de type int, a.truc aussi, mais on a besoin de savoir le type de a
- 13/05
    - Ré-organisation du code et des imports
    - SetOp
    - Memref ne permet pas d'accéder à des attributs de structure llvm
        - Soit Memref + llvm
        - Soit llvm.load
        - Soit llvm.getelementptr ou dialect ptr
        - Soit builtin.tuple ?
    - Autres structure
        - Pour un même type: Tuples / Struct
        - Tensort --- Bufferization ---> Memref
        - ptr ?
    - A faire:
        - Analyse des besoins
        - Modane ?
        - Tableaux memref ?
        - Structures ?
- 18/05
    - 

https://discourse.llvm.org/t/codegen-dialect-overview/2723
https://mlir.llvm.org/docs/Dialects/Vector/


# Autre

# Structures ?
class LLVMStructType(ParametrizedAttribute, TypeAttribute):
    class ParametrizedAttribute(Attribute):
        class Attribute(ABC):
    class TypeAttribute(Attribute):

    
class SSAValue(IRWithUses, IRWithName, ABC, Generic[AttributeCovT]):
    class IRWithUses(ABC):
    class IRWithName(ABC):
    AttributeCovT = TypeVar(
        "AttributeCovT", bound=Attribute, covariant=True, default=Attribute
    )

AnyFloat: TypeAlias = (
    BFloat16Type | Float16Type | Float32Type | Float64Type | Float80Type | Float128Type
)
class BFloat16Type(ParametrizedAttribute, _FloatType):
class ParametrizedAttribute(Attribute):


from_mixed_indices -> 
class GEPOp(IRDLOperation):
class IRDLOperation(Operation):
class Operation(_IRNode):
    """A generic operation. Operation definitions inherit this class."""

créer  une struct a besoin de Attribute ? C'est okay
Hummmmm, sinon utiliser le type renvoyé par ce truc ?

## Differents types
Type opaque (utilisé par des dialects ayant besoin de leurs propres types) https://mlir.llvm.org/docs/Dialects/Builtin/#opaqueattr
Type (type qui contient un type) https://mlir.llvm.org/docs/Dialects/Builtin/#typeattr
Unitattr ? https://mlir.llvm.org/docs/Dialects/Builtin/#unitattr
StridedLayoutAttr https://mlir.llvm.org/docs/Dialects/Builtin/#stridedlayoutattr
DenseTypedElementsAttr : Raw buffer same attribut, pas optimisé, utiliser plutôt raw bytes instead https://mlir.llvm.org/docs/Dialects/Builtin/#densetypedelementsattr
denseresourceelementsattr ? : https://mlir.llvm.org/docs/Dialects/Builtin/#denseresourceelementsattr
densearrayattr = DenseTypedElementsAttr mais pas d'opti pour le "splat" https://mlir.llvm.org/docs/Dialects/Builtin/#densearrayattr
DenseTypedElementsAttr https://mlir.llvm.org/docs/Dialects/Builtin/#arrayattr
DistinctAttribut
complex : nombre imaginaire https://mlir.llvm.org/docs/Dialects/Builtin/#complextype
TupleType : tuple possiblement de differents types https://mlir.llvm.org/docs/Dialects/Builtin/#tupletype

## ABI
Application Binary Interface (ABI).
https://sbaziotis.com/compilers/how-target-independent-is-your-ir.html


A faire
- différences SSAValues et SSAValue 
- Extern C obligatoire ? Mais pas trop un pb ?
- ll++ ? llc++ ?
