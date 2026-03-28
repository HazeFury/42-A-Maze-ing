import curses
from mazegen.maze_generator import MazeGenerator


class MazeDisplay:
    def __init__(
            self, maze: MazeGenerator, entry_coord: tuple[int, int],
            exit_coord: tuple[int, int]) -> None:

        self.maze = maze
        self.WALL_CHAR = "██"
        self.PATH_CHAR = "  "
        self.P42_CHAR = "██"
        self.SOL_CHAR = "██"
        self.entry_coord = entry_coord
        self.exit_coord = exit_coord
        self.wall_colors = [1, 6, 7, 8, 9, 10]
        self.current_wall_color_idx = 0

    def _init_colors(self) -> None:
        """
        Initialize pair color for curses.

        Structure is => curses.init_pair(ID, Text_color, Background)
        """
        curses.start_color()

        # ========  ITEMS  =============
        # Yellow inside "42" pattern
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        # Cyan for solution path
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
        # Red for entry point
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
        # Green for exit point
        curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)

        # ========  WALLS  ==============
        # White (basic color)
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        # Violet (magenta)
        curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        # Blue
        curses.init_pair(7, curses.COLOR_BLUE, curses.COLOR_BLACK)
        # Orange
        curses.init_pair(8, 166, curses.COLOR_BLACK)
        # Rose
        curses.init_pair(9, 163, curses.COLOR_BLACK)
        # Grey
        curses.init_pair(10, 244, curses.COLOR_BLACK)

    def _draw_maze(self, stdscr: curses.window, is_showing_path: bool) -> None:
        """
        Dessine le labyrinthe en utilisant le concept de Grille Étendue.
        """

        curr_maze_color_id = self.wall_colors[self.current_wall_color_idx]
        entry_x, entry_y = self.entry_coord
        exit_x, exit_y = self.exit_coord
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

                try:
                    # --- 1. DÉTERMINATION DU CENTRE (Couleur et Caractère) ---
                    color = curses.color_pair(1)
                    char_to_draw = self.PATH_CHAR  # Par défaut : vide

                    if cell.is_part_of_42:
                        color = curses.color_pair(2)
                        char_to_draw = self.P42_CHAR
                    elif cell.x == entry_x and cell.y == entry_y:
                        # L'entrée gagne toujours !
                        color = curses.color_pair(4)
                        char_to_draw = self.SOL_CHAR
                    elif cell.x == exit_x and cell.y == exit_y:
                        # La sortie gagne toujours !
                        color = curses.color_pair(5)
                        char_to_draw = self.SOL_CHAR
                    elif cell.is_solution and is_showing_path:
                        # Le chemin standard (uniquement si activé)
                        color = curses.color_pair(3)
                        char_to_draw = self.SOL_CHAR

                    # On dessine le centre !
                    stdscr.addstr(screen_y, screen_x, char_to_draw, color)

                    # --- 2. DESSIN DES PONTS CONTINUS ---
                    # On ne les dessine QUE si on affiche le chemin
                    if cell.is_solution and is_showing_path:
                        solution_color = curses.color_pair(3)

                        if cell.path_connections["N"]:
                            stdscr.addstr(screen_y - 1, screen_x,
                                          self.SOL_CHAR, solution_color)
                        if cell.path_connections["S"]:
                            stdscr.addstr(screen_y + 1, screen_x,
                                          self.SOL_CHAR, solution_color)
                        if cell.path_connections["W"]:
                            stdscr.addstr(screen_y, screen_x - 2,
                                          self.SOL_CHAR, solution_color)
                        if cell.path_connections["E"]:
                            stdscr.addstr(screen_y, screen_x + 2,
                                          self.SOL_CHAR, solution_color)

                    # 3. Dessin des murs (On dessine les murs autour du centre)
                    # Si le mur Nord existe, on met un bloc au-dessus
                    if cell.walls["N"]:
                        stdscr.addstr(screen_y - 1, screen_x, self.WALL_CHAR,
                                      curses.color_pair(curr_maze_color_id))

                    # Si le mur Sud existe, on met un bloc en-dessous
                    if cell.walls["S"]:
                        stdscr.addstr(screen_y + 1, screen_x, self.WALL_CHAR,
                                      curses.color_pair(curr_maze_color_id))

                    # Mur Ouest (à gauche)
                    if cell.walls["W"]:
                        stdscr.addstr(screen_y, screen_x - 2, self.WALL_CHAR,
                                      curses.color_pair(curr_maze_color_id))

                    # Mur Est (à droite)
                    if cell.walls["E"]:
                        stdscr.addstr(screen_y, screen_x + 2, self.WALL_CHAR,
                                      curses.color_pair(curr_maze_color_id))

                    # Les coins (toujours des murs pour que visuellement ce soit fermé)
                    stdscr.addstr(screen_y - 1, screen_x - 2, self.WALL_CHAR,
                                  curses.color_pair(curr_maze_color_id))  # Nord-Ouest
                    stdscr.addstr(screen_y - 1, screen_x + 2, self.WALL_CHAR,
                                  curses.color_pair(curr_maze_color_id))  # Nord-Est
                    stdscr.addstr(screen_y + 1, screen_x - 2, self.WALL_CHAR,
                                  curses.color_pair(curr_maze_color_id))  # Sud-Ouest
                    stdscr.addstr(screen_y + 1, screen_x + 2, self.WALL_CHAR,
                                  curses.color_pair(curr_maze_color_id))  # Sud-Est

                except curses.error:
                    # Ignore les erreurs si on essaie de dessiner en dehors du terminal
                    pass

    def _draw_loop(self, stdscr: curses.window) -> None:
        curses.curs_set(0)
        self._init_colors()
        is_showing_path: bool = True
        margin: int = 10

        # On calcule la taille "physique" dont notre labyrinthe a besoin sur l'écran
        # Axe Y : (hauteur * 2) + 1 (pour les murs) + 2 (pour la marge et la barre d'infos)
        required_y = (self.maze.height * 2) + margin

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
                warning = "⚠️  Terminal too small! Enlarge the window."
                # On centre le message d'erreur
                try:
                    stdscr.addstr(max_y // 2, (max_x - len(warning)) // 2, warning, curses.color_pair(1) | curses.A_BOLD)
                except curses.error:
                    raise Exception("Terminal (very) too small! Please"
                                    " enlarge the window to launch display")

            else:
                # La fenêtre est assez grande, on dessine la merveille !
                self._draw_maze(stdscr, is_showing_path)

                instructions = [
                    "============  A-Maze-ing  ============",
                    " 1. Re-generate a new maze            ",
                    " 2. Show/Hide path from entry to exit ",
                    " 3. Rotate maze colors                ",
                    " 4. Quit                              "
                    ]
                try:
                    for i, line in enumerate(instructions):
                        stdscr.addstr(max_y - ((len(instructions) + 1) - i), 2,
                                      line, curses.A_REVERSE)
                        # curses.A_REVERSE inverse les couleurs (texte noir sur fond blanc) pour faire un beau menu !
                        # Affichage du texte (stdscr.addstr(y, x, texte))
                except curses.error:
                    pass

            #  On rafraîchit l'écran pour appliquer les modifications visuelles
            stdscr.refresh()

            # On attend une action.
            # Astuce: si l'utilisateur redimensionne la fenêtre, curses génère une touche spéciale (curses.KEY_RESIZE)
            key = stdscr.getch()

            if key == ord('4'):
                break  # On sort de la boucle, le wrapper va fermer l'écran proprement
            if key == ord('2'):
                is_showing_path = not is_showing_path
            if key == ord('3'):
                self.current_wall_color_idx = (
                    (self.current_wall_color_idx + 1) % len(self.wall_colors)
                )
            elif key == ord('1'):
                # On regénère
                self.maze.replace_seed()
                self.maze.reset_grid()
                self.maze.generate_maze()
                self.maze.solve_path(self.entry_coord, self.exit_coord)
            # Si la touche est curses.KEY_RESIZE, la boucle recommence toute seule,
            # recalcule max_y/max_x, et affiche le labyrinthe si c'est devenu assez grand !

    def start(self) -> None:
        """
        Point d'entrée sécurisé. Le wrapper gère l'écran alternatif et les crashs.
        """
        curses.wrapper(self._draw_loop)
