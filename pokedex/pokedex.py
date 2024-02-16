import json
import pygame
import sys

with open("pokedex.json", "r") as file: # Lien avec le fichier .json
    data = json.load(file)

print(data)

# Création de l'interface graphique
pygame.init()

largeur_fenetre = 800
hauteur_fenetre = 600
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
pygame.display.set_caption("Pokedex")

for pokemon in data["pokedex"]:
    image_pokemon = pygame.image.load(pokemon["image"])
    pokemon["image_obj"] = image_pokemon

font = pygame.font.Font(None, 36)

# Création de rectangles pour les boutons Précédent et Suivant
bouton_precedent = pygame.Rect(50, 15, 150, 50)
bouton_suivant = pygame.Rect(600, 15, 150, 50)  

# Fonction pour dessiner les boutons et afficher quand la souris est dessus
def dessiner_boutons(fenetre, bouton_precedent_hover, bouton_suivant_hover):
    if bouton_precedent_hover:
        pygame.draw.rect(fenetre, (100, 100, 100, 200), bouton_precedent) #Dessin des fonctions bouton precedent suivant avec pygame.draw (hover =  retour ou avant fenetre)
    else:
        pygame.draw.rect(fenetre, (200, 200, 200), bouton_precedent)

    if bouton_suivant_hover:
        pygame.draw.rect(fenetre, (100, 100, 100, 200), bouton_suivant)
    else:
        pygame.draw.rect(fenetre, (200, 200, 200), bouton_suivant)

    text_precedent = font.render("Previous", True, (0, 0, 0)) #Police, taille et couleur.
    text_suivant = font.render("Next", True, (0, 0, 0))
    fenetre.blit(text_precedent, (bouton_precedent.x + 10, bouton_precedent.y + 10))
    fenetre.blit(text_suivant, (bouton_suivant.x + 20, bouton_suivant.y + 10))
    

# Fonction pour afficher la couleur du fond selon le type
def afficher_pokemon(fenetre, pokemon):

    couleur_fond1 = couleurtype(pokemon['types'][0]) #Si le Pokemon possède 1 type 
    couleur_fond2 = couleurtype(pokemon['types'][1]) if len(pokemon['types']) > 1 else couleur_fond1 #Si le Pokemon possède 2 types, affiche deux couleurs

    fenetre.fill(couleur_fond1, (0, 0, largeur_fenetre // 2, hauteur_fenetre)) #Fait en sorte que la couleur prend tout le fond
    fenetre.fill(couleur_fond2, (largeur_fenetre // 2, 0, largeur_fenetre // 2, hauteur_fenetre)) #Pareil mais avec les 2 couleurs

    image = pygame.transform.scale(pokemon["image_obj"], (300, 300))
    fenetre.blit(image, (largeur_fenetre // 2 - 150, 60))

# Coordonnées taille et couleur cercle
    cercle_centre = (largeur_fenetre // 2, 210) 
    cercle_rayon = 150  
    pygame.draw.circle(fenetre, (255, 255, 255), cercle_centre, cercle_rayon) #Ajoute un cercle avec blanc au centre autour du pokémon

# Image du pokemon
    image = pygame.transform.scale(pokemon["image_obj"], (300, 300)) #Redimensionner l'image du pokémon
    fenetre.blit(image, (largeur_fenetre // 2 - 150, 60)) #C'est ou le pokémon va apparaître dans la fenêtre

# Fiche du pokemon affiché 
    stats = [
        f"Name: {pokemon['Name']}",
        f"Type: {', '.join(pokemon['types'])}",
        f"Move: {', '.join([attaque['nom'] for attaque in pokemon['Move']])}" 
    ]

    for i, stat in enumerate(stats): #Boucle sur la liste stats pour utiliser l'Index pour calculer la position ou le texte sera affiché
        text = font.render(stat, True, (0, 0, 0))
        fenetre.blit(text, (50, 350 + i * 30))


# Fonction qui attribue une couleur a chaque type
def couleurtype(type_pokemon):
    couleurs_types = {
        "Water": (0, 105, 148),
        "Fire": (205, 34, 0),
        "Grass": (0, 128, 0),
        "Ghost": (75, 0, 130),
        "Basic": (128, 128, 128), 
        "Electric": (255, 215, 0),
        "Poison": (128, 0, 128), 
        }
    return couleurs_types.get(type_pokemon, (255, 255, 255))  


# Index du pokemon actuellement affiché
index_pokemon_actuel = 0

# Boucle 
en_cours = True
bouton_precedent_hover = False
bouton_suivant_hover = False
while en_cours:

    fenetre.fill((255, 255, 255))# Effacer l'écran

    afficher_pokemon(fenetre, data["pokedex"][index_pokemon_actuel])

    # Gestion des événements
    for event in pygame.event.get(): #Boucle qui parcours tout les evenements 
        if event.type == pygame.QUIT: #Verifie si l'utilisateur a fermé la fenêtre 
            en_cours = False #Si c'est le cas ferme la boucle et la fenêtre
        elif event.type == pygame.MOUSEBUTTONDOWN: #Verifie si l'utilisateur a utilisé un clic souris (MOUSEBUTTON)
            if event.button == 1: #1 = le bouton gauche de la souris
                if bouton_precedent.collidepoint(event.pos): # Cette condition vérifie si le point de la souris avec e.p est à l'intérieur du rectangle défini par b.p. Si c'est le cas l'utilisateur a cliqué sur le bouton Précédent.
                    index_pokemon_actuel = (index_pokemon_actuel - 1) % len(data["pokedex"]) #précedente page du pokedex
                elif bouton_suivant.collidepoint(event.pos): #Sinon Bouton suivant.
                    index_pokemon_actuel = (index_pokemon_actuel + 1) % len(data["pokedex"]) #prochaine page du pokedex
        elif event.type == pygame.MOUSEMOTION: #Verifie que la souris a été déplacé
            bouton_precedent_hover = bouton_precedent.collidepoint(event.pos) #indique si la souris est sur le bouton precedent
            bouton_suivant_hover = bouton_suivant.collidepoint(event.pos) #suivant
        elif event.type == pygame.KEYDOWN: #verifie si une  des touches flèches a été touché 
            if event.key == pygame.K_LEFT: #verifie si la touche GAUCHE
                index_pokemon_actuel = (index_pokemon_actuel - 1) % len(data["pokedex"]) #page preecedente
            elif event.key == pygame.K_RIGHT: #DROITE
                index_pokemon_actuel = (index_pokemon_actuel + 1) % len(data["pokedex"]) #page suivante

    dessiner_boutons(fenetre, bouton_precedent_hover, bouton_suivant_hover) 


# Chargement de l'image pokedex
    image = pygame.image.load('pokedex.png')
    image = pygame.transform.scale(image, (200, 100))
    position_image = (largeur_fenetre // 19, hauteur_fenetre - 510)
    fenetre.blit(image, position_image)

    pygame.display.update() # Mettre à jour l'affichage

pygame.quit()
sys.exit()
