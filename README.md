# AI Digital Security Surveillance App

## Overview

This project is designed to run on a live Arch Linux environment. It includes tools for digital security and forensic analysis, such as John the Ripper, Hashcat, and Python. This document provides a step-by-step guide for setting up and running the application.

## Requirements

- A USB drive with Arch Linux installed
- Basic familiarity with Linux commands
- Internet connection for installing dependencies

## Installation and Setup

### 1. Prepare the Live USB

1. **Install Arch Linux on a USB Drive**
   - Follow the [Arch Linux installation guide](https://wiki.archlinux.org/title/Installation_guide) to install Arch Linux on your USB drive.

2. **Boot from the USB Drive**
   - Restart your computer and boot from the USB drive containing Arch Linux.

### 2. Install Required Tools

Once you have booted into Arch Linux, open a terminal and run the following commands to install the necessary tools and dependencies:

bash
sudo pacman -Syu  # Update the system
sudo pacman -S john hashcat python hashid

3. Update John the Ripper
Download and Update John the Ripper's Source File

Download the latest source code and apply updates to support the office2john script:
git clone https://github.com/openwall/john.git
cd john/src

