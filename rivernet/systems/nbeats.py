import matplotlib.pyplot as plt
import pl_bolts
import torch
import wandb
from einops import repeat
from rivernet.modules import Module
from rivernet.modules.loss import LpLoss

from .base import System


@System.register('nbeats')
class NBEATSSystem(System):
    def __init__(self, model: Module, backcast_length: int,
                 forecast_length: int,  model_path: str = None):
        super().__init__()
        self.model = model
        self.backcast_len = backcast_length
        self.forecast_len = forecast_length

    def forward(self, x):
        x = self.model(x)
        return x

    def _learning_step(self, batch):
        views, log_views = batch
        # x.shape == [batch_size, seq_len]

        sources = log_views[:, :self.backcast_len]
        targets = views[:, -self.forecast_len:]

        _, X = self.model(sources)
        preds = torch.exp(X)
        numerator = torch.abs(targets - preds)
        denominator = torch.abs(targets) + torch.abs(preds)
        loss = 200 * numerator / denominator
        loss[torch.isnan(loss)] = 0
        loss = loss.mean()

        return loss

    def training_step(self, batch, batch_idx):
        loss = self._learning_step(batch)
        self.log('train_loss', loss)
        return loss

    def validation_step(self, batch, batch_idx):
        loss = self._learning_step(batch)
        self.log('valid_loss', loss)

    def test_step(self, batch, batch_idx):
        loss = self._learning_step(batch)
        self.log('test_loss', loss)

    def configure_optimizers(self):
        opt = torch.optim.AdamW(
            self.parameters(), lr=1e-4, weight_decay=1e-4)
        scheduler = pl_bolts.optimizers.lr_scheduler.LinearWarmupCosineAnnealingLR(
            opt, warmup_epochs=1, max_epochs=5)
        return [opt], [scheduler]