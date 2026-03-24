import curses


class MazeDisplay:
    def __init__(self):
        # Plus tard, on passera l'objet MazeGenerator ici pour lire la grille
        pass

    def _draw_loop(self, stdscr: curses.window) -> None:
        """
        C'est ici que tout se passe. stdscr est la fenêtre principale.
        """
        # 1. Configuration initiale
        curses.curs_set(0)  # Cache le curseur clignotant du terminal
        stdscr.clear()      # Nettoie l'écran alternatif

        # 2. Récupération dynamique de la taille actuelle du terminal
        height, width = stdscr.getmaxyx()

        # 3. Préparation des textes
        title = "Bienvenue dans A-Maze-ing !"
        instruction = "Appuie sur 'q' pour quitter, ou 'r' pour regénérer."

        # 4. Affichage du texte (stdscr.addstr(y, x, texte))
        # On calcule le centre de l'écran mathématiquement
        stdscr.addstr(height // 2 - 1, (width - len(title)) // 2, title)
        stdscr.addstr(
            height // 2 + 1, (width - len(instruction)) // 2, instruction
            )

        # 5. On rafraîchit l'écran pour appliquer les modifications visuelles
        stdscr.refresh()

        count = 0

        # 6. La Boucle d'Événements (écoute le clavier en temps réel)
        while True:
            key = stdscr.getch()  # Attend que l'utilisateur appuie sur une touche

            if key == ord('q'):
                break  # On sort de la boucle, le wrapper va fermer l'écran proprement
            elif key == ord('r'):
                # C'est ici qu'on appellera maze.generate() pour l'Epic 5 !
                stdscr.clear()
                stdscr.addstr(0, 0, "Génération d'un nouveau labyrinthe...")
                stdscr.refresh()
                stdscr.clear()
                stdscr.addstr(height // 2, (width - len(str(count))) // 2,
                              str(count))
                count += 1
                stdscr.refresh()

    def start(self) -> None:
        """
        Point d'entrée sécurisé. Le wrapper gère l'écran alternatif et les crashs.
        """
        curses.wrapper(self._draw_loop)
