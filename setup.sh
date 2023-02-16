#!/bin/bash

# Update package lists and install Tesseract OCR
apt-get update
apt-get install -y tesseract-ocr

# Add Tesseract OCR to PATH
echo 'export PATH=/usr/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
