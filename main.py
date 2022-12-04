import game


if __name__ == "__main__":

    proc = game.Game()
    proc.init_colors()
    proc.init_data()
    proc.init_fonts()
    
    # proc.level()
    proc.menu()