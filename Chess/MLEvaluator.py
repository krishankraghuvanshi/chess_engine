try:
    import torch
    import torch.nn as nn
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    print("PyTorch is not installed. ML evaluation is disabled. Run 'pip install torch' to use the ML model.")

class ChessBoardEvaluator(nn.Module if TORCH_AVAILABLE else object):
    def __init__(self):
        super().__init__()
        if not TORCH_AVAILABLE:
            return
        # A simple Multi-Layer Perceptron (MLP) for board evaluation
        # Input size: 64 squares * 12 piece types = 768
        self.fc1 = nn.Linear(768, 256)
        self.relu1 = nn.ReLU()
        self.fc2 = nn.Linear(256, 64)
        self.relu2 = nn.ReLU()
        self.fc3 = nn.Linear(64, 1)
        self.tanh = nn.Tanh() # Output between -1 (Black winning) and 1 (White winning)
    
    def forward(self, x):
        x = self.fc1(x)
        x = self.relu1(x)
        x = self.fc2(x)
        x = self.relu2(x)
        x = self.fc3(x)
        x = self.tanh(x)
        return x

def encode_board(board):
    """
    Encode the 2D board array into a 1D tensor of size 768.
    There are 12 piece types: wp, wR, wN, wB, wQ, wK, bp, bR, bN, bB, bQ, bK
    """
    import numpy as np
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
    piece_to_idx = {p: i for i, p in enumerate(pieces)}
    
    encoded = np.zeros((64, 12), dtype=np.float32)
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece != '--':
                encoded[r * 8 + c][piece_to_idx[piece]] = 1.0
                
    # Flatten to 768
    encoded = encoded.flatten()
    if TORCH_AVAILABLE:
        return torch.tensor(encoded).unsqueeze(0) # [1, 768]
    return encoded

ml_model = None

def init_model(weights_path=None):
    global ml_model
    if not TORCH_AVAILABLE:
        print("ML Evaluator not initialized because PyTorch is missing.")
        return False
        
    ml_model = ChessBoardEvaluator()
    if weights_path:
        try:
            ml_model.load_state_dict(torch.load(weights_path))
            print(f"Loaded ML model weights from {weights_path}")
        except Exception as e:
            print(f"Could not load weights: {e}. Using random weights.")
    else:
        print("Using randomly initialized ML model weights. Train the model for accurate chess evaluations.")
        
    ml_model.eval()
    return True

def evaluate_board_ml(board):
    """
    Returns a score from the ML model.
    Scales the output from [-1, 1] to a typical chess score range (e.g. [-10000, 10000]).
    """
    if not TORCH_AVAILABLE or ml_model is None:
        return 0 # Fallback
        
    encoded_state = encode_board(board)
    with torch.no_grad():
        score = ml_model(encoded_state).item()
        
    return score * 10000 # Scale up to match material score magnitude
