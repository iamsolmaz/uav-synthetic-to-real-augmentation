# Data Augmentation Pipeline for Enhanced UAV Surveillance

Official repository for the paper:

**Data Augmentation Pipeline for Enhanced UAV Surveillance**
Solmaz Arezoomandan, John Klohoker, David K. Han
*Pattern Recognition. ICPR 2024, Lecture Notes in Computer Science, Springer*

[[Paper]](https://link.springer.com/chapter/10.1007/978-3-031-78172-8_24)
[[DOI]](https://doi.org/10.1007/978-3-031-78172-8_24)
[[Project Page]](https://iamsolmaz.github.io/uav-synthetic-to-real-augmentation/)

---

## Overview

Long-range UAV detection is challenging because drones are often small, low-resolution, and difficult to distinguish from cluttered backgrounds. Collecting and annotating large-scale real UAV datasets is also expensive.

This work presents a data augmentation pipeline for improving UAV detection by combining synthetic UAV image generation, synthetic-to-real image translation, and object detection training. Synthetic UAV images are first generated in a simulation environment and then translated toward the real image domain using CycleGAN. The augmented data is used to train YOLO-based UAV detectors and evaluate their generalization on unseen real-world UAV surveillance datasets.

---

## Method

The proposed pipeline consists of three main stages:

1. **Synthetic UAV image generation**
   Synthetic UAV images are generated in a simulation environment to increase the diversity of the training data.

2. **Synthetic-to-real image translation**
   CycleGAN is used to reduce the visual domain gap between synthetic and real UAV images.

3. **UAV detector training and evaluation**
   YOLO-based object detectors are trained using different combinations of real, synthetic, and translated synthetic images. The trained detectors are then evaluated on unseen real-world UAV datasets.

---

## Project Page

The project page is available here:

https://iamsolmaz.github.io/uav-synthetic-to-real-augmentation/

---

## Code and Data

Code, configuration files, and reproducibility instructions will be added to this repository.

Dataset access and additional resources will be provided based on availability and sharing permissions.

---

## Citation

If you find this work useful, please cite:

```bibtex
@inproceedings{arezoomandan2025data,
  title={Data Augmentation Pipeline for Enhanced UAV Surveillance},
  author={Arezoomandan, Solmaz and Klohoker, John and Han, David K.},
  booktitle={Pattern Recognition. ICPR 2024},
  series={Lecture Notes in Computer Science},
  volume={15306},
  pages={366--380},
  year={2025},
  publisher={Springer},
  doi={10.1007/978-3-031-78172-8_24}
}
```

---

## Contact

For questions about this work, please contact:

**Solmaz Arezoomandan**

