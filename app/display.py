import curses
from src.mazegen.MazeGenerator import MazeGenerator


class MazeDisplay:
    def __init__(
            self, maze: MazeGenerator, entry_coord: tuple[int, int],
            exit_coord: tuple[int, int]):
        self.maze = maze
        self.WALL_CHAR = "██"
        self.PATH_CHAR = "  "
        self.P42_CHAR = "██"
        self.SOL_CHAR = "██"
        self.entry_coord = entry_coord
        self.exit_coord = exit_coord

    def _init_colors(self) -> None:
        """Initialise les paires de couleurs pour curses."""
        curses.start_color()
        # curses.use_default_colors()  # Respecte le fond transparent du terminal // Decommente pour débug

        # curses.init_pair(ID, Couleur_Texte, Couleur_Fond)
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Murs standards
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Motif 42
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)   # Solution

    def _draw_maze(self, stdscr: curses.window) -> None:
        """
        Dessine le labyrinthe en utilisant le concept de Grille Étendue.
        """

        # On parcourt la grille mathématique
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                cell = self.maze.get_cell(x, y)
                if not cell:
                    continue

                # 1. Calcul des coordonnées sur l'écran (Grille étendue)
                # On multiplie par 2 l'axe X car un caractère ASCII est plus haut que large
                # Utiliser 2 caractères (ex: "██") rend le labyrinthe carré visuellement !
                screen_y = (y * 2) + 1
                screen_x = (x * 2) * 2 + 2  # *2 pour l'étendue, *2 pour la largeur du "██"

                # 2. Détermination de la couleur et du caractère central
                color = curses.color_pair(1)
                char_to_draw = self.PATH_CHAR

                if cell.is_part_of_42:
                    color = curses.color_pair(2)
                    char_to_draw = self.P42_CHAR
                elif cell.is_solution:
                    color = curses.color_pair(3)
                    char_to_draw = self.SOL_CHAR

                # On dessine le centre de la cellule
                try:
                    stdscr.addstr(screen_y, screen_x, char_to_draw, color)

                    # 3. Dessin des murs (On dessine les murs autour du centre)
                    # Si le mur Nord existe, on met un bloc au-dessus
                    if cell.walls["N"]:
                        stdscr.addstr(screen_y - 1, screen_x, self.WALL_CHAR, curses.color_pair(1))

                    # Si le mur Sud existe, on met un bloc en-dessous
                    if cell.walls["S"]:
                        stdscr.addstr(screen_y + 1, screen_x, self.WALL_CHAR, curses.color_pair(1))

                    # Mur Ouest (à gauche)
                    if cell.walls["W"]:
                        stdscr.addstr(screen_y, screen_x - 2, self.WALL_CHAR, curses.color_pair(1))

                    # Mur Est (à droite)
                    if cell.walls["E"]:
                        stdscr.addstr(screen_y, screen_x + 2, self.WALL_CHAR, curses.color_pair(1))

                    # Les coins (toujours des murs pour que visuellement ce soit fermé)
                    stdscr.addstr(screen_y - 1, screen_x - 2, self.WALL_CHAR, curses.color_pair(1))  # Nord-Ouest
                    stdscr.addstr(screen_y - 1, screen_x + 2, self.WALL_CHAR, curses.color_pair(1))  # Nord-Est
                    stdscr.addstr(screen_y + 1, screen_x - 2, self.WALL_CHAR, curses.color_pair(1))  # Sud-Ouest
                    stdscr.addstr(screen_y + 1, screen_x + 2, self.WALL_CHAR, curses.color_pair(1))  # Sud-Est

                except curses.error:
                    # Ignore les erreurs si on essaie de dessiner en dehors du terminal
                    pass

    def _draw_loop(self, stdscr: curses.window) -> None:
        curses.curs_set(0)
        self._init_colors()

        # On calcule la taille "physique" dont notre labyrinthe a besoin sur l'écran
        # Axe Y : (hauteur * 2) + 1 (pour les murs) + 2 (pour la marge et la barre d'infos)
        required_y = (self.maze.height * 2) + 4

        # Axe X : (largeur * 4) + 2 (pour les murs) + 2 (marge)
        # On multiplie par 4 car chaque cellule fait 2 caractères de large + l'espacement
        required_x = (self.maze.width * 4) + 4

        #  La Boucle d'Événements (écoute le clavier et les évènement de resize en temps réel)
        while True:
            stdscr.clear()  # Nettoie l'écran alternatif
            # On demande à curses la taille actuelle de la fenêtre à chaque tour de boucle
            max_y, max_x = stdscr.getmaxyx()

            # LE VIDEUR DU BOÎTE DE NUIT (Le check de taille)
            if max_y < required_y or max_x < required_x:
                warning = "⚠️ Terminal trop petit ! Agrandissez la fenêtre."
                # On centre le message d'erreur
                try:
                    stdscr.addstr(max_y // 2, (max_x - len(warning)) // 2, warning, curses.color_pair(1) | curses.A_BOLD)
                except curses.error:
                    pass  # Si le terminal est vraiment minuscule (genre 2x2), on ignore
            else:
                # La fenêtre est assez grande, on dessine la merveille !
                self._draw_maze(stdscr)

                instructions = [" Appuie sur 'r' pour regénérer ", " Appuie sur 'q' pour quitter"]
                try:
                    for i, line in enumerate(instructions):
                        stdscr.addstr(max_y - (2 - i), 2, line, curses.A_REVERSE)
                        # curses.A_REVERSE inverse les couleurs (texte noir sur fond blanc) pour faire un beau menu !
                        # Affichage du texte (stdscr.addstr(y, x, texte))
                except curses.error:
                    pass

            #  On rafraîchit l'écran pour appliquer les modifications visuelles
            stdscr.refresh()

            # On attend une action.
            # Astuce: si l'utilisateur redimensionne la fenêtre, curses génère une touche spéciale (curses.KEY_RESIZE)
            key = stdscr.getch()

            if key == ord('q'):
                break  # On sort de la boucle, le wrapper va fermer l'écran proprement
            elif key == ord('r'):
                # On regénère
                self.maze.replace_seed()
                self.maze.reset_grid()  # Ta fameuse fonction !
                self.maze.generate_maze()
                self.maze.solve_path(self.entry_coord, self.exit_coord)
            # Si la touche est curses.KEY_RESIZE, la boucle recommence toute seule,
            # recalcule max_y/max_x, et affiche le labyrinthe si c'est devenu assez grand !

    def start(self) -> None:
        """
        Point d'entrée sécurisé. Le wrapper gère l'écran alternatif et les crashs.
        """
        curses.wrapper(self._draw_loop)
