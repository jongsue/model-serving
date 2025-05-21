import torch
import torch.nn as nn

class YourModel(nn.Module):
    def __init__(self):
        super(YourModel, self).__init__()
        # 예시 모델 구조 (실제 모델로 대체)
        self.layers = nn.Sequential(
            nn.Linear(100, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 10)  # 출력 크기는 요구사항에 맞게 조정
        )
    
    def forward(self, x):
        # 입력 데이터 형태: [8000, 100]
        return self.layers(x)