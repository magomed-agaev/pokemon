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

# Fonction pour dessiner les boutons
def dessiner_boutons(fenetre, bouton_precedent_hover, bouton_suivant_hover):
    if bouton_precedent_hover:
        pygame.draw.rect(fenetre, (100, 100, 100, 200), bouton_precedent)
    else:
        pygame.draw.rect(fenetre, (200, 200, 200), bouton_precedent)

    if bouton_suivant_hover:
        pygame.draw.rect(fenetre, (100, 100, 100, 200), bouton_suivant)
    else:
        pygame.draw.rect(fenetre, (200, 200, 200), bouton_suivant)

    text_precedent = font.render("Previous", True, (0, 0, 0))
    text_suivant = font.render("Next", True, (0, 0, 0))
    fenetre.blit(text_precedent, (bouton_precedent.x + 10, bouton_precedent.y + 10))
    fenetre.blit(text_suivant, (bouton_suivant.x + 20, bouton_suivant.y + 10))
    

# Fonction pour afficher les stats du Pokémon
def afficher_pokemon(fenetre, pokemon):

    couleur_fond1 = couleurtype(pokemon['types'][0])
    couleur_fond2 = couleurtype(pokemon['types'][1]) if len(pokemon['types']) > 1 else couleur_fond1

    fenetre.fill(couleur_fond1, (0, 0, largeur_fenetre // 2, hauteur_fenetre))
    fenetre.fill(couleur_fond2, (largeur_fenetre // 2, 0, largeur_fenetre // 2, hauteur_fenetre))

    image = pygame.transform.scale(pokemon["image_obj"], (300, 300))
    fenetre.blit(image, (largeur_fenetre // 2 - 150, 60))

# Coordonnées taille et couleur cercle
    cercle_centre = (largeur_fenetre // 2, 210)  
    cercle_rayon = 150  
    pygame.draw.circle(fenetre, (255, 255, 255), cercle_centre, cercle_rayon)

# Image du pokemo,
    image = pygame.transform.scale(pokemon["image_obj"], (300, 300))
    fenetre.blit(image, (largeur_fenetre // 2 - 150, 60))  # Centrer l'image

# Infos du pokemon affiché
    stats = [
        f"Name: {pokemon['Name']}",
        f"Type: {', '.join(pokemon['types'])}",
        f"Move: {', '.join([attaque['nom'] for attaque in pokemon['Move']])}"
    ]

    for i, stat in enumerate(stats):
        text = font.render(stat, True, (0, 0, 0))
        fenetre.blit(text, (50, 350 + i * 30))


# Fonction pour Couleures du BG
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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_cours = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Clic gauche
                if bouton_precedent.collidepoint(event.pos):
                    index_pokemon_actuel = (index_pokemon_actuel - 1) % len(data["pokedex"])
                elif bouton_suivant.collidepoint(event.pos):
                    index_pokemon_actuel = (index_pokemon_actuel + 1) % len(data["pokedex"])
        elif event.type == pygame.MOUSEMOTION:
            bouton_precedent_hover = bouton_precedent.collidepoint(event.pos)
            bouton_suivant_hover = bouton_suivant.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                index_pokemon_actuel = (index_pokemon_actuel - 1) % len(data["pokedex"])
            elif event.key == pygame.K_RIGHT:
                index_pokemon_actuel = (index_pokemon_actuel + 1) % len(data["pokedex"])

    dessiner_boutons(fenetre, bouton_precedent_hover, bouton_suivant_hover) 


# Chargement de l'image
    image = pygame.image.load('pokedex.png')
    image = pygame.transform.scale(image, (200, 100))
    # Position de l'image
    position_image = (largeur_fenetre // 19, hauteur_fenetre - 510)
    # Dessin de l'image
    fenetre.blit(image, position_image)

    pygame.display.update() # Mettre à jour l'affichage

pygame.quit()
sys.exit()
