import time

import torch
import wandb
from torch.utils.data import ConcatDataset

from TrainingInterfaces.Text_to_Spectrogram.FastSpeech2.FastSpeech2 import FastSpeech2
from TrainingInterfaces.Text_to_Spectrogram.FastSpeech2.meta_train_loop import train_loop
from Utility.corpus_preparation import prepare_fastspeech_corpus
from Utility.path_to_transcript_dicts import *


def run(gpu_id, resume_checkpoint, finetune, model_dir, resume, use_wandb, wandb_resume_id):
    if gpu_id == "cpu":
        os.environ["CUDA_VISIBLE_DEVICES"] = ""
        device = torch.device("cpu")

    else:
        os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
        os.environ["CUDA_VISIBLE_DEVICES"] = f"{gpu_id}"
        device = torch.device("cuda")

    torch.manual_seed(131714)
    random.seed(131714)
    torch.random.manual_seed(131714)

    print("Preparing")

    if model_dir is not None:
        save_dir = model_dir
    else:
        save_dir = os.path.join("Models", "FastSpeech2_Quechua")  # KEEP THE 'FastSpeech2_' BUT CHANGE THE MODEL ID TO SOMETHING MEANINGFUL FOR YOUR DATA
    os.makedirs(save_dir, exist_ok=True)

    datasets = list()
    datasets.append(
        prepare_fastspeech_corpus(
            transcript_dict=build_path_to_transcript_dict_quechua(),
            corpus_dir=os.path.join("Corpora", "Quechua"),
            lang="qu"))  

    datasets.append(
        prepare_fastspeech_corpus(
            transcript_dict=build_path_to_transcript_dict_libritts_clean_360(),
            corpus_dir=os.path.join("Corpora", "LibriTTS"),
            lang="en"))  

    #train_set = ConcatDataset(datasets)
    if use_wandb:
        wandb.init(
            name=f"{__name__.split('.')[-1]}_{time.strftime('%Y%m%d-%H%M%S')}" if wandb_resume_id is None else None,
            id=wandb_resume_id,  # this is None if not specified in the command line arguments.
            resume="must" if wandb_resume_id is not None else None)
    model = FastSpeech2()
    if resume_checkpoint is None: 
        path_to_checkpoint="Models/FastSpeech2_Meta/best.pt"
    else:
        path_to_checkpoint= resume_checkpoint    
    train_loop(net=model,
               datasets=datasets,
               device=device,
               save_directory=save_dir,
               batch_size=8,                 
               lr=0.001,
               warmup_steps=4000,               
               path_to_checkpoint=path_to_checkpoint,
               path_to_embed_model="Models/Embedding/embedding_function.pt",               
               resume=resume,
               phase_1_steps=50000,
               phase_2_steps=50000,
               steps_per_checkpoint=1000,
               use_wandb=use_wandb)
    if use_wandb:
        wandb.finish()
