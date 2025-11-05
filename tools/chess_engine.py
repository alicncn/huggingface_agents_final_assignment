"""Chess engine tools for analyzing positions and finding best moves."""
import chess
import chess.engine
from typing import Optional
from langchain_core.tools import tool


@tool
def analyze_chess_fen(fen: str, depth: int = 15) -> str:
    """
    Analyze a chess position given in FEN notation and find the best move.
    
    Args:
        fen: Position in FEN (Forsyth-Edwards Notation)
        depth: Search depth for analysis (default: 15)
    
    Returns:
        Best move and position evaluation
    """
    try:
        # Parse the FEN position
        board = chess.Board(fen)
        
        # Validate the position
        if not board.is_valid():
            return f"Error: Invalid chess position: {fen}"
        
        # Check for game over
        if board.is_game_over():
            if board.is_checkmate():
                return f"Game Over: Checkmate! {'White' if board.turn == chess.BLACK else 'Black'} wins."
            elif board.is_stalemate():
                return "Game Over: Stalemate (Draw)"
            elif board.is_insufficient_material():
                return "Game Over: Draw by insufficient material"
            else:
                return "Game Over: Draw"
        
        # Use basic evaluation without an engine
        # Count material and position
        evaluation = evaluate_position(board)
        
        # Find best move using the chess library's legal moves
        legal_moves = list(board.legal_moves)
        
        if not legal_moves:
            return "No legal moves available"
        
        # Simple evaluation: try each move and pick the best
        best_move = None
        best_score = float('-inf') if board.turn == chess.WHITE else float('inf')
        
        for move in legal_moves:
            board.push(move)
            score = evaluate_position(board)
            board.pop()
            
            if board.turn == chess.WHITE:
                if score > best_score:
                    best_score = score
                    best_move = move
            else:
                if score < best_score:
                    best_score = score
                    best_move = move
        
        result = []
        result.append(f"Position: {fen}")
        result.append(f"Turn: {'White' if board.turn == chess.WHITE else 'Black'}")
        result.append(f"\nPosition evaluation: {evaluation:.2f}")
        result.append(f"(Positive favors White, Negative favors Black)")
        result.append(f"\nBest move: {best_move.uci()} ({board.san(best_move)})")
        result.append(f"Expected evaluation after move: {best_score:.2f}")
        
        # Add some context about the move
        board.push(best_move)
        if board.is_check():
            result.append("This move gives check!")
        board.pop()
        
        result.append(f"\nTotal legal moves: {len(legal_moves)}")
        
        return "\n".join(result)
        
    except ValueError as e:
        return f"Error parsing FEN: {str(e)}"
    except Exception as e:
        return f"Error analyzing position: {str(e)}"


def evaluate_position(board: chess.Board) -> float:
    """
    Simple position evaluation based on material count.
    Returns positive for White advantage, negative for Black advantage.
    """
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0
    }
    
    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            value = piece_values[piece.piece_type]
            if piece.color == chess.WHITE:
                score += value
            else:
                score -= value
    
    return score


@tool
def get_chess_position_info(fen: str) -> str:
    """
    Get detailed information about a chess position.
    
    Args:
        fen: Position in FEN notation
    
    Returns:
        Detailed information about the position
    """
    try:
        board = chess.Board(fen)
        
        result = []
        result.append(f"FEN: {fen}")
        result.append(f"\nPosition:")
        result.append(str(board))
        result.append(f"\nTurn: {'White' if board.turn == chess.WHITE else 'Black'}")
        result.append(f"Move number: {board.fullmove_number}")
        
        # Castling rights
        castling = []
        if board.has_kingside_castling_rights(chess.WHITE):
            castling.append("White O-O")
        if board.has_queenside_castling_rights(chess.WHITE):
            castling.append("White O-O-O")
        if board.has_kingside_castling_rights(chess.BLACK):
            castling.append("Black O-O")
        if board.has_queenside_castling_rights(chess.BLACK):
            castling.append("Black O-O-O")
        
        if castling:
            result.append(f"Castling rights: {', '.join(castling)}")
        else:
            result.append("Castling rights: None")
        
        # Check status
        if board.is_check():
            result.append("Status: IN CHECK")
        
        # Material count
        white_material = 0
        black_material = 0
        piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9
        }
        
        for piece_type, value in piece_values.items():
            white_count = len(board.pieces(piece_type, chess.WHITE))
            black_count = len(board.pieces(piece_type, chess.BLACK))
            white_material += white_count * value
            black_material += black_count * value
        
        result.append(f"\nMaterial: White {white_material} - Black {black_material}")
        result.append(f"Legal moves: {board.legal_moves.count()}")
        
        return "\n".join(result)
        
    except Exception as e:
        return f"Error getting position info: {str(e)}"


@tool
def validate_chess_move(fen: str, move: str) -> str:
    """
    Check if a move is legal in a given position.
    
    Args:
        fen: Position in FEN notation
        move: Move in UCI format (e.g., 'e2e4') or SAN (e.g., 'Nf3')
    
    Returns:
        Whether the move is legal and the resulting position
    """
    try:
        board = chess.Board(fen)
        
        # Try to parse move
        try:
            chess_move = board.parse_san(move)
        except:
            try:
                chess_move = chess.Move.from_uci(move)
            except:
                return f"Error: Could not parse move '{move}'. Use UCI (e2e4) or SAN (Nf3) format."
        
        # Check if move is legal
        if chess_move in board.legal_moves:
            board.push(chess_move)
            result = []
            result.append(f"Move '{move}' is LEGAL")
            result.append(f"\nResulting position:")
            result.append(str(board))
            result.append(f"\nNew FEN: {board.fen()}")
            
            if board.is_check():
                result.append("This move gives CHECK")
            if board.is_checkmate():
                result.append("This move is CHECKMATE!")
            
            return "\n".join(result)
        else:
            return f"Move '{move}' is ILLEGAL in this position"
        
    except Exception as e:
        return f"Error validating move: {str(e)}"
