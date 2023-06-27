# AbitaPy

<img src="../logos/logo_abitapy.png" alt="" width="400px">

## Installation

> Prérequis : vous devez avoir `Python 2.7` ou `Python 3.7+` d'installé selon la
> version que vous souhaitez utiliser.

* Téléchargez la dernière version de l'archive `AbitaPy.zip` sur la page des
    releases : [https://github.com/hydrielax/Abita/releases](https://github.com/hydrielax/Abita/releases)
* Décompressez l'archive, puis ouvrez un terminal dans le dossier extrait
* Installez les dépendances :
    ```bash
    pip install -r requirements.txt
    ```
* Lancez le programme :
    ```bash
    python3 -m abitaPy
    ```
    ou pour la version en python2 :
    ```bash
    python -m abitaPy2
    ```

## Utilisation

### Exécution du solveur

Dans le dossier `AbitaPy` (avec une majuscule), vous pouvez exécuter la commande
`abitaPy` d'une des manières suivantes :
* `$ python3 -m abitaPy` : le programme vous demande alors d'entrer le chemin
    d'un fichier `.abi` en entrée, et le nom du fichier de sortie ;
* `$ python3 -m abitaPy source.abi` : le programme lit le fichier `source.abi`
    et enregistre les résultats dans un fichier `source_solved.abi` ;
* `$ python3 -m abitaPy source.abi sortie.abi` : le programme lit le fichier
    `source.abi` et enregistre les résultats dans `sortie.abi`.

Le fichier généré contient alors la liste des solutions possibles : il est 
visualisable dans Grasshopper via le module Abita4Rhino, ou dans le visualiseur
de Abita+.

> À NOTER : si vous souhaitez utiliser python2, la commande à exécuter devient 
> `python2 -m abitaPy2` au lieu de `python3 -m abitaPy`. 

### Exemples

Des exemples sont fournis dans le dossier `data`. Vous pouvez les tester avec la
commande suivante (par exemple pour tester le fichier `G001.abi` et enregistrer 
les résultats dans un fichier `G001_solved.abi`) :
```bash
python3 -m abitaPy data/G001.abi data/G001_solved.abi
```

### Écriture d'un fichier .abi

Ce programme fonctionne avec le format de fichiers `.abi`. 
Pour créer un problème, créez un fichier `.abi` selon les consignes décrites
dans le document `Docs/User_Manual_Abita+.pdf` (des exemples sont fournis 
dans le dossier `data`). Celui-ci devrait avoir la structure suivante (les 
valeurs marquées comme facultatives ont pour valeur par défaut celles données 
en exemple, sauf indication contraire) :
```python
# PARAMÈTRES
A1     3000     # initIT (facultatif, défaut à -1)
A2      120     # endIT (facultatif, défaut à -1)
A3      100     # Nombre de solutions souhaitées (facultatif)
A4     0.00     # Paramètre alpha (facultatif)
# Types de lot : [valeur pour 1m²] [surface min] [surface max] [nombre min] [nombre max] (facultatif)
T1    70.00    30.00    45.00      0   1000     
T2    80.00    45.00    60.00      0   1000
T3   100.00    60.00    75.00      0   1000
T4    50.00    75.00    85.00      0   1000
T5    40.00    85.00   100.00      0   1000

# GÉOMÉTRIE
# Définition de l'étage n°1
F1
# Point n°x [coordonée X en mètres] [coordonée Y en mètres]
P1       0.00     0.00      
P2       6.00     0.00
P3      12.00     0.00
P4       0.00     6.00
P5       6.00     6.00
P6      12.00     6.00
P7       0.00    12.00
P8       6.00    12.00
P9      12.00    12.00
# Elément n°X [nombre de points] [liste des numéros des points]
E1    4   1   2   5   4
E2    4   2   3   6   5
E3    4   4   5   8   7
E4    4   5   6   9   8
# Définir l'élément 1 comme Entrée-Sortie (obligatoire, au moins un élément)
X1
# Définir l'élément 2 comme Commun Imposé
I2
# Définir l'élément 3 comme Commun Possible
C3
```

*REMARQUE : les commentaires (signalés par `#`) dans les fichiers `.abi` ne
sont admis que par le solveur Python ; le solveur C++ (cf Abita+) ne les
accepte pas.*



## Utilisation du code pour exécution pas à pas

Cette documentation permet de comprendre comment fonctionne le code, et explique
pas à pas comment l'utiliser pour créer algoritmiquement une géométrie puis les
solutions associées.

1. Créez un script Python3. On supposera dans la suite, pour les imports, que le
    dossier `abitaPy` (avec une minuscule) se situe dans le même dossier que 
    votre script. 
    > REMARQUE : si vous souhaitez écrire un script pour Python2, remplacez le
    > dossier `abitaPy` par le dossier `abitaPy2`. De même, dans toutes les 
    > lignes de code qui suivent, remplacez les imports du module `abitaPy` par 
    > le module `abitaPy2`.

1. Créez de nouveaux objets `Geom` et `Population` vides, puis créez l'objet 
    `Algo` avec les deux objets précédents :
    ```python
    from abitaPy import Geom
    from abitaPy import Population
    from abitaPy import Algo
    geom = Geom()
    popu = Popu()
    algo = Algo(geom, popu)
    ```

2. Modifiez les paramètres de l'algorithme. Cette étape est facultative ; si
    vous ne redéfinissez pas les paramètres, ils prenennt leur valeur par défaut 
    montrée ci-après. Référez-vous à la doc de la class `Algo` pour plus d'info.
    ```python
    algo.nbSols = 100
    algo.initIT = -1
    algo.endIT = -1
    algo.alpha = 0
    ```

3. Définir les différents types de lots et les ajouter à l'agorithme. 
    Cette étape est facultative : si vous n'en créez aucun, les types suivants
    seront créés automatiquement. Référez-vous à la doc de la classe `Tx` pour 
    chaque paramètre.
    ```python
    from abitaPy import Tx
    algo.addType(Tx(benefit=70,  areaMin=30, areaMax=45,  nbMin=0, nbMax=1000, numero=1))
    algo.addType(Tx(benefit=80,  areaMin=45, areaMax=60,  nbMin=0, nbMax=1000, numero=2))
    algo.addType(Tx(benefit=100, areaMin=60, areaMax=75,  nbMin=0, nbMax=1000, numero=3))
    algo.addType(Tx(benefit=50,  areaMin=75, areaMax=85,  nbMin=0, nbMax=1000, numero=4))
    algo.addType(Tx(benefit=40,  areaMin=85, areaMax=100, nbMin=0, nbMax=1000, numero=5))
    ```

4. Créez un étage (obligatoire) : chaque étage est définit avec un numéro, 
    indiquant de quel étage il s'agit (rez-de-chaussée, 1er étage, etc...). On
    tient à jour à côté une variable `floorId`, indiquant le combien-ième étage
    on est en train de définir (cela est permet de conserver en mémoire l'index 
    de l'étage en cours de définition dans la liste des étages). `floorId` est
    complètement décorrelé du numéro de l'étage (même si souvent ils valent la
    même chose). On suppose `floorId` initialisé à `-1`.
    ```python
    from abitaPy import Floor
    geom.addFloor(Floor(no = 6))
    floorId += 1
    ```

5. Définissez les points de la géométrie (obligatoire), avec `x` et `y` les 
    coordonnées du point, `floorId` l'étage où le point se situe, et `no` le 
    numéro du point (servant d'identifiant unique)
    ```python
    from abitaPy import Point
    p1 = Point(x=0, y=0, floorId = floorId, no = 1)
    geom.addPoint(p1)
    p2 = Point(x=0, y=1, floorId = floorId, no = 2)
    geom.addPoint(p2)
    ...
    ```

6. Définissez les éléments (obligatoire), en indiquant l'étage (`floorId`), le 
    numéro (`no`), et les différents points précédemment définis :
    ```python
    from abitaPy import Element
    elt = Element(floorId = floorId, no = 1)
    elt.addPoint(p = p1)
    elt.addPoint(p = p2)
    ...
    geom.addElement(elt)
    ```

    Pour chaque élément, vous pouvez aussi indiquer un bonus (facultatif) :
    ```python
    elt.bonus = 3.14
    ```

    Pour chaque élément, vous pouvez définir le type de l'élement :
    * par défaut un élément est Libre (L)
    * pour définir un élément comme Commun (C) : 
        ```python
        elt.common = True
        ```
    * pour définir un élément comme Commun Imposé (I) : 
        ```python
        elt.common = True
        elt.imposed = True
        ```
    * pour définir un élément comme entrée-sortie (X) *(vous devez en définir au 
        moins un*) :
        ```python
        elt.common = True
        elt.imposed = True
        elt.exit = True
        ```

6. Initialisez la géométrie, la population et l'algorithme :
    ```python
    geom.build()
    for sol in popu.solutionList: 
        algo.evaluate(sol)
    popu.stats()
    ```

7. Exécutez l'algorithme avec la boucle suivante (vous pouvez mettre ce que vous
    voulez dans la boucle, par exemple afficher les statistiques) :
    ```python
    while algo.run():
        print(algo.currentIteration())
    print("Problem solved!")
    ```

8. Explorez les résultats :
    * l'élement `popu` précédemment défini contient un attribut `solutionList` 
        correspondant à la liste des solutions calculées
    * pour chaque solution `sol` de la liste, utilisez l'attribut `lotList` pour
        accéder à la liste des lots définissant la solution
    * pour chaque lot `lot`, accédez à l'attribut `elementList` pour accéder à 
        la liste des éléments définissant le lot.


9. Exportez les résultats dans un fichier .abi pour les lire dans le 
    visualiseur :
    ```python
    from abitaPy import AbiFile
    file = AbiFile("output.abi")
    file.write(geom, popu, algo)
    ```


## Contribuer

### Conversion du code Python3 vers Python2

* Installer la librarie `3to2` :
    ```bash
    pip install 3to2
    ```
* Exécutez le script de conversion :
    ```bash
    python3 convert3to2.py
    ```
* Cela crée alors un dossier `abitaPy2`, contenant le code source du programme
adapté à Python 2.7.

> Attention : certaines syntaxes des dernières versions de Python 3 ne sont pas
> prises en comptes par `3to2`. Veillez donc à toujours garder un code python3
> convertible (la référence étant la syntaxe de Python 3.5).
>
> De plus, ne modifiez jamais le code source d'`abitaPy2` : celui-ci n'est pas
> synchronisé sur le repository, et est automatiquement regénéré à chaque
> release.

### Développement avec SonarQube

Pour obtenir un code unifié, le projet utilise SonarQube pour analyser le code.
Pour l'utiliser, vous devez avoir installé `sonarqube` et `sonar-scanner` et 
avoir ajouté les commandes `StartSonar.bat` et `sonar-scanner` au PATH.

Pour faire une analyse du code via sonarqube :
1. Lancez le serveur sonarqube : exécutez `StartSonar.bat`, puis dans un 
    navigateur, ouvez [localhost:9000](http://localhost:9000).
1. Changez le profil qualité : dans l'onglet "Profils Qualité", sélectionnez 
    "Restaurer" puis importez le fichier `Profile4Abita.xml`. 
1. Toujours dans SonarQube, créez un nouveau projet localement et nommez-le 
    `abita` par exemple. Copiez le token généré.
1. Dans le menu "Project Settings" du projet, choissez "Profils Qualité", puis 
    cliquez sur le bouton "Change Profile" et sélectionnez le profil 
    "Profile4Abita".
2. De retour dans VScode, déplacez vous dans le dossier `AbitaPy`
3. Créez un fichier `sonar-project.properties` et remplissez-le avec le code 
    suivant, en remplaçant *YOUR_TOKEN_HERE* par le token copié précédemment :
    ```
    # must be unique in a given SonarQube instance
    sonar.projectKey=abita

    # defaults to project key
    sonar.projectName=abita
    # defaults to 'not provided'
    #sonar.projectVersion=1.0
    
    # Path is relative to the sonar-project.properties file. Defaults to .
    #sonar.sources=.
    
    # Encoding of the source code. Default is default system encoding
    sonar.sourceEncoding=UTF-8

    sonar.login=YOUR_TOKEN_HERE
    sonar.python.version=3.7
    ```
5. Toujours depuis le dossier `AbitaPy`, lancez la commande `sonar-scanner` 
    puis retournez dans le navigateur observer les résultats !
