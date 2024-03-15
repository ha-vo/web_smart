## The model of the chatbot was uploaded to hugging face at the address "https://huggingface.co/summerB2014567/finetunninggpt2"

## Loading model
    from transformers import GPT2LMHeadModel, GPT2Tokenizer
    model = GPT2LMHeadModel.from_pretrained("summerB2014567/finetunninggpt2")
    tokenizer = GPT2Tokenizer.from_pretrained("summerB2014567/finetunninggpt2")
