# Modèle Notion · Suivi de réactivation réseau

La structure de base recommandée pour piloter une campagne de reprise de contact.

## Schéma de la base

| Champ | Type | Options / Notes |
| --- | --- | --- |
| Nom | Titre | Nom complet du contact |
| Poste actuel | Texte | Ce qu'il fait aujourd'hui |
| Entreprise actuelle | Texte | Son employeur du moment |
| URL LinkedIn | URL | Le lien vers son profil |
| Où on s'est connus | Sélection | À remplacer par vos propres chapitres : un choix par employeur, client ou projet marquant, plus « Client » / « Perso » / « Autre » |
| Époque | Sélection | Avant 2010 / 2010-2015 / 2015-2020 / 2020-2024 / 2024+ |
| Son poste à l'époque | Texte | Ce qu'il faisait quand vous travailliez ensemble |
| Type de relation | Sélection | Manager / Collaborateur direct / Pair / Transverse / Client / Prestataire / Autre |
| Force du lien | Sélection | 🟢 Fort / 🟡 Tiède / ⚪ Éteint |
| Géo | Sélection | Paris / Londres / Bordeaux / Autre France / Autre UK / Autre UE / Reste du monde / Inconnu |
| Relations communes | Nombre | Le compteur LinkedIn, utile pour les chaînes d'intro |
| Statut | Sélection | 📋 À trier / 🎯 À contacter / 💬 Message envoyé / 🔄 Réponse reçue / ☕ Échange calé / ✅ Relation active / ❌ Hors d'atteinte |
| Priorité | Sélection | 🔥 Haute / 🟡 Moyenne / ⚪ Basse |
| Dernier contact | Date | Le dernier échange réel |
| Date d'envoi | Date | Quand le message de reprise est parti |
| Ancrage mémoire | Texte | Le souvenir précis sur lequel le message va accrocher. Le champ le plus important de la base. |
| Notes | Texte | Contexte libre |
| Relu par le coach | Case à cocher | Cochée une fois le message validé |
| Commentaire du coach | Texte | Ses corrections ou remarques |
| Créé le | Date de création | Automatique |

**Le champ qui fait la différence** : `Ancrage mémoire`. Notez-le au moment du tri, pendant que le souvenir est frais. Une entrée sans ancrage n'est pas prête à être contactée, elle est encore à trier.

## Les vues recommandées

### 1. 📋 File de tri (vue par défaut, tableau)

Filtre : `Statut = 📋 À trier`
Tri : `Force du lien` croissant, puis `Créé le` décroissant
Colonnes : Nom, Poste actuel, Entreprise actuelle, Où on s'est connus, Force du lien, Géo, Relations communes, Ancrage mémoire

C'est là qu'atterrissent les nouvelles entrées avant traitement, et là que commence chaque séance de tri.

### 2. 🏢 Par chapitre (tableau kanban)

Regroupement : `Où on s'est connus`
Tri : `Force du lien` croissant
Colonnes : Nom, Poste actuel, Entreprise actuelle, Époque, Force du lien, Statut

Permet de voir ensemble tous les contacts d'un même employeur ou d'un même client. Utile pour préparer une séance concentrée sur un seul chapitre de votre parcours : la mémoire remonte par grappes, pas contact par contact.

### 3. 🔄 Pipeline de contact (tableau kanban)

Regroupement : `Statut`
Tri : `Priorité` croissante, puis `Date d'envoi` décroissante
Colonnes : Nom, Entreprise actuelle, Où on s'est connus, Priorité, Dernier contact, Date d'envoi

Vue kanban : À contacter → Message envoyé → Réponse reçue → Échange calé → Relation active. C'est le pouls opérationnel de la campagne.

### 4. 👥 File de relecture (tableau)

Filtre : `Relu par le coach` décoché ET `Statut` différent de `📋 À trier`
Tri : `Priorité` croissante
Colonnes : Nom, Entreprise actuelle, Où on s'est connus, Priorité, Statut, Notes

Ne fait remonter que les entrées travaillées mais pas encore relues. Vous envoyez le lien au coach, il déroule cette vue, vous envoyez après validation.

## Comment l'installer

**Option 1 : dupliquer le modèle public (2 minutes)**

Ouvrez le modèle public partagé avec cette skill et cliquez sur « Dupliquer » en haut à droite. La base arrive dans votre espace, vide, avec les quatre vues déjà configurées.

**Option 2 : à la main (15 minutes)**

Créez une base Notion avec le schéma ci-dessus et ajoutez les quatre vues. Rien de plus.

Dans les deux cas, la première chose à faire est de remplacer les options de `Où on s'est connus` par vos propres chapitres de carrière. C'est ce champ qui fait tourner le classement automatique du script CSV.

## Conseils d'usage

- **Ne cherchez pas une base propre.** C'est un outil de travail, pas une archive. Les entrées floues (« Maria, designer vers 2020 ») ont de la valeur : l'import CSV comblera beaucoup de trous tout seul.
- **Triez par lots, pas au goutte-à-goutte.** Réservez trente minutes une fois par semaine pour faire passer vingt à trente contacts de `📋 À trier` vers `🎯 À contacter` ou `❌ Hors d'atteinte`. Travailler la base tous les jours devient vite pénible.
- **La relecture n'est pas optionnelle.** La vue `👥 File de relecture` existe pour ça. L'auto-relecture ne tient pas à cette échelle.
- **Le statut donne le rythme.** Mettez-le à jour au moment où la chose arrive (message parti, réponse reçue, échange calé). Un statut périmé égale une campagne morte.
