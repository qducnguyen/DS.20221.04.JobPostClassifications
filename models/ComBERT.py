# Refer to https://www.kaggle.com/trnmtin/phobert-classification-for-vietnamese-text

# Refer to https://towardsdatascience.com/how-to-combine-textual-and-numerical-features-for-machine-learning-in-python-dc1526ca94d9


from transformers import AutoModel

import torch
from torch import nn


class ComPhoBERTModel(nn.Module):
  
    def __init__(self,in_dimensions, dense_size, num_classes):

        self.in_dimensions = in_dimensions
        self.dense_size = dense_size

        super(ComPhoBERTModel, self).__init__()
        self.bert = AutoModel.from_pretrained("vinai/phobert-base")
        self.drop = nn.Dropout(p=0.3)

        self.fc_1 = nn.Linear(self.bert.config.hidden_size, self.dense_size)
        self.fc_2 = nn.Linear(self.dense_size + self.in_dimensions , num_classes)

        nn.init.normal_(self.fc_1.weight, std=0.02)
        nn.init.normal_(self.fc_1.bias, 0)

        nn.init.normal_(self.fc_2.weight, std=0.02)
        nn.init.normal_(self.fc_2.bias, 0)


    def forward(self, x_batch):
        
        x_text, x_num = x_batch

        input_ids = x_text['input_ids']
        attention_masks = x_text['attention_masks']        

        _, output = self.bert(
            input_ids=input_ids,
            attention_mask=attention_masks,
            return_dict=False # Dropout will errors if without this
        )

        x = self.drop(output)

        dense_out = self.fc_1(x)

        concat_layer = torch.concat([dense_out, x_num], dim=1)

        out = self.fc_2(concat_layer)

        return out


