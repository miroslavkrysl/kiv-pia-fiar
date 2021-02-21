from datetime import datetime
from enum import Enum, auto
from typing import Optional

from fiar.data.models import User, Friendship, Game, Move, MoveResult
from fiar.persistence.sqlalchemy.repositories.game import GameRepo
from fiar.persistence.sqlalchemy.repositories.invite import InviteRepo
from fiar.persistence.sqlalchemy.repositories.move import MoveRepo


class GameService:
    """
    Various game logic.
    """

    def __init__(self,
                 game_repo: GameRepo,
                 invite_repo: InviteRepo,
                 move_repo: MoveRepo,
                 board_size: int):
        assert board_size >= 5

        self.game_repo = game_repo
        self.invite_repo = invite_repo
        self.move_repo = move_repo
        self.board_size = board_size

    def give_up(self, player: int, game: Game):
        """
        Give up game. Sets ended_at datetime to now and winner to other player.
        :param player: Player who gives up - 0 for O, 1 for X.
        :param game: Game.
        """
        assert player == 0 or player == 1
        game.winner = 0 if player == 1 else 1
        game.ended_at = datetime.now()

    def do_move(self, game: Game, side: int, row: int, col: int) -> MoveResult:
        """
        Perform a game move. Checks board bounds and field emptiness.
        :param game: Game.
        :param side: Player - 0 for O, 1 for X.
        :param row: Row number.
        :param col: Col number.
        :return: MoveResult.
        """
        assert side == 0 or side == 1

        if row < 0 or row >= self.board_size:
            return MoveResult.INVALID

        if col < 0 or col >= self.board_size:
            return MoveResult.INVALID

        if self.is_cell_occupied(game, row, col):
            return MoveResult.INVALID

        move = Move(game.id, side, row, col)
        self.move_repo.add(move)

        if self.check_fiar(game, side, row, col):
            return MoveResult.WINNER

        if self.is_full(game):
            return MoveResult.DRAW

        return MoveResult.OK

    def accept_invite(self, user: User, opponent: User) -> Game:
        """
        Accept an invite. Creates a new game and removes pending invites between the two users.
        :param user: User
        :param opponent: Opponent - who invites.
        """
        game = Game(user.id, opponent.id)
        self.game_repo.add(game)

        self.remove_pending_invites(user, opponent)

        return game

    def remove_invite(self, user: User, opponent: User):
        """
        Remove an invite. Removes pending invites between the two users.
        :param user: User
        :param opponent: Opponent - who invites.
        """
        self.remove_pending_invites(user, opponent)

    def get_player_side(self, player: User, game: Game) -> Optional[int]:
        """
        Get the player side - 0 for O, 1 for X.
        :param player: Player.
        :param game: Game.
        :return: The player side number or None if player is not in game.
        """
        if player.id == game.player_o_id:
            return 0
        elif player.id == game.player_x_id:
            return 1
        else:
            return None

    def is_invite_pending(self, user: User, opponent: User) -> bool:
        """
        Check whether there is a pending invite between users.
        :param user: User.
        :param opponent: Opponent.
        :return: True if an invite is pending, False otherwise.
        """
        return self.invite_repo.get_by_users(user, opponent) is not None \
               or self.invite_repo.get_by_users(opponent, user) is not None

    def has_received_invite(self, user: User, sender: User) -> bool:
        """
        Check whether the user has received an invite from sender.
        :param user: User.
        :param sender: Sender.
        :return: True if an invite was received, False otherwise.
        """
        return self.invite_repo.get_by_users(sender, user) is not None

    def remove_pending_invites(self, user: User, friend: User):
        invite1 = self.invite_repo.get_by_users(user, friend)
        invite2 = self.invite_repo.get_by_users(friend, user)

        if invite1:
            self.invite_repo.delete(invite1)

        if invite2:
            self.invite_repo.delete(invite2)

    def is_cell_occupied(self, game: Game, row: int, col: int) -> bool:
        """
        Check if the cell is occupied.
        :param game: Game.
        :param row: Row number.
        :param col: Col number.
        :return: True if occupied, false otherwise.
        """
        move = self.move_repo.get_by_game_and_pos(game, row, col)
        return move is not None

    def check_fiar(self, game: Game, side: int, row: int, col: int) -> bool:
        """
        Check if there is five in a row containing the given cell.
        :param side: Side - 0 for O, 1 for X.
        :param row: Cell row number.
        :param col: Cell col number.
        :param game: Game.
        :return: True if is, false otherwise.
        """
        # horizontal check
        in_line = 0
        for c in range(col - 4, col + 5):
            move = self.move_repo.get_by_game_and_pos(game, row, c)

            if move is None or move.side != side:
                in_line = 0
            else:
                in_line += 1

        if in_line == 5:
            return True

        # vertical check
        in_line = 0
        for r in range(row - 4, row + 5):
            move = self.move_repo.get_by_game_and_pos(game, r, col)

            if move is None or move.side != side:
                in_line = 0
            else:
                in_line += 1

        if in_line == 5:
            return True

        # diagonal down
        in_line = 0
        for r, c in range(row - 4, row + 5), range(col - 4, col + 5):
            move = self.move_repo.get_by_game_and_pos(game, r, c)

            if move is None or move.side != side:
                in_line = 0
            else:
                in_line += 1

        if in_line == 5:
            return True

        # diagonal up
        in_line = 0
        for r, c in reversed(range(row - 4, row + 5)), range(col - 4, col + 5):
            move = self.move_repo.get_by_game_and_pos(game, r, c)

            if move is None or move.side != side:
                in_line = 0
            else:
                in_line += 1

        if in_line == 5:
            return True

        return False

    def is_full(self, game: Game) -> bool:
        """
        Check if the game board is full.
        :param game: Game.
        :return: True if full, false otherwise.
        """
        count = self.move_repo.count_by_game(game)
        return count == self.board_size * self.board_size
