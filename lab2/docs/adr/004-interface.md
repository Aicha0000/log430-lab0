# ADR-004: Stratégie d'interface utilisateur: Console + Web minimal

## Status
Acceptée par Aicha Aanounou

## Date 
30 Mai 2025

## Context
Deux types d'utilisateurs identifiés avec besoins différents : employés de magasin nécessitant rapidité d'exécution (ventes, consultation stocks UC2) et gestionnaires maison mère nécessitant visualisations consolidées (rapports UC1, tableaux bord UC3, interface web UC8).

## Décision
Console pour employés magasins (continuité de ce que j'avais déjà implémenté au labo 1) + Interface web minimale pour gestionnaires maison mère + API REST pour communication inter-services. 

## Alternatives considérées
- uniquement console : Inadéquat pour UC8 "interface web minimale" requise
- uniquement une interface web : Perte du travail Lab 1, moins efficace pour employés magasins

## Justification
Le cas d'utilisation UC8 impose une "interface web minimale pour gestionnaires" et la console conservée pour employés magasins (continuité Lab 1) permet une rapidité opérationnelle. De plus, cette séparation des interfaces selon les rôles utilisateurs optimise l'expérience et renfonrce l'approche DDD.

## Conséquences positives ou négatives acceptées
- Réutilisation de la console du labo1 (simplicité), renforce l'approche DDD avec l'assignation d'une interfaces optimisées par type d'utilisateur
- Maintenance de deux interfaces différentes, Tests d'intégration plus complexes
