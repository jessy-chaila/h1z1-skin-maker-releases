# H1Z1 Skin Maker

**Documentation fonctionnelle — profil « Skin Maker »**

| | |
|---|---|
| Version de référence | 1.5.0 |
| Public | Membres disposant du rôle « Skin Maker » |
| Objet | Présentation du logiciel, de son organisation et du rôle de chaque module |
| Hors périmètre | Procédures pas à pas (les assistants du logiciel guident chaque opération) |

---

## Sommaire

1. [Présentation](#1-présentation)
2. [Principes de fonctionnement](#2-principes-de-fonctionnement)
3. [Authentification et droits d'accès](#3-authentification-et-droits-daccès)
4. [Organisation de l'interface](#4-organisation-de-linterface)
5. [Accueil](#5-accueil)
6. [Créer](#6-créer)
7. [Voir](#7-voir)
8. [Partager](#8-partager)
9. [Gérer](#9-gérer)
10. [Fonctions non incluses dans le profil](#10-fonctions-non-incluses-dans-le-profil)
11. [Emplacement des données](#11-emplacement-des-données)
12. [Glossaire](#12-glossaire)

---

## 1. Présentation

H1Z1 Skin Maker est une application Windows dédiée à la création de skins personnalisés pour H1Z1, destinés au projet communautaire ROTK.

Elle regroupe quatre fonctions :

- **Création** : skins d'armes (statiques ou animés), vêtements, objets portés et personnages.
- **Environnement de test** : un client de jeu local (Z1BR local) et son serveur, permettant de contrôler les créations en jeu sans intervenir sur ROTK.
- **Consultation** : catalogues des modèles 3D, des effets et des sons du jeu, et prévisualisation des skins.
- **Export** : production de paquets normalisés destinés à l'équipe ROTK.

Les créations restent locales. Leur diffusion sur ROTK dépend exclusivement de l'intégration réalisée par l'équipe ROTK à partir des exports transmis.

---

## 2. Principes de fonctionnement

| Principe | Description |
|---|---|
| Environnement isolé | Le client local est une copie distincte du client H1Z1, associée à un serveur local. L'installation Steam et le launcher ROTK ne sont pas modifiés. |
| Conservation des données | Aucune suppression définitive : les skins retirés sont archivés (`custom-skins\_retired`), les personnages remplacés sont sauvegardés. |
| Jeu fermé | Les opérations qui modifient le client local exigent que le jeu et le serveur local soient arrêtés. |
| Reconstruction de l'aperçu | Le menu Customize s'appuie sur des données d'aperçu. Certaines opérations les régénèrent afin que les nouveaux skins y apparaissent. |
| Auteur | Le pseudo d'auteur défini dans la Configuration est appliqué aux exports et aux licences associées. |
| Textures | Les images fournies doivent correspondre au dépliage UV du modèle ciblé. |
| Mises à jour | Le logiciel détecte les nouvelles versions et applique des mises à jour incrémentales. |
| Journal | Chaque traitement consigne son déroulement (informations, avertissements, erreurs) dans le journal de l'application. |

---

## 3. Authentification et droits d'accès

### 3.1 Authentification

L'accès au logiciel nécessite une authentification Discord. Seules les données d'identité Discord (identifiant, pseudo, avatar) sont utilisées.

### 3.2 Association au poste de travail

Chaque compte est associé à un poste unique, identifié par un code PC (`XXXX-XXXX-XXXX-XXXX`). En cas de refus d'accès, l'application affiche l'identifiant Discord et le code PC à communiquer à l'administrateur. Le code PC est modifié en cas de réinstallation de Windows et doit alors être de nouveau validé.

### 3.3 Contrôle périodique

- Les droits sont contrôlés toutes les 5 minutes ; toute modification est appliquée sans redémarrage.
- Le retrait d'un accès entraîne la fermeture de l'application.
- Sans connexion Internet, l'application reste utilisable 3 jours au maximum.

### 3.4 Périmètre du profil « Skin Maker »

| Module | Accès |
|---|---|
| Accueil | Complet |
| Configuration | Complet |
| Perso et tenues | Complet |
| Skins d'armes | Nouveau skin depuis une texture, Skin animé d'arme, Vues 3P et sol |
| Objets portés | Nouveau skin depuis une texture, Vêtement ou objet animé |
| Liste de modèles | Complet |
| Sons et effets | Complet |
| Aperçu ingame | Complet |
| Exports ROTK | Skin d'arme, Objet porté animé, Replace de skin de base, Convertir PNG vers DDS |
| Bibliothèque | Retirer des skins, Corbeille |
| Outils | Complet |

Les éléments non inclus restent affichés, grisés et marqués d'un cadenas. Des droits complémentaires peuvent être attribués individuellement par l'administrateur.

### 3.5 Compte utilisateur

La carte de compte, en bas de la barre latérale, présente l'avatar, le pseudo et le rôle. Son menu donne accès à :

- **Signaler un bug** : copie du journal (chemins anonymisés) et création d'un signalement prérempli sur GitHub ;
- **Déconnexion** ;
- l'identifiant Discord du compte.

### 3.6 Guide de démarrage

Tant que la configuration requise est incomplète, un guide de mise en service s'affiche au lancement. Il couvre la localisation du jeu, l'installation des prérequis (Git, Node.js), l'installation du client local (environ 20 Go, de préférence sur le disque de H1Z1), Blender (facultatif) et le profil. Il peut être relancé depuis la Configuration.

---

## 4. Organisation de l'interface

- **Barre latérale** : navigation organisée en quatre familles : Créer, Voir, Partager, Gérer. Elle comprend également le bouton « Lancer le jeu » et la carte de compte.
- **Hubs** : chaque module de création se présente sous forme de tuiles. Une tuile ouvre soit un formulaire, soit un assistant en plusieurs étapes conclu par un récapitulatif.
- **Assistants** : le fil d'étapes est cliquable pour revenir directement à une étape déjà atteinte. Après une création, le bouton **Modifier ce skin** rouvre l'assistant avec les mêmes valeurs : une nouvelle exécution met à jour le même skin.
- **Journal** : suivi en temps réel des traitements en cours.
- **Discord Rich Presence** : affichage optionnel de l'activité dans le statut Discord.
- **Langues** : français, anglais.

---

## 5. Accueil

- **Synthèse** : date, heure et indicateurs de l'installation ; accès direct à la Configuration.
- **Mises à jour** : indicateur de disponibilité d'une nouvelle version et installation.
- **Parcourir** : accès à l'ensemble des modules, avec filtre par famille et recherche.
- **Environnement** : état des chemins, du client, du serveur et des prérequis.

---

## 6. Créer

### 6.1 Perso et tenues

Gestion des personnages et des tenues du client local.

| Fonction | Rôle |
|---|---|
| Personnage et tenue | Sélection du personnage actif et de la tenue portée dans le client local. Les personnages remplacés sont sauvegardés. |
| Créer une peau custom | Création d'un personnage à partir d'une peau peinte (corps et visage sur une texture unique). Génère un kit de travail Substance, puis intègre la texture finalisée. |
| Exporter vers Blender | Export du personnage et des pièces sélectionnées avec le squelette du jeu (129 os), aux formats `.glb`, `.blend` et `.fbx`, accompagné des textures PNG. Sert de référence pour la modélisation et le calage d'objets. |

### 6.2 Skins d'armes

| Fonction | Rôle |
|---|---|
| Nouveau skin depuis une texture | Création d'un skin à partir d'un modèle du jeu (arme, vêtement, véhicule ou corps) et d'une texture. |
| Skin animé d'arme | Création ou modification d'un skin d'arme animé selon deux méthodes : **Multiscroll** (défilement d'un motif) ou **Print** (séquence d'images limitée à une zone définie par un masque). Paramètres disponibles : motif, fond, seconde zone, ondulation, effet de particules natif du jeu. |
| Vues 3P et sol | Ajout des vues à la troisième personne et au sol (avec niveaux de détail), conformément à la structure des packs officiels, et application de l'effet Print à ces vues. |

### 6.3 Objets portés

Vêtements (hauts, vestes, pantalons) et accessoires (casques, masques, lunettes, sacs, chaussures, montres).

| Fonction | Rôle |
|---|---|
| Nouveau skin depuis une texture | Création d'un skin de vêtement ou d'accessoire à partir d'un modèle du jeu et d'une texture. |
| Vêtement ou objet animé | Animation d'un vêtement ou accessoire existant par la méthode Print (masque, motif, couches de fond). |

---

## 7. Voir

### 7.1 Liste de modèles

Catalogue des modèles 3D du jeu et des skins personnalisés.

- Catégories : armes, personnage et vêtements, véhicules, décors, structures, skins personnalisés.
- Recherche par nom et visionneuse 3D interactive.
- Affichage des textures de chaque modèle.
- Capture d'image (PNG) et export du modèle (OBJ et textures PNG).

Usage : identification du modèle cible, consultation des textures d'origine, récupération d'une base de travail.

### 7.2 Sons et effets

Catalogue des effets (particules, sons, effets composites) et des sons du jeu, avec recherche, catégories et détail de composition. Il alimente les listes d'effets proposées dans les assistants.

### 7.3 Aperçu ingame

Prévisualisation d'un skin avant lancement du jeu.

| Mode | Rôle |
|---|---|
| Mes skins | Affichage des skins installés avec texture et animation, comparaison avec l'original et poids du skin (Mo). |
| Texture sur un modèle | Application d'une texture (PNG, TGA, DDS) et, en option, d'une animation Print sur un modèle du jeu, avant toute création. |

---

## 8. Partager

### Exports ROTK

Production de paquets destinés à l'équipe ROTK. Le pseudo d'auteur de la Configuration y est appliqué. Les fichiers installés localement ne sont pas modifiés.

| Fonction | Contenu produit |
|---|---|
| Skin d'arme | Dossier et archive : texture, icône, animation, modèles. |
| Objet porté animé | Dossier et archive : fichiers homme et femme, animation, icône, guide d'intégration. |
| Replace de skin de base | Texture de remplacement d'un skin existant : fichiers C, S, N et dossier `Icon` contenant l'icône d'origine. |
| Convertir PNG vers DDS | Conversion d'une image au format DDS BC3 (DXT5) avec mipmaps, avec détourage optionnel d'un fond uni. |

Les exports ne contiennent que les fichiers nécessaires à l'intégration ; les modalités d'intégration relèvent de l'équipe ROTK.

---

## 9. Gérer

### 9.1 Bibliothèque

**Retirer des skins** : liste de l'ensemble des skins personnalisés, triable par date ou par nom, avec aperçu 3D. Deux actions :

- **Archiver** : le skin est déplacé dans `custom-skins\_retired` et reste restaurable ;
- **Supprimer définitivement** : les fichiers du skin sont effacés du disque, après confirmation. Cette action est irréversible.

Les skins protégés sont exclus. Une reconstruction de l'aperçu est proposée en fin d'opération.

**Corbeille** : liste des skins archivés, avec aperçu 3D. **Restaurer** rétablit un skin avec ses identifiants d'origine : les tenues sauvegardées qui l'utilisaient le retrouvent. Un skin réinstallé depuis son archivage apparaît grisé et ne peut pas être restauré.

### 9.2 Outils

**Client local**

| Fonction | Rôle |
|---|---|
| Lancer le client local | Démarrage du serveur local et du client Z1BR. L'arrêt du jeu arrête les services associés. |
| Console props (F9) | Apparition de tout modèle du jeu en Combat training. |
| Reconstruire l'aperçu | Régénération des données d'aperçu du menu Customize pour l'ensemble des skins. |
| Installer le client local | Installation complète sur un nouveau poste (environ 20 Go). Prérequis : H1Z1 (Steam) et launcher ROTK. Reprise possible après interruption. |

**Import**

| Fonction | Rôle |
|---|---|
| Importer fichiers game ready | Import d'exports ROTK (archive ou dossier, un ou plusieurs paquets) : objets portés, animations, skins d'armes, montres. Les éléments existants sont mis à jour. |
| Ajouter les items « Vide » | Création, dans chaque catégorie d'habillement, d'un item permettant de retirer l'objet porté en jeu. |

**Captures et décor**

| Fonction | Rôle |
|---|---|
| Studio photo | Paramétrage des caméras du menu Customize et de la position du personnage dans le lobby, mode nuit inclus, pour la réalisation de captures. |
| Remplacer une texture de décor | Remplacement d'une texture d'élément de décor sur l'ensemble de ses occurrences en Combat training ; opération réversible. |

### 9.3 Configuration

- Chemins : données, assets H1Z1, client local, serveur local, Blender, Node.js, Git (détection automatique disponible).
- Pseudo d'auteur.
- Langue.
- Discord Rich Presence.
- Relance du guide de démarrage.

---

## 10. Fonctions non incluses dans le profil

| Module | Fonctions |
|---|---|
| Créer | Tatouages, Animations (émotes personnalisées) |
| Skins d'armes | Flux 3D, Skin animé depuis une vidéo, Animation HD, Aperçu Blender |
| Objets portés | Import de modèles 3D, Optimisation, Réparation des UV, Texture Substance |
| Exports ROTK | Modèle 3D Custom, Tatouages, Animations |
| Bibliothèque | Retrait des modèles 3D et des tatouages |
| Administration | Gestion des membres, rôles et droits |

---

## 11. Emplacement des données

| Emplacement | Contenu |
|---|---|
| `%APPDATA%\H1Z1 Skin Maker\` | Configuration, session, cache des droits |
| Dossier du client local | Client isolé, serveur local, outils |
| `custom-skins\` | Skins installés |
| `custom-skins\_retired\` | Skins archivés (restaurables depuis la Corbeille) |
| `Skins H1Z1\Persos\<Nom>` | Kits Substance des personnages |
| `Blender\<Nom>` | Exports Blender |
| Dossier d'export indiqué en fin d'assistant | Paquets ROTK |

---

## 12. Glossaire

| Terme | Définition |
|---|---|
| ROTK | Projet communautaire H1Z1 destinataire des créations. |
| Client local (Z1BR local) | Instance privée du jeu et de son serveur, dédiée aux tests. |
| Combat training | Mode d'entraînement du client local. |
| Customize | Menu du lobby de sélection des tenues, armes et véhicules. |
| Skin | Variante visuelle d'un objet du jeu. |
| Replace | Skin remplaçant la texture d'un skin existant. |
| UV | Dépliage 2D d'un modèle 3D déterminant l'application de la texture. |
| DDS | Format de texture compressé utilisé par le jeu. |
| C / S / N | Textures de couleur, spéculaire et normale. |
| Multiscroll | Animation par défilement d'un motif. |
| Print | Animation par séquence d'images limitée à une zone. |
| Masque | Image définissant la zone animée. |
| 3P / LOD | Vue à la troisième personne / niveaux de détail. |
| Game ready | Export directement intégrable dans le jeu. |
| Code PC | Identifiant du poste associé au compte. |

---

H1Z1 Skin Maker — développé par waaksH1. Signalement d'anomalie : carte de compte › Signaler un bug.
