---
name: coyote-network-reactivation
description: Construire et mener une campagne structurée de réactivation de contacts LinkedIn dormants (anciens collègues, anciens managers, anciens clients) perdus de vue depuis des années. À déclencher quand l'utilisateur parle de renouer avec d'anciens contacts, de réactiver son réseau, de recontacter d'anciens collègues, de constituer une liste de relations passées, de traiter un export CSV de connexions LinkedIn, de rédiger des messages de reprise de contact, ou demande comment réaborder quelqu'un qu'il n'a pas eu au téléphone depuis des années. Vaut aussi pour les formulations anglaises (reconnect with my network, reactivate LinkedIn contacts, warm outreach to former colleagues). À utiliser dès que quelqu'un veut renouer méthodiquement avec son réseau dormant plutôt qu'envoyer des messages au coup par coup, même sans employer le mot réactivation. La skill produit un système de tri, des modèles de messages appariés à cinq archétypes en FR et EN, et un déroulé qui privilégie la chaleur relationnelle sur la transaction.
---

# Réactivation réseau

Un système pour renouer avec des relations dormantes de façon à construire du capital relationnel au lieu de le brûler.

## Pourquoi ça compte

On accumule des centaines de relations professionnelles sur une carrière. La plupart refroidissent. Les trois erreurs classiques quand on essaie de les rallumer :

1. **L'énergie du message de masse.** Des accroches génériques (« J'espère que tu vas bien ! ») que le destinataire identifie en une seconde comme de l'envoi en nombre, et qu'il ignore.
2. **Le cadrage transactionnel.** Ouvrir sur une demande (un poste, une intro, un conseil) avant d'avoir rétabli la relation.
3. **L'absence de système.** Des messages au coup par coup, sans suivi, sans relecture, sans priorité. Au bout de trois semaines la campagne s'effondre.

Cette skill neutralise les trois : d'abord la structure, ensuite le contenu, avec une boucle de relecture intégrée.

## Le principe central

**Reconnecter d'abord. L'intention vient après.**

Toute accroche écrite sous cette skill est purement relationnelle. Zéro mention d'un poste, d'un projet, d'un produit ou de quoi que ce soit qu'on pourrait vouloir du contact. La relation se rétablit avant que la moindre demande ne soit posée. Ce n'est pas optionnel : c'est ce qui sépare cette approche des modèles de prospection déguisée.

## Les cinq archétypes

Les gens se situent différemment par rapport à vous selon le rapport de force d'origine. Une seule accroche ne peut pas couvrir les cinq cas :

1. **Ancien manager** (il vous était hiérarchiquement supérieur) : respectueux, ancré sur un moment précis qu'il a mené ou enseigné.
2. **Ancien pair** (même niveau, collaboration serrée) : chaleureux, d'égal à égal, souvenir de tranchée partagé.
3. **Ancien collaborateur direct** (vous l'avez managé) : orienté attention, on investit sur lui, on n'extrait rien.
4. **Ancien client** (il a payé pour votre travail) : non transactionnel, la preuve de non-demande se fait dans l'accroche.
5. **Transverse ou éteint** (connaissance lointaine) : sans pression, avec une porte de sortie intégrée.

Les modèles par archétype, en FR et EN, sont dans `templates/dm-templates.md`.

## Déroulé

### Phase 1 : poser l'infrastructure de suivi

Avant toute prise de contact, créer une base (Notion, Airtable, ou même un tableur structuré) avec ces champs :

**Identité** : Nom, Poste actuel, Entreprise actuelle, URL LinkedIn
**Historique relationnel** : Où on s'est connus (nom de l'entreprise), Époque, Son poste à l'époque, Type de relation (manager / pair / collaborateur direct / client / transverse), Force du lien (fort / tiède / éteint)
**Géo et densité** : Géo (Paris / Londres / Bordeaux / etc.), Nombre de relations communes
**État de la prise de contact** : Statut (À trier / À contacter / Message envoyé / Réponse reçue / Échange calé / Relation active / Hors d'atteinte), Priorité, Date du dernier contact, Date d'envoi du message, Notes
**Couche de relecture** : Relu par le coach (case à cocher), Commentaire du coach

Un modèle Notion prêt à l'emploi est décrit dans `references/notion-template.md`.

### Phase 2 : constituer la liste

Deux sources complémentaires, à mener en parallèle :

**A. Export CSV LinkedIn (la largeur)**
1. Préférences et confidentialité → Confidentialité des données → Obtenir une copie de vos données → cocher « Relations » uniquement → Demander l'archive.
2. LinkedIn envoie le CSV par e-mail en une dizaine de minutes.
3. Le CSV contient : First Name, Last Name, URL, Email Address, Company, Position, Connected On.

**B. Vidage de mémoire (la profondeur)**
Pour chaque chapitre de votre carrière (employeur, client, projet), listez les gens avec qui vous avez réellement travaillé au quotidien. Les noms qui remontent sans effort sont les plus chauds. Les souvenirs flous (« Maria quelque chose, designer ») comptent aussi : le CSV comblera les trous.

### Phase 3 : classer et trier

Avec le script `scripts/classify-csv.py` (ou à la main), enrichir chaque ligne du CSV :
- `Où on s'est connus` à partir du champ Company confronté à l'historique de carrière fourni en entrée.
- `Époque` à partir de la date `Connected On`.
- Toutes les entrées démarrent en `Statut = À trier` et `Force = tiède`.

Après classement, l'utilisateur passe la file de tri et fixe :
- `Force du lien` (Fort / Tiède / Éteint)
- `Priorité` (Haute / Moyenne / Basse)
- `Type de relation` (Manager / Pair / Collaborateur direct / Client / Transverse)

C'est une passe manuelle : seul l'utilisateur connaît le contexte relationnel. Ne jamais déduire le type de relation du seul intitulé de poste.

### Phase 4 : rédiger les messages

Pour chaque entrée `À contacter`, prendre le modèle correspondant dans `templates/dm-templates.md` et remplir les variables entre crochets :
- `[Prénom]`
- `[moment précis]` : un souvenir partagé concret, jamais générique
- `[entreprise actuelle]`
- Pour un ancien manager : une chose précise qu'il a enseignée ou tranchée
- Pour un ancien pair : un moment de tranchée partagé
- Pour un ancien collaborateur direct : un moment précis qui a forcé le respect
- Pour un ancien client : un résultat concret de la mission

Si vous ne parvenez pas à ancrer le message sur un souvenir précis, soit le contact est trop éteint pour un message chaleureux (passer à l'archétype 5, la réintroduction), soit il faut le sauter.

### Phase 5 : la boucle de relecture

Avant l'envoi, faire relire chaque message par un coach (coach visibilité LinkedIn, mentor, ou simplement un pair exigeant). Le relecteur attrape :
- Les accroches génériques passées entre les mailles
- La demande glissée par accident dans la clôture
- Le décalage de ton avec la relation d'origine
- Les détails « précis » qui sonnent fabriqués

Ne sautez pas cette étape. L'auto-relecture échoue parce que l'auteur est trop près de ses propres mots.

### Phase 6 : envoyer et suivre

Après validation :
1. Envoyer le message.
2. Mettre à jour le suivi : `Statut = Message envoyé`, renseigner la date d'envoi.
3. Consigner toute réponse : `Statut = Réponse reçue`.
4. Si un échange se cale : `Statut = Échange calé`.
5. Après la première vraie conversation : `Statut = Relation active`.

### Phase 7 : gérer la réponse

Quand un contact répond, c'est au deuxième message que la plupart des campagnes meurent. On se fige, on retombe sur « on se prend un café ? », et la chaleur retombe.

Les règles de réponse par archétype sont dans `templates/dm-templates.md`. Le principe général : poser une question sur *son* travail à lui avant de proposer quoi que ce soit sur le vôtre. Laissez-le ouvrir la porte s'il en a envie. Ne poussez jamais.

## Les anti-patterns à refuser

En rédigeant des messages sous cette skill, refusez de produire ce qui suit :

1. **Les accroches génériques** : « J'espère que tu vas bien ! », « Ça fait un bail ! », « Bonjour [prénom], je suis tombé sur ton profil et je me permets de te contacter ». Le destinataire les reconnaît comme de l'envoi en nombre et supprime en cinq secondes.
2. **Un lien CV, portfolio ou Calendly dans l'accroche** : un seul lien tue la chaleur. L'accroche est du texte, rien d'autre.
3. **Mention d'une mission, d'un poste ou d'un produit dans le premier message** : à garder pour après la réponse, ET seulement s'il demande ce que vous faites.
4. **La clôture « on se prend un café ? »** : elle crée une obligation. Préférer « curieux de savoir ce que tu deviens ».
5. **S'excuser d'avoir perdu le contact** : ça vous rabaisse. Le dire neutrement ou ne pas le dire.
6. **Le monologue sur sa propre vie** : il n'a rien demandé. Une phrase maximum sur vous, tout le reste porte sur lui ou sur le passé commun.

Si l'utilisateur demande un message qui enfreint l'un de ces points, opposez une objection une fois, avec la raison, et proposez la version corrigée.

## Format de sortie des messages

Présentez toujours les brouillons ainsi, pour que l'utilisateur puisse copier-coller directement dans LinkedIn :

```
=== [Nom du contact] · [Archétype] ===

[Contrôle avant envoi]
- Ancrage : [le souvenir précis sur lequel le message accroche]
- Longueur : [nombre de mots]
- Vérifications : ✓ pas d'accroche générique, ✓ aucune demande, ✓ ancrage précis, ✓ clôture sans pression

[Corps du message, à copier à partir d'ici]
Salut [Prénom],

...

À très vite,
[Votre prénom]
[Fin du message]

[Note de gestion de réponse]
S'il répond : [conseil propre à l'archétype]
```

## Périmètre

Cette skill couvre :
- La conception du schéma de base pour le suivi relationnel
- La lecture et le classement d'un export CSV LinkedIn
- La rédaction de messages sur cinq archétypes, en FR et EN
- Le déroulé de relecture par un coach
- La conduite de la réponse

Cette skill ne couvre pas :
- La prospection à froid vers des gens jamais rencontrés (autre méthodologie, ne pas réutiliser ces modèles)
- La prospection commerciale (transactionnelle par nature, cadrage inverse)
- L'approche de recruteurs (utiliser un modèle dédié, pas ceux-ci)

## Références

- `templates/dm-templates.md` : les modèles complets, 5 archétypes × FR et EN, plus la gestion de réponse
- `references/notion-template.md` : le schéma de base et les 4 vues recommandées
- `references/anti-patterns.md` : les anti-patterns détaillés, avec exemples avant/après
- `scripts/classify-csv.py` : script optionnel pour classer en masse un export CSV LinkedIn contre un historique de carrière fourni
