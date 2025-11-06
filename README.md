# 🌱 AI Plant Disease Detector

A complete web application for detecting plant diseases in crops using Deep Learning CNN with transfer learning.

## Overview

This application uses a Convolutional Neural Network (CNN) with transfer learning from MobileNetV2 to detect diseases in:
- 🍅 **Tomato** (10 disease classes + healthy)
- 🌽 **Corn/Maize** (4 disease classes + healthy) 
- 🥔 **Potato** (3 disease classes + healthy)

**Total Classes:** 17 plant conditions across 3 crop types

## Features

### ✨ Current Implementation
- **Image Upload Interface** - Drag-and-drop or browse for crop leaf images
- **Transfer Learning Model** - MobileNetV2 (ImageNet pre-trained) + custom classification head
- **Real-time Predictions** - Instant disease detection with confidence scores
- **Top-3 Predictions** - View alternative diagnoses with probabilities
- **Comprehensive Disease Database** - Detailed information on:
  - Symptoms
  - Treatment recommendations
  - Prevention measures
  - Pathogen information
- **Responsive UI** - Works on desktop, tablet, and mobile browsers
- **Error Handling** - Robust error management and user feedback
- **Low Confidence Warnings** - Alerts users when predictions are uncertain

### 🚀 Architecture
