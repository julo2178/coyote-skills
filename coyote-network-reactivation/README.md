# Réactivation réseau · une skill Claude

Un système pour renouer avec des relations professionnelles dormantes de façon à construire du capital relationnel au lieu de le brûler.

## Ce qu'il y a dans la boîte

```
coyote-network-reactivation/
├── SKILL.md                          Le fichier principal, celui que Claude lit
├── templates/
│   └── dm-templates.md               5 archétypes × FR et EN, plus la gestion de réponse
├── references/
│   ├── notion-template.md            Schéma de base et vues recommandées
│   └── anti-patterns.md              Ce qui tue un message, avec exemples avant/après
└── scripts/
    ├── classify-csv.py               Classement en masse d'un export CSV LinkedIn
    └── career.example.json           Exemple d'historique de carrière pour le script
```

## Installation

### Option 1 : installer la skill dans Claude

1. Récupérez le fichier `network-reactivation.skill` dans la dernière release de ce dépôt.
2. Sur Claude.ai : Paramètres → Capacités → Compétences → importer le fichier. Dans Claude Code : déposez le dossier dans votre répertoire de skills.
3. Déclenchez-la en disant quelque chose comme « aide-moi à renouer avec mon ancien réseau », « je veux réactiver mes contacts LinkedIn », ou « écris un message à un ancien manager que je n'ai pas eu depuis 5 ans ».

### Option 2 : utiliser la méthode directement

Tout est lisible en clair. Ouvrez `SKILL.md` et suivez le déroulé en 7 phases sans Claude. Les modèles et le document d'anti-patterns fonctionnent seuls.

## Le principe central

**Reconnecter d'abord. L'intention vient après.**

Toute accroche est purement relationnelle. Zéro mention de poste, de projet, de produit ou de demande. La relation se rétablit avant que quoi que ce soit ne soit demandé. C'est ce qui sépare cette approche des modèles de prospection déguisée.

## Les 5 archétypes

Les gens se situent différemment par rapport à vous selon le rapport de force d'origine :

| Archétype | Ton |
| --- | --- |
| Ancien manager | Respectueux, ancré sur ce qu'il a enseigné ou tranché |
| Ancien pair | Chaleureux, d'égal à égal, souvenir de tranchée |
| Ancien collaborateur direct | Orienté attention : on investit, on n'extrait pas |
| Ancien client | Non transactionnel, la non-demande doit être prouvée |
| Transverse ou éteint | Sans pression, porte de sortie intégrée |

Une seule accroche ne peut pas couvrir les cinq. C'est la raison d'être des modèles.

## Les 7 phases

1. Poser l'infrastructure de suivi
2. Constituer la liste (export CSV LinkedIn + vidage de mémoire)
3. Classer et trier
4. Rédiger les messages à partir des modèles
5. Faire relire par un coach
6. Envoyer et suivre
7. Conduire la réponse

Détail complet dans `SKILL.md`.

## Le script de classement

`scripts/classify-csv.py` prend un export `Connections.csv` de LinkedIn et votre historique de carrière au format JSON, et produit un CSV enrichi prêt à importer dans Notion ou Airtable. Il classe automatiquement le champ « Où on s'est connus » en confrontant l'employeur du contact à vos anciens employeurs, et range les contacts par époque à partir de la date de mise en relation.

```bash
python scripts/classify-csv.py \
  --csv connections.csv \
  --career mon-parcours.json \
  --output enrichi.csv
```

La revue manuelle reste indispensable : le type de relation, la géo, la priorité et la force du lien relèvent tous du jugement humain.

## Crédits

Construit par Julien Amar, Coyote Consulting, en avril 2026, à partir d'une campagne réelle de réactivation menée sur un réseau de plus de vingt ans.

## Licence

MIT. Servez-vous, partagez, forkez. Sans garantie. Si vous construisez par-dessus, une mention fait plaisir mais n'est pas exigée.
