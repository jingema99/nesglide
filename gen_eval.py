#gen_eval.py
import argparse
from glob import glob
import os
import json

import numpy as np
import torch as th
import torchvision.transforms as T
from tqdm import trange

from glide_finetune.glide_finetune import run_glide_finetune_epoch
from glide_finetune.glide_util import load_model, sample
from glide_finetune.loader import TextImageDataset
from glide_finetune.train_util import wandb_setup, pred_to_pil
from glide_finetune.wds_loader import glide_wds_loader
from glide_text2im.nes import NES



def run_glide_finetune(
    data_dir="./data",
    batch_size=1,
    learning_rate=1e-5,
    adam_weight_decay=0.0,
    side_x=64,
    side_y=64,
    resize_ratio=1.0,
    uncond_p=0.0,
    resume_ckpt="",
    checkpoints_dir="./finetune_checkpoints",
    use_fp16=False,  # Tends to cause issues,not sure why as the paper states fp16 is stable.
    device="cpu",
    freeze_transformer=False,
    freeze_diffusion=False,
    project_name="glide_finetune",
    activation_checkpointing=False,
    use_captions=True,
    num_epochs=100,
    log_frequency=100,
    test_prompt="a group of skiers are preparing to ski down a mountain.",
    sample_bs=1,
    sample_gs=8.0,
    use_webdataset=False,
    image_key="jpg",
    caption_key="txt",
    enable_upsample=False,
    upsample_factor=4,
    image_to_upsample='low_res_face.png',
    max_text_len=3,
    vocab_path = "/content/nesglide/CLEVR_short.json",
    xf_width = 512,
):
    if "~" in data_dir:
        data_dir = os.path.expanduser(data_dir)
    if "~" in checkpoints_dir:
        checkpoints_dir = os.path.expanduser(checkpoints_dir)

    # Create the checkpoint/output directories
    os.makedirs(checkpoints_dir, exist_ok=True)

    # Start wandb logging
    wandb_run = wandb_setup(
        batch_size=batch_size,
        side_x=side_x,
        side_y=side_y,
        learning_rate=learning_rate,
        use_fp16=use_fp16,
        device=device,
        data_dir=data_dir,
        base_dir=checkpoints_dir,
        project_name=project_name,
    )
    print("Wandb setup.")


    print("Loading data...")
    f = open(vocab_path)
    vocab_dict = json.load(f) 
    f.close()


    # Model setup
    glide_model, glide_diffusion, glide_options = load_model(
        glide_path=resume_ckpt,
        use_fp16=use_fp16,
        freeze_transformer=freeze_transformer,
        freeze_diffusion=freeze_diffusion,
        activation_checkpointing=activation_checkpointing,
        model_type="base" if not enable_upsample else "upsample",
        xf_width=xf_width,
    )
    glide_model.train()
    number_of_params = sum(x.numel() for x in glide_model.parameters())
    print(f"Number of parameters in GLIDE: {number_of_params}")
    number_of_trainable_params = sum(
        x.numel() for x in glide_model.parameters() if x.requires_grad
    )
    print(f"Trainable parameters in GLIDE: {number_of_trainable_params}")

    #NES model setup
    nes_model = NES(text_ctx=max_text_len, n_vocab=len(vocab_dict), xf_width=xf_width)

    if resume_ckpt == "":
      pass     
    else:
      glide_name = resume_ckpt.split("/")[-1]
      root_weights_dir = resume_ckpt.replace(glide_name,'')
      nes_name = glide_name.replace("glide",'nes')
      nes_resume_ckpt = root_weights_dir + nes_name
      try:
        nes_weights = th.load(nes_resume_ckpt, map_location="cpu")
        nes_model.load_state_dict(nes_weights)
        print("nes weights loaded successfully")
      except:
        print("no nes weights loaded")


    
    glide_model.to(device)
    nes_model.to(device)

    glide_model.eval()
    nes_model.eval()

    outputs_dir = "./outputs"
    os.makedirs(outputs_dir, exist_ok=True)


    txt_dict = {}
    folder_path = test_prompt
    files = os.listdir(folder_path)
    for file_name in files:
        with open(os.path.join(folder_path, file_name), "r") as f:
            content = f.read()
            txt_dict[file_name] = content


    for txt_name, prompt in txt_dict.items():
      samples = sample(
              glide_model=glide_model,
              nes_model=nes_model,
              glide_options=glide_options,
              side_x=side_x,
              side_y=side_y,
              prompt=prompt,
              batch_size=sample_bs,
              guidance_scale=sample_gs,
              device=device,
              image_to_upsample=image_to_upsample,
              vocab_dict=vocab_dict,
              max_text_len=max_text_len,
          )
      sample_save_path = os.path.join(outputs_dir, txt_name.replace(".txt", ".png"))
      pred_to_pil(samples).save(sample_save_path)
      print(f"Saved sample {sample_save_path}")



def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", "-data", type=str, default="./data")
    parser.add_argument("--batch_size", "-bs", type=int, default=1)
    parser.add_argument("--learning_rate", "-lr", type=float, default=2e-5)
    parser.add_argument("--adam_weight_decay", "-adam_wd", type=float, default=0.0)
    parser.add_argument("--side_x", "-x", type=int, default=64)
    parser.add_argument("--side_y", "-y", type=int, default=64)
    parser.add_argument(
        "--resize_ratio", "-crop", type=float, default=0.8, help="Crop ratio"
    )
    parser.add_argument(
        "--uncond_p",
        "-p",
        type=float,
        default=0.2,
        help="Probability of using the empty/unconditional token instead of a caption. OpenAI used 0.2 for their finetune.",
    )
    parser.add_argument(
        "--train_upsample",
        "-upsample",
        action="store_true",
        help="Train the upsampling type of the model instead of the base model.",
    )
    parser.add_argument(
        "--resume_ckpt",
        "-resume",
        type=str,
        default="",
        help="Checkpoint to resume from",
    )
    parser.add_argument(
        "--checkpoints_dir", "-ckpt", type=str, default="./glide_checkpoints/"
    )
    parser.add_argument("--use_fp16", "-fp16", action="store_true")
    parser.add_argument("--device", "-dev", type=str, default="")
    parser.add_argument("--log_frequency", "-freq", type=int, default=100)
    parser.add_argument("--freeze_transformer", "-fz_xt", type=bool, default=False)
    parser.add_argument("--freeze_diffusion", "-fz_unet", action="store_true")
    parser.add_argument("--project_name", "-name", type=str, default="glide-finetune")
    parser.add_argument("--activation_checkpointing", "-grad_ckpt", action="store_true")
    parser.add_argument("--use_captions", "-txt", action="store_true")
    parser.add_argument("--epochs", "-epochs", type=int, default=20)
    parser.add_argument(
        "--test_prompt",
        "-prompt",
        type=str,
        default="a group of skiers are preparing to ski down a mountain.",
    )
    parser.add_argument(
        "--test_batch_size",
        "-tbs",
        type=int,
        default=1,
        help="Batch size used for model eval, not training.",
    )
    parser.add_argument(
        "--test_guidance_scale",
        "-tgs",
        type=float,
        default=4.0,
        help="Guidance scale used during model eval, not training.",
    )
    parser.add_argument(
        "--use_webdataset",
        "-wds",
        action="store_true",
        help="Enables webdataset (tar) loading",
    )
    parser.add_argument(
        "--wds_image_key",
        "-wds_img",
        type=str,
        default="jpg",
        help="A 'key' e.g. 'jpg' used to access the image in the webdataset",
    )
    parser.add_argument(
        "--wds_caption_key",
        "-wds_cap",
        type=str,
        default="txt",
        help="A 'key' e.g. 'txt' used to access the caption in the webdataset",
    )
    parser.add_argument(
        "--wds_dataset_name",
        "-wds_name",
        type=str,
        default="laion",
        help="Name of the webdataset to use (laion or alamy)",
    )
    parser.add_argument("--seed", "-seed", type=int, default=0)
    parser.add_argument(
        "--cudnn_benchmark",
        "-cudnn",
        action="store_true",
        help="Enable cudnn benchmarking. May improve performance. (may not)",
    )
    parser.add_argument(
        "--upscale_factor", "-upscale", type=int, default=4, help="Upscale factor for training the upsampling model only"
    )
    parser.add_argument("--image_to_upsample", "-lowres", type=str, default="low_res_face.png")
    parser.add_argument("--max_text_len", "-maxlen", type=int, default=3)
    parser.add_argument("--vocab_path", "-vocab", type=str, default="/content/nesglide/CLEVR_short.json")
    parser.add_argument("--xf_width", "-width", type=int, default=512)

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    # CUDA/CPU setup
    args = parse_args()
    if len(args.device) > 0:
        device = th.device(args.device)
    else:
        device = th.device("cpu") if not th.cuda.is_available() else th.device("cuda")

    th.manual_seed(args.seed)
    np.random.seed(args.seed)
    th.backends.cudnn.benchmark = args.cudnn_benchmark

    for arg in vars(args):
        print(f"--{arg} {getattr(args, arg)}")

    if args.use_webdataset:
        # webdataset uses tars
        data_dir = glob(os.path.join(args.data_dir, "*.tar"))
    else:
        data_dir = args.data_dir
    print(args.freeze_transformer)
    
    run_glide_finetune(
        data_dir=args.data_dir,
        batch_size=args.batch_size,
        learning_rate=args.learning_rate,
        adam_weight_decay=args.adam_weight_decay,
        side_x=args.side_x,
        side_y=args.side_y,
        resize_ratio=args.resize_ratio,
        uncond_p=args.uncond_p,
        resume_ckpt=args.resume_ckpt,
        checkpoints_dir=args.checkpoints_dir,
        use_fp16=args.use_fp16,
        device=device,
        log_frequency=args.log_frequency,
        freeze_transformer=args.freeze_transformer,
        freeze_diffusion=args.freeze_diffusion,
        project_name=args.project_name,
        activation_checkpointing=args.activation_checkpointing,
        use_captions=args.use_captions,
        num_epochs=args.epochs,
        test_prompt=args.test_prompt,
        sample_bs=args.test_batch_size,
        sample_gs=args.test_guidance_scale,
        use_webdataset=args.use_webdataset,
        image_key=args.wds_image_key,
        caption_key=args.wds_caption_key,
        enable_upsample=args.train_upsample,
        upsample_factor=args.upscale_factor,
        image_to_upsample=args.image_to_upsample,
        max_text_len = args.max_text_len,
        vocab_path = args.vocab_path,
        xf_width= args.xf_width,
    )
#gen_eval.py
