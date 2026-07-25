# Repo Analyzer Keywords

Load when classifying task type, stack, or architecture.

## Task type

| type | keywords | file cues |
|------|----------|-----------|
| CV | image, cv2, PIL, resnet, vit, unet, detection, segmentation, classification | image datasets; torchvision, mmcv |
| NLP | text, token, bert, gpt, transformer, llm, sentence, corpus | transformers, datasets, tokenizers |
| RL | policy, agent, environment, reward, ppo, dqn, sac, gym, env | env loop; reward fn |
| Robotics | robot, kinematics, dynamics, simulation, gazebo, ros, control | physics sim; robot models |
| Multimodal | image-text, vision-language, clip, multimodal, cross-modal | dual image+text paths |
| Time series | timeseries, forecast, temporal, sequence, lstm, gru | temporal dims |
| Generative | gan, diffusion, vae, generative, generation, synthesize | generator / diffusion loop |

## Frameworks

| framework | cues |
|-----------|------|
| PyTorch | `import torch`, `nn.Module` |
| TensorFlow | `import tensorflow`, `tf.keras` |
| JAX/Flax | `import jax`, flax, haiku, optax |
| MxNet | `import mxnet`, gluon |
| PaddlePaddle | `import paddle` |

## Aux libraries

- CV: torchvision, mmcv, detectron2, albumentations
- NLP: transformers, datasets, tokenizers, nltk, spacy
- RL: gym, stable-baselines3, ray[rllib]
- Science: numpy, scipy, pandas, matplotlib
- Tracking: wandb, mlflow, tensorboard
- Distributed: torch.distributed, deepspeed, accelerate

## Architecture tokens

Transformer, Attention, Self-Attention, Cross-Attention, CNN, ResNet, ViT, Swin, U-Net, FPN, RNN, LSTM, GRU, Seq2Seq, GNN, GCN, GAT, GAN, Diffusion, VAE, Flow

## Algorithm dig sites

- losses: `loss =`, `criterion =`, `loss_fn`
- novel modules / nonstandard layer names
- augmentation pipeline
- optimizers / LR schedules
