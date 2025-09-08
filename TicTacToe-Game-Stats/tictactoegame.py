def play_game(self):
    """
    Main game loop that handles complete game sessions.

    Manages:
    - Player setup and database initialization
    - Multiple game rounds with same players
    - Game state management (moves, winner checking)
    - Statistics updates after each game
    - Play again functionality

    Game Flow:
    1. Setup players (once per session)
    2. Play individual games (multiple rounds possible)
    3. Update statistics after each game
    4. Show current stats
    5. Ask if players want to continue
    """
    self.setup_players()  # Get player names and setup database

    # Main game session loop (allows multiple games)
    while True:
        self.reset_game()  # Start with clean board
        print(f"\n=== NEW GAME ===")

        # Individual game loop (one complete game)
        while True:
            self.display_board()  # Show current board state

            # Determine current player name for display
            current_name = (self.player1_name if self.current_player == 'X'else self.player2_name)


import sqlite3
import os
from datetime import datetime


class TicTacToeStats:
    def __init__(self, db_name="tictactoe_stats.db"):
        self.db_name = db_name
        self.init_database()

    def init_database(self):
        """Initialize the SQLite database and create tables if they don't exist."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                matches_played INTEGER DEFAULT 0,
                wins INTEGER DEFAULT 0,
                losses INTEGER DEFAULT 0,
                draws INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player1_name TEXT NOT NULL,
                player2_name TEXT NOT NULL,
                winner TEXT,
                game_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (player1_name) REFERENCES players (name),
                FOREIGN KEY (player2_name) REFERENCES players (name)
            )
        ''')

        conn.commit()
        conn.close()

    def add_player(self, name):
        """Add a new player to the database."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        try:
            cursor.execute('INSERT INTO players (name) VALUES (?)', (name,))
            conn.commit()
            print(f"Player '{name}' added successfully!")
        except sqlite3.IntegrityError:
            print(f"Player '{name}' already exists!")

        conn.close()

    def get_player_stats(self, name):
        """Get statistics for a specific player."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT name, matches_played, wins, losses, draws 
            FROM players WHERE name = ?
        ''', (name,))

        result = cursor.fetchone()
        conn.close()

        if result:
            return {
                'name': result[0],
                'matches_played': result[1],
                'wins': result[2],
                'losses': result[3],
                'draws': result[4],
                'win_rate': (result[2] / result[1] * 100) if result[1] > 0 else 0
            }
        return None

    def update_player_stats(self, player_name, result):
        """Update player statistics after a game."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        if result == 'win':
            cursor.execute('''
                UPDATE players 
                SET matches_played = matches_played + 1, wins = wins + 1 
                WHERE name = ?
            ''', (player_name,))
        elif result == 'loss':
            cursor.execute('''
                UPDATE players 
                SET matches_played = matches_played + 1, losses = losses + 1 
                WHERE name = ?
            ''', (player_name,))
        elif result == 'draw':
            cursor.execute('''
                UPDATE players 
                SET matches_played = matches_played + 1, draws = draws + 1 
                WHERE name = ?
            ''', (player_name,))

        conn.commit()
        conn.close()

    def record_game(self, player1, player2, winner):
        """Record a game in the database."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO games (player1_name, player2_name, winner)
            VALUES (?, ?, ?)
        ''', (player1, player2, winner))

        conn.commit()
        conn.close()

    def get_all_players(self):
        """Get all players and their statistics."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT name, matches_played, wins, losses, draws 
            FROM players 
            ORDER BY wins DESC, matches_played DESC
        ''')

        results = cursor.fetchall()
        conn.close()

        return results

    def display_leaderboard(self):
        """Display the leaderboard."""
        players = self.get_all_players()

        if not players:
            print("No players found!")
            return

        print("\n" + "=" * 60)
        print("                    LEADERBOARD")
        print("=" * 60)
        print(f"{'Name':<15} {'Matches':<8} {'Wins':<6} {'Losses':<7} {'Draws':<6} {'Win Rate':<8}")
        print("-" * 60)

        for player in players:
            name, matches, wins, losses, draws = player
            win_rate = (wins / matches * 100) if matches > 0 else 0
            print(f"{name:<15} {matches:<8} {wins:<6} {losses:<7} {draws:<6} {win_rate:<8.1f}%")
        print("=" * 60)


class TicTacToeGame:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
        self.stats = TicTacToeStats()
        self.player1_name = ""
        self.player2_name = ""

    def display_board(self):
        """Display the current state of the board."""
        print("\n   |   |   ")
        print(f" {self.board[0]} | {self.board[1]} | {self.board[2]} ")
        print("___|___|___")
        print("   |   |   ")
        print(f" {self.board[3]} | {self.board[4]} | {self.board[5]} ")
        print("___|___|___")
        print("   |   |   ")
        print(f" {self.board[6]} | {self.board[7]} | {self.board[8]} ")
        print("   |   |   \n")

        print("Positions:")
        print(" 1 | 2 | 3 ")
        print("___|___|___")
        print(" 4 | 5 | 6 ")
        print("___|___|___")
        print(" 7 | 8 | 9 ")
        print()

    def is_valid_move(self, position):
        """Check if the move is valid."""
        return 0 <= position <= 8 and self.board[position] == ' '

    def make_move(self, position):
        """Make a move on the board."""
        if self.is_valid_move(position):
            self.board[position] = self.current_player
            return True
        return False

    def check_winner(self):
        """Check if there's a winner."""
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]

        for combo in winning_combinations:
            if (self.board[combo[0]] == self.board[combo[1]] ==
                    self.board[combo[2]] != ' '):
                return self.board[combo[0]]

        if ' ' not in self.board:
            return 'Draw'

        return None

    def switch_player(self):
        """Switch to the other player."""
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def reset_game(self):
        """Reset the game board."""
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'

    def setup_players(self):
        """Set up player names and add them to database if needed."""
        print("=== TIC-TAC-TOE GAME ===\n")

        self.player1_name = input("Enter Player 1 name (X): ").strip()
        self.player2_name = input("Enter Player 2 name (O): ").strip()

        # Add players to database
        self.stats.add_player(self.player1_name)
        self.stats.add_player(self.player2_name)

        print(f"\n{self.player1_name} (X) vs {self.player2_name} (O)")

    def play_game(self):
        """Main game loop."""
        self.setup_players()

        while True:
            self.reset_game()
            print(f"\n=== NEW GAME ===")

            # Game loop
            while True:
                self.display_board()

                current_name = (self.player1_name if self.current_player == 'X'
                                else self.player2_name)

                try:
                    move = int(input(f"{current_name} ({self.current_player}), "
                                     f"enter position (1-9): ")) - 1

                    if not self.make_move(move):
                        print("Invalid move! Try again.")
                        continue

                except (ValueError, IndexError):
                    print("Please enter a number between 1 and 9.")
                    continue

                # Check for winner
                result = self.check_winner()
                if result:
                    self.display_board()

                    if result == 'Draw':
                        print("It's a draw!")
                        # Update stats for draw
                        self.stats.update_player_stats(self.player1_name, 'draw')
                        self.stats.update_player_stats(self.player2_name, 'draw')
                        self.stats.record_game(self.player1_name, self.player2_name, 'Draw')
                    else:
                        winner_name = (self.player1_name if result == 'X'
                                       else self.player2_name)
                        loser_name = (self.player2_name if result == 'X'
                                      else self.player1_name)

                        print(f"🎉 {winner_name} ({result}) wins!")

                        # Update stats
                        self.stats.update_player_stats(winner_name, 'win')
                        self.stats.update_player_stats(loser_name, 'loss')
                        self.stats.record_game(self.player1_name, self.player2_name, winner_name)

                    break

                self.switch_player()

            # Show updated stats
            print("\n=== CURRENT STATS ===")
            stats1 = self.stats.get_player_stats(self.player1_name)
            stats2 = self.stats.get_player_stats(self.player2_name)

            if stats1:
                print(f"{stats1['name']}: {stats1['wins']}W-{stats1['losses']}L-"
                      f"{stats1['draws']}D (Win Rate: {stats1['win_rate']:.1f}%)")

            if stats2:
                print(f"{stats2['name']}: {stats2['wins']}W-{stats2['losses']}L-"
                      f"{stats2['draws']}D (Win Rate: {stats2['win_rate']:.1f}%)")

            # Ask if players want to play again
            while True:
                choice = input("\nPlay again? (y/n): ").lower().strip()
                if choice in ['y', 'yes']:
                    break
                elif choice in ['n', 'no']:
                    return
                else:
                    print("Please enter 'y' for yes or 'n' for no.")


def main():
    """Main function to run the game."""
    game = TicTacToeGame()

    while True:
        print("\n" + "=" * 40)
        print("      TIC-TAC-TOE WITH STATISTICS")
        print("=" * 40)
        print("1. Play Game")
        print("2. View Leaderboard")
        print("3. View Player Stats")
        print("4. Exit")
        print("-" * 40)

        try:
            choice = input("Enter your choice (1-4): ").strip()

            if choice == '1':
                game.play_game()

            elif choice == '2':
                game.stats.display_leaderboard()

            elif choice == '3':
                name = input("Enter player name: ").strip()
                stats = game.stats.get_player_stats(name)
                if stats:
                    print(f"\n=== STATS FOR {stats['name']} ===")
                    print(f"Matches Played: {stats['matches_played']}")
                    print(f"Wins: {stats['wins']}")
                    print(f"Losses: {stats['losses']}")
                    print(f"Draws: {stats['draws']}")
                    print(f"Win Rate: {stats['win_rate']:.1f}%")
                else:
                    print("Player not found!")

            elif choice == '4':
                print("Thanks for playing! Goodbye!")
                break

            else:
                print("Invalid choice! Please enter 1, 2, 3, or 4.")

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()