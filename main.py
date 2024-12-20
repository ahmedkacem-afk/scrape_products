import Vidange
import PieceAuto
import AutoPiece

if __name__ == "__main__":
    user_input = input("Enter the search term for auto spare parts: ")   
    if user_input:
        Vidange.Vidange(user_input)
        PieceAuto.Vidange(user_input)
        AutoPiece.Vidange(user_input)
    Vidange.Vidange()
    PieceAuto.Vidange()
    AutoPiece.Vidange()

