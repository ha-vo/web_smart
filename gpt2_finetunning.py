import os
import requests
import json
from transformers import TextDataset, DataCollatorForLanguageModeling
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from transformers import Trainer, TrainingArguments

os.mkdir("squad")

url = 'https://rajpurkar.github.io/SQuAD-explorer/dataset/'
for file in ['train-v2.0.json','dev-v2.0.json']:
    res = requests.get(f'{url}{file}')
    with open(f'squad/{file}','wb') as f:
        for chunk in res.iter_content(chunk_size=4):
            f.write(chunk)

def write_data_to_txt(path):
    with open(path, 'rb') as f:
        dict_squad = json.load(f)
    result = ""
    filename = os.path.splitext(path)[0] + '.txt'
    with open(filename, "w", encoding="utf-8") as f:
        for data in dict_squad['data']:
            for para in data['paragraphs']:
                cnt = para['context']
                for qas in para['qas']:
                    ques = qas['question']
                    if 'plausible_answers' in qas.keys():
                        access = 'plausible_answers'
                    else:
                        access = 'answers'
                    for ans in qas[access]:
                        if ques is not None and ans['text'] is not None:
                            f.write(f"[Q] {ques}")
                            f.write(f"[A] {ans['text']}")
                        break
write_data_to_txt('squad/train-v2.0.json')
write_data_to_txt('squad/dev-v2.0.json')

filename_train = "squad/train-v2.0.txt"
filename_val = "squad/dev-v2.0.txt"

def read_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
    return text


def load_dataset(file_path, tokenizer, block_size = 128):
    dataset = TextDataset(
        tokenizer = tokenizer,
        file_path = file_path,
        block_size = block_size,
    )
    return dataset

def load_data_collator(tokenizer, mlm = False):
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=mlm,
    )
    return data_collator

def train(num_train_epochs,
          save_steps,
          per_device_train_batch_size,
          output_dir,
          model):
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    train_dataset = load_dataset(filename_train, tokenizer)
    tokenizer.save_pretrained(output_dir)
    data_collator = load_data_collator(tokenizer)
    model = model
    model.save_pretrained(output_dir)

    trainnig_args = TrainingArguments(
            output_dir = output_dir,
            overwrite_output_dir = False,
            per_device_train_batch_size=per_device_train_batch_size,
            num_train_epochs=num_train_epochs,
            save_steps = save_steps
        )

    trainer = Trainer(
            model = model,
            args = trainnig_args,
            data_collator=data_collator,
            train_dataset=train_dataset,
        )
    trainer.train()
    trainer.save_model()

per_device_train_batch_size = 8
num_train_epochs = 80.0
save_steps = 50000
output_dir = "gpt2"
model = GPT2LMHeadModel.from_pretrained("gpt2")

train(
    num_train_epochs,
    save_steps,
    per_device_train_batch_size,
    output_dir,
    model
)
