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
def dessiner_boutons(fenetre):
    pygame.draw.rect(fenetre, (200, 200, 200), bouton_precedent)
    pygame.draw.rect(fenetre, (200, 200, 200), bouton_suivant)  
    text_precedent = font.render("Précédent", True, (0, 0, 0))
    text_suivant = font.render("Suivant", True, (0, 0, 0))
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

# Image du Pokémon
    image = pygame.transform.scale(pokemon["image_obj"], (300, 300))
    fenetre.blit(image, (largeur_fenetre // 2 - 150, 60))  # Centrer l'image

    stats = [
        f"Nom: {pokemon['nom']}",
        f"Type: {', '.join(pokemon['types'])}",
        f"PV: {pokemon['pv']}",
        f"Attaque: {pokemon['atk']}",
        f"Défense: {pokemon['def']}",
        f"Expérience: {pokemon['exp']}",
        f"Attaques: {', '.join([attaque['nom'] for attaque in pokemon['attaques']])}"
    ]

    for i, stat in enumerate(stats):
        text = font.render(stat, True, (0, 0, 0))
        fenetre.blit(text, (50, 350 + i * 30))


# Fonction pour Couleures du BG
def couleurtype(type_pokemon):
    couleurs_types = {
        "Eau": (0, 105, 148),
        "Feu": (205, 34, 0),
        "Plante": (0, 128, 0),
        "Spectre": (75, 0, 130),
        }
    return couleurs_types.get(type_pokemon, (255, 255, 255))  

    # Surfaces de textes des statistiques
    stats = [
        f"Nom: {pokemon['nom']}",
        f"Type: {', '.join(pokemon['types'])}",
        f"PV: {pokemon['pv']}",
        f"Attaque: {pokemon['atk']}",
        f"Défense: {pokemon['def']}",
        f"Expérience: {pokemon['exp']}",
        f"Attaques: {', '.join([attaque['nom'] for attaque in pokemon['attaques']])}"
    ]

    for i, stat in enumerate(stats):
        text = font.render(stat, True, (0, 0, 0)) 
        fenetre.blit(text, (50, 350 + i * 30))

# Index du Pokémon actuellement affiché
index_pokemon_actuel = 0

# Boucle 
en_cours = True
while en_cours:

    fenetre.fill((255, 255, 255))# Effacer l'écran

    afficher_pokemon(fenetre, data["pokedex"][index_pokemon_actuel])# Affichage du Pokémon actuel

    dessiner_boutons(fenetre) # Dessiner les boutons

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_cours = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic gauche
                if bouton_precedent.collidepoint(event.pos):
                    index_pokemon_actuel = (index_pokemon_actuel - 1) % len(data["pokedex"])
                elif bouton_suivant.collidepoint(event.pos):
                    index_pokemon_actuel = (index_pokemon_actuel + 1) % len(data["pokedex"])
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                index_pokemon_actuel = (index_pokemon_actuel - 1) % len(data["pokedex"])
            elif event.key == pygame.K_RIGHT:
                index_pokemon_actuel = (index_pokemon_actuel + 1) % len(data["pokedex"])

    pygame.display.flip()    # Mise à jour de l'affichage

pygame.quit()
sys.exit()
