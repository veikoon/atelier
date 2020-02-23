# atelier de E2 : IA et jeux

## Bomberman

### Explications
Ce projet a été réalisé dans le cadre d'un projet de deuxième année à l'ESIEE Paris
Il s'agit d'une copie du jeu Bomberman mettant en scene un joueur se déplacant avec les flèches du claviers, aini que 3 ia, avec des caractères différents :
- IA tueuse : Cette IA a pour unique but de tuer le joueur humain, quelques soit la postion des autres IA
- IA froussarde : Cette IA très peureuse joue plus sur la défenisive et casse les blocs pour récuperer un maximum de bonus, tout en cherchant à s'éloigner le plus possible des autres joueurs
- IA complète : Cette IA a pour objectif de tuer les autres joueurs, qu'ils soint IA ou humain, ramasser un maximum de bonus, tout en survivant le plus longtemps possible.

### Installation
``` bash
	$ git clone https://github.com/veikoon/atelier.git
	$ cd atelier/
	$ pip install -r requirements.txt
	$ python3 main.py
```
### Commandes du jeu
Il y a une page de commandes accessible directiement sur le menu du jeu, en appuyant sur la fflèche du bas et en appuyant sur entrée.
Les commandes sont:
-ESPACE: Poser des Bombes
-Flèches directionnelles pour se deplacer
Le but étant de tuer les autres IA avec les bombes en s'aidant si l'on veut des différents bonus cachés dans les briques
### Bugs reports
Une section dédiée aux bugs reports se trouve dans le dossier .github
