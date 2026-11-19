# Harvey, l'agent Claude Code qui prospecte : ce qu'il faut savoir avant de l'installer

> Les vrais prérequis, les réglages à changer en France, ce que dit la CNIL et ce qui nous inquiète sur l'abonnement. Lecture du dépôt au 4 novembre 2026 : on ne l'a pas lancé.

Abyane Nabeebaccus, Eigenflow. Publié le 04/11/2026, mis à jour le 04/11/2026. Lecture : 7 min.  
Page : https://eigenflow.fr/fr/guides/harvey-agent-prospection-claude-code  
PDF : https://eigenflow-leads.vercel.app/harvey-agent-prospection-claude-code.pdf

## L'essentiel en 30 secondes

- On n’a pas lancé Harvey. Ce guide vient de la lecture du dépôt le 4 novembre 2026 : le README, le fichier de configuration, le code du score, le journal des versions. Aucun email n’est parti de chez nous, et on ignore ce que ça rapporte.
- Tous les noms, chiffres et captures viennent de la démo du projet. Elle est inventée par ses auteurs : une entreprise fictive, Bookwell, qui vend de la prise de rendez-vous en ligne à des couvreurs, des dentistes et des chauffagistes.
- Harvey est un projet open source sous licence MIT, créé le 12 mars 2026. Au 4 novembre : 4 358 étoiles, 911 forks, dernière version publiée 0.3.0. Eigenflow n’a aucun lien avec ses auteurs ni avec Anthropic.

## Le guide · Ce qu’il y a dans ce guide

Tu as commenté HARVEY. Le dépôt est ici : https://github.com/ethanplusai/harvey. Le reste de ce guide, c’est ce qu’on aurait voulu lire avant de l’installer, surtout depuis la France, où deux réglages par défaut ne te conviennent pas.

## Partie 1 · Ce qu’il fait, sans le vernis

Harvey tourne sur ton ordinateur et se réveille toutes les 15 minutes. À chaque réveil, il regarde s’il est dans ses heures calmes, vérifie son budget, choisit quoi faire, le fait, le note et se rendort. Le choix suit un ordre fixe, sans appel au modèle : répondre, envoyer, écrire, prospecter.

Le reel d’origine dit « 24/7 ». Par défaut, c’est faux : Harvey dort de 22 h à 7 h, et il s’arrête avec ta machine.

Son travail tient en quatre étapes :

- Trouver des entreprises. La source par défaut est OpenStreetMap, gratuite et sans compte. Le README prévient qu’elle couvre mal les métiers sans vitrine : moins de 2 000 couvreurs sur tous les États-Unis. Il existe des sources payantes, à partir d’environ 0,37 $ les 1 000 résultats.
- Lire leurs sites. Trois requêtes par site, sans appel au modèle, donc sans coût.
- Les noter de 0 à 100 : secteur 20 points, décideur identifié 30, adresse joignable 25, signal d’achat 25.
- Écrire, puis suivre les réponses. Le modèle rédige à partir de ce qui a été trouvé sur l’entreprise.

## Partie 2 · « Gratuit », mais pas tout à fait

Le logiciel est gratuit. Faire partir de vrais emails demande ceci :

- Claude Pro ou Max, avec Claude Code connecté. Les appels au modèle passent par ton abonnement, sans clé API. Par défaut, Harvey se limite à 80 % de ton quota.
- Une boîte mail sur un domaine secondaire dédié, jamais ton domaine principal. Le README compte environ 7 $ par mois chez Google Workspace, plus le prix du domaine.
- Un service de préchauffage. Le README recommande TrulyInbox, avec un lien qui porte le paramètre **via=harvey**. Pour le connecter à Harvey, il faut au moins son offre Starter.
- SPF, DKIM et DMARC configurés sur ce domaine.
- Deux à quatre semaines de préchauffage avant un vrai volume, puis 10 à 20 envois par jour au départ. C’est ce qui nous a le plus refroidis en lisant : entre l’installation et le premier vrai volume, il faut compter au moins deux semaines.

## Partie 3 · L’installer

Il te faut Python 3.11 ou plus. La voie la plus simple selon le README :

**Terminal**

```text
git clone https://github.com/ethanplusai/harvey.git
```

**Terminal**

```text
cd harvey
```

**Terminal**

```text
claude
```

Puis tu dis à Claude :

**À coller**

```text
set up Harvey for me
```

Le dépôt contient un **CLAUDE.md** qui transforme Claude Code en assistant d’installation. C’est du code tiers qui tourne sur ta machine avec ta connexion : lis-le avant, et ne le mets pas dans un dossier qui contient autre chose. On n’a pas rejoué ces commandes.

Ensuite, trois commandes font l’essentiel. **harvey train** apprend ton produit depuis ton site et écrit **harvey.local.yaml**. **harvey signals --confirm free** valide les 26 signaux gratuits sur 29. **harvey discover** cherche les entreprises.

**À coller**

```text
harvey train https://ton-site.fr
```

**À coller**

```text
harvey signals --confirm free
```

**À coller**

```text
harvey discover
```

## Partie 4 · Ce qu’il faut changer en France

Ces points viennent de la lecture du dépôt, on ne les a pas éprouvés.

- Le fuseau. Dans **harvey.yaml**, **usage.quiet_hours.timezone** vaut **America/New_York**. Sans changement, ses heures calmes tombent de 4 h à 13 h à Paris. Mets **Europe/Paris**.
- La phrase de désinscription. Par défaut, elle est en anglais : « Not interested? Reply "no thanks" ». Le commentaire du fichier demande de garder des mots qu’il reconnaît. Le journal des versions annonce la détection de l’espagnol sans passer par le modèle, et on n’a trouvé aucune trace du français dans le dépôt. Avant tout envoi, teste une réponse comme « merci de me retirer » et vérifie qu’il l’arrête.
- La validation. **channels.email.require_approval** vaut **true**. Laisse-le ainsi. Le mode automatique s’active à part, en tapant **autopilot** dans les réglages.
- La liste d’exclusion. Remplis **compliance.do_not_contact** avec tes clients et tes concurrents avant le premier lancement.

## Partie 5 · Rien ne part sans toi, par défaut

C’est le meilleur choix du projet. Chaque email attend dans une boîte d’envoi, et tu valides un par un avec les touches **A** pour approuver, **R** pour rejeter. L’écran montre à côté du texte ce que Harvey a trouvé sur l’entreprise, donc tu peux vérifier d’où vient la phrase personnalisée.

Avant l’envoi, un contrôle sans modèle rejette les balises non remplies, les emails trop longs, les liens en trop et les adresses qui ne collent pas à la fiche. Et **harvey sending pause** coupe tout.

![La boîte d’envoi de la démo : l’email, ce que Harvey sait de l’entreprise, Approve, Edit, Reject.](https://eigenflow.fr/guides/harvey-agent-prospection-claude-code/outbox.jpg)

*La boîte d’envoi de la démo : l’email, ce que Harvey sait de l’entreprise, Approve, Edit, Reject.*

Le tableau de bord tourne en local, à l’adresse **127.0.0.1:5555**. La page Today rassemble ce qui attend ta décision.

![La page Today de la démo : contacts trouvés, emails envoyés, conversations, et les contacts par étape.](https://eigenflow.fr/guides/harvey-agent-prospection-claude-code/today.jpg)

*La page Today de la démo : contacts trouvés, emails envoyés, conversations, et les contacts par étape.*

Quand une réponse sort de son cadre, il te rend la main. Dans la démo, un prospect demande un contrat : Harvey s’arrête et te laisse répondre.

![Une conversation rendue à l’humain dans la démo : le prospect veut voir le contrat.](https://eigenflow.fr/guides/harvey-agent-prospection-claude-code/conversations.jpg)

*Une conversation rendue à l’humain dans la démo : le prospect veut voir le contrat.*

## Partie 6 · Le droit français, d’après la CNIL

Tu restes l’expéditeur, et le README le dit noir sur blanc. La page de la CNIL sur la prospection par email (datée du 10 juin 2026) pose ces règles :

- Entre professionnels, pas de consentement préalable. Il faut que la personne soit informée et puisse s’opposer simplement et gratuitement, et que le message ait un rapport avec son métier. Présenter un logiciel à un directeur informatique convient. Un message sans lien avec son poste, non.
- Si tu n’as pas collecté l’adresse toi-même, tu dois t’assurer que la personne a été informée de cet usage et peut s’y opposer. C’est le point délicat avec un outil qui récupère les adresses sur les sites.
- Les adresses génériques (**contact@**, **info@**) concernent des personnes morales et échappent à ces principes, selon la même page.
- Vers des particuliers, il faut un consentement préalable, sauf exceptions étroites.
- Chaque message doit donner l’identité de l’expéditeur et un moyen simple de refuser la suite.

La page ne parle pas des micro-entrepreneurs ni des entrepreneurs individuels. Or ce sont exactement les petites structures que Harvey sait viser. Pose la question à un juriste avant d’envoyer du volume. Ce guide n’est pas un conseil juridique.

Le dépôt propose un contrôle optionnel, Precleared, qui vérifie chaque adresse avant le premier email et dit couvrir les règles françaises. Il transmet l’adresse et, s’il les a, le nom de la personne et de l’entreprise à ce service. On ne l’a pas essayé.

## Partie 7 · Ton abonnement Claude : ce qui nous inquiète

Harvey appelle le programme **claude** avec ta connexion, en boucle, sans que tu sois devant. Le README renvoie la question à toi : vérifie les conditions et les limites de ton fournisseur.

On les a lues le 4 novembre. La page d’Anthropic sur Claude Code dit que les limites annoncées supposent un « ordinary, individual usage » et que l’entreprise peut agir sans préavis. Les conditions grand public interdisent l’accès par des moyens automatisés, sauf avec une clé API ou avec une permission explicite. Rien ne traite clairement le cas d’une boucle lancée par ton propre programme sur ta propre machine.

Franchement, ça nous inquiète pour un compte sur lequel tu travailles tous les jours. Si tu tiens à ton abonnement, lis ces deux pages avant le premier **harvey run**, et n’en attends pas une garantie.

## Partie 8 · Ce qu’on ne sait pas

- Le taux de réponse. Le dépôt ne donne aucun résultat réel, et nos captures sont une démo.
- La qualité de ses emails en français.
- La couverture d’OpenStreetMap en France pour ton métier. Les chiffres du README portent sur les États-Unis.
- Comment il se comporte sur plusieurs semaines, et ce que ça consomme de ton quota.

Si tu l’essaies, commence par une liste d’une dizaine d’entreprises, relis tout à la main et regarde ce qui part. Le reel le montre en 30 secondes. Le faire proprement prend plusieurs semaines.

## Auteur et méthode

**Abyane Nabeebaccus**. Fondateur d’Eigenflow. On construit des agents et des automatisations IA pour les PME et les indépendants.

Méthode : lecture du dépôt le 4 novembre 2026 (README, harvey.yaml, fit.py, journal des versions), page GitHub capturée le jour même. Harvey n'a pas été lancé. Les captures du tableau de bord sont celles du dépôt, avec ses données de démo inventées. Sources : page de la CNIL sur la prospection par email (10 juin 2026), page Legal and compliance de Claude Code et conditions grand public d'Anthropic, lues le 4 novembre.

## On branche ta prospection avec toi.

On regarde si un agent convient à ton entreprise, on l'installe et on garde la validation humaine là où elle compte.

- Démarrer un projet : https://eigenflow.fr/fr/candidature
- Réserver un appel : https://eigenflow.fr/fr/booking

## Les autres guides

- [Les 6 pièges juridiques d'une app faite avec l'IA : le prompt testé et les vrais textes](https://eigenflow.fr/fr/guides/pieges-juridiques-app-ia) (Claude)
- [42 choses à installer dans Claude : les commandes, les liens et mes vrais chiffres](https://eigenflow.fr/fr/guides/42-choses-installer-claude) (Claude)
- [L’art du Claude maxxing : la config complète en cinq niveaux](https://eigenflow.fr/fr/guides/claude-maxxing) (Claude)
