# 3I_SI4 : Projet Tron

## Objectifs

À partir du jeu Tron validé, il faut implémenter les fonctionnalitées suivantes :

* Plusieurs IA sur le terrain.
* Agrandir le décor.
* Faire de nouveau décor.
* Ajout de téléporteur.

## Fonctionnalitées réalisées

Afin d'implémenter ces améliorations, nous avons réalisé les tâches suivantes :

* Séparation des parties principales du jeu en fichier (logique / affichage / IA).
* Respect au mieux de la convention PEP8 avec pylint.

Après cela, nous avons implémenté dans l'ordre :

* Plus grand décor avec des cases plus grandes (pour plus de visibilité).
* Nouveaux niveaux avec une sélection aléatoire. 
* La téléportation de l'IA si celle-ci se trouve sur un téléporteur.
* Ajout d'une seconde IA.

## Axes d'améliorations

Il est toujours possible d'améliorer le jeu en améliorant les points suivants :

* Prendre en compte les téléporteurs dans l'algorithme vectoriel. L'algorithme ne prend pas encore en compte si le le joueur est sur un téléporteur et ne simule pas la téléportation.
* Modifier la structure Game pour faire une liste de joueurs et ne plus 'hardcoder' le nombre de joueurs ce qui pourra permettre de faire jouer N joueur (en n'oubliant pas l'affichage).
* Lors de la simulation faire jouer les N IA en même temps. Actuellement, on lance une simulation pour chaque IA ce qui cause de gros problème de performance. Afin d'atténuer ceux-ci, on pourrait faire en sortie que la simulation gère les différentes IA en même temps et retourne un tableau de score à la place.
