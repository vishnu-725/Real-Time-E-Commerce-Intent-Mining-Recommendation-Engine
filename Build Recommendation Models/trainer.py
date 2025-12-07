

import os
import time
from typing import Any, Dict
import torch
from torch.utils.data import DataLoader
from phase3.utils import get_logger, ensure_dir

logger = get_logger(__name__)

def train_epoch(model: torch.nn.Module, dataloader: DataLoader, optimizer, device: str):
    model.train()
    total_loss = 0.0
    count = 0
    for batch in dataloader:
        inputs, targets = batch
        inputs = inputs.to(device)
        targets = targets.to(device)
        optimizer.zero_grad()
        logits = model(inputs)  # (batch, vocab_size)
        loss = torch.nn.functional.cross_entropy(logits, targets)
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * inputs.size(0)
        count += inputs.size(0)
    return total_loss / max(1, count)

def evaluate_epoch(model: torch.nn.Module, dataloader: DataLoader, device: str, k: int = 10):
    model.eval()
    top1 = 0
    total = 0
    with torch.no_grad():
        for batch in dataloader:
            inputs, targets = batch
            inputs = inputs.to(device)
            targets = targets.to(device)
            logits = model(inputs)  # (batch, vocab)
            _, topk = logits.topk(k, dim=1)
            topk = topk.cpu().numpy()
            t = targets.cpu().numpy()
            for i in range(len(t)):
                total += 1
                if t[i] in topk[i]:
                    top1 += 1
    return top1 / max(1, total)

def save_checkpoint(state: Dict[str, Any], checkpoint_dir: str, filename: str = "checkpoint.pth"):
    ensure_dir(checkpoint_dir)
    path = os.path.join(checkpoint_dir, filename)
    torch.save(state, path)
    logger.info("Saved checkpoint to %s", path)

def load_checkpoint(checkpoint_path: str, model: torch.nn.Module = None, optimizer = None):
    if not os.path.exists(checkpoint_path):
        raise FileNotFoundError(checkpoint_path)
    state = torch.load(checkpoint_path, map_location='cpu')
    if model is not None and 'model_state_dict' in state:
        model.load_state_dict(state['model_state_dict'])
    if optimizer is not None and 'optimizer_state_dict' in state:
        optimizer.load_state_dict(state['optimizer_state_dict'])
    logger.info("Loaded checkpoint from %s", checkpoint_path)
    return state
