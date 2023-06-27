# Abita4Rhino

<img src="../logos/logo_abita4rhino.png" alt="" width="400px">
<br><br>

*Guide d'installation du projet Abita4Rhino sous Rhino et Grasshopper*

## Installation rapide pour Rhino 7

1. Téléchargez la dernière version de l'archive `Abita4Rhino.zip` sur la page
    des releases: [https://github.com/hydrielax/Abita/releases](https://github.com/hydrielax/Abita/releases)
2. Décompressez l'archive
3. Exécutez le script `install.bat` en double-cliquant dessus : cela copie
    les libraries python dans le dossier IronPython de Rhino7, et les
    composants Grasshopper dans le dossier par défaut.
4. Vous pouvez alors démarrer Rhino puis Grasshopper : les composants
    d'Abita4Rhino devraient apparaître dans la barre d'outils !

## Installation détaillée

Dans ce guide, nous allons détailler comment procéder à l'installation manuelle
des composants nécessaires à l'utilisation du projet.

L'installation du projet néccessite d'avoir Rhino 7 ainsi que Grasshopper 
d'installés. 

### 1. Téléchargement du code source

Téléchargez la dernière version de l'archive `Abita4Rhino.zip` sur la page
des releases: [https://github.com/hydrielax/Abita/releases](https://github.com/hydrielax/Abita/releases), puis décompressez l'archive sur votre ordinateur.

### 2. Copie des libraries Python

Pour que Rhino puisse exécuter la librarie python AbitaPy (contenant le code
source du programme), il est nécessaire d'ajouter la librarie ainsi que ses
dépendances au plug-in *IronPython* de *Rhino* (version 7 de préférence).

Copiez et collez tout le contenu du dossier `Libraries` du dossier précédemment
téléchargé dans le dossier des libraries IronPython de *Rhino* :
`C:\Program Files\Rhino 7\Plug-ins\IronPython\Lib`. Le chemin peut être
légèrement différent selon votre configuration.

### 3. Copies des composants Grasshopper

Une fois les libraries python installés, on peut lancer Rhino puis Grasshoper. 
Nous allons alors copier les composants Grasshopper d'Abita4Rhino dans le
dossier par défaut de Grasshopper pour les rendre accessible par le logiciel : 
  - Dans une fenêtre Grasshopper, ouvrez l'onglet `File`
  - Sélectionnez `"Special Folders"` puis `"User Object Folder"`
  - Le dossier contenant les modules personnalisés de Grasshopper s'ouvre. 
    Copiez-collez alors tous les fichiers .ghuser du dossier 
    `Abita4Rhino/UserObjects` dans ce dossier.
  - C'est terminé ! Si l'installation est réussie, vous devriez voir un nouvel 
    onglet `Abita` de plus dans  la barre d'outils de Grasshopper, qui 
    contient les composants propres à `Abita4Rhino`.

## Utilisation

Voir le document `Guide Utilisateur.pdf`.

### Puis-je utiliser *Abita4Rhino* avec un autre logiciel que *Rhino* ?

*Abita4Rhino* s'exécute sur Grasshopper et IronPython. Si votre logiciel intègre
aussi IronPython, alors vous pouvez en théorie utiliser les composants de
*Abita4Rhino* dans votre logiciel. 

Néanmoins, veuillez noter que les composants de *Abita4Rhino* ne pourront pas
communiquer avec votre logiciel principal : en effet, les composants ne prennent
en charge que la conversion des objets Python vers des objets Rhino, et pas vers
d'autres logiciels. Vous pourrez toujours néanmoins importer et exporter vos
calculs avec les fichiers `.abi` au sein de Grasshopper.

## Contribuer

Pour modifier les composants `.ghuser` :
* Ajoutez un composant existant ou créez un nouveau composant dans le plan de 
  travail de Grasshopper
* Double-cliquez dessus pour ouvrir le code et modifiez-le, puis sauvegardez
  et quittez.
* Sélectionnez le bloc modifié (sans l'ouvrir).
* Sélectionnez `File` > `Create UserObject`.
* Une boîte de dialogue s'ouvre : vous pouvez changer les propriétés du
  composant.
* Valiez. Le composant est enregistré dans le `UserObjects` folder!
