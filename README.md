# Synthetic-to-Real UAV Data Augmentation for Enhanced Drone Detection

This repository contains code and resources related to our published paper:

**Data Augmentation Pipeline for Enhanced UAV Surveillance**  
Solmaz Arezoomandan, John Klohoker, David K. Han  
Published in *Pattern Recognition, ICPR 2024, Lecture Notes in Computer Science, Springer*.

Paper: https://doi.org/10.1007/978-3-031-78172-8_24

## Overview

This project explores a synthetic-to-real data augmentation pipeline for UAV detection. The pipeline first generates synthetic UAV imagery using Unreal Engine, then translates the synthetic images toward the real-image domain using CycleGAN. The translated synthetic data is used to augment real training data and improve YOLO-based drone detection.

## Pipeline

```text
Unreal Engine Synthetic Data
        ↓
CycleGAN Synthetic-to-Real Translation
        ↓
Real + Translated Synthetic Training Data
        ↓
YOLO Drone Detector
        ↓
Evaluation on Real UAV Images
