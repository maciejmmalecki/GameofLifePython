import argparse
import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from game_of_life.board import Board
from game_of_life.simulation import Simulation, Video

def main():
    parser = argparse.ArgumentParser(description="Symulacja Gry w Życie Conwaya")
    parser.add_argument('config_file', help='Ścieżka do pliku konfiguracyjnego (układ planszy)')
    parser.add_argument('--fps', type=int, default=10, help='Klatki na sekundę dla animacji (domyślnie 10)')
    parser.add_argument('--max-steps', type=int, default=500, help='Maksymalna liczba kroków symulacji (domyślnie 500)')

    args = parser.parse_args()

    try:
        board = Board(1, 1)
        board.load_board_from_file(args.config_file)
    except Exception as e:
        print(f"Błąd ładowania pliku konfiguracyjnego: {e}")
        sys.exit(1)

    simulation = Simulation(board, max_number_of_steps=args.max_steps, stop_simulation=True)
    video = Video(simulation)
    result = video.video_run()

    fig, ax = plt.subplots()
    ax.set_xlim(0, board.cols)
    ax.set_ylim(0, board.rows)
    ax.set_aspect('equal')
    ax.axis('off')

    frames_data = result['frames']

    def animate(i):
        ax.clear()
        ax.imshow(frames_data[i], cmap='binary', origin='upper')
        ax.set_title(f'Krok {i}')
        ax.axis('off')

    ani = animation.FuncAnimation(fig, animate, frames=len(frames_data), interval=1000/args.fps, repeat=False)

    try:
        ani.save('simulation.gif', writer='pillow', fps=args.fps)
        print("Animacja zapisana jako simulation.gif")
    except Exception as e:
        print(f"Błąd zapisywania animacji: {e}")
        plt.show()

if __name__ == "__main__":
    main()