#!/usr/bin/env python3
"""
Script to generate figures for the IEEE conference paper
"Real-Time Steering Angle Estimation via Monocular Depth Profiling and 1D Free-Space Analysis"
"""

import os
import subprocess
import matplotlib.pyplot as plt
import numpy as np
import cv2
import torch
from depth_anything_v2.dpt import DepthAnythingV2

def ensure_dir(directory):
    """Ensure that a directory exists."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def generate_system_architecture():
    """Generate the system architecture diagram from the GraphViz description."""
    print("Generating system architecture diagram...")
    
    # Check if GraphViz is installed
    try:
        subprocess.run(["dot", "-V"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: GraphViz is not installed or not in PATH.")
        print("Please install GraphViz (https://graphviz.org/) and try again.")
        return False
    
    # Generate the diagram
    try:
        subprocess.run(
            ["dot", "-Tpng", "images/system_architecture.txt", "-o", "figures/system_architecture.png"],
            check=True
        )
        print("System architecture diagram generated successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error generating system architecture diagram: {e}")
        return False

def generate_depth_comparison(image_path, output_path="figures/depth_comparison.png"):
    """Generate a comparison of depth maps from different model variants."""
    print("Generating depth map comparison...")
    
    # Load the input image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not load image from {image_path}")
        return False
    
    # Convert BGR to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Define model configurations
    model_configs = {
        'vits': {'encoder': 'vits', 'features': 64, 'out_channels': [48, 96, 192, 384]},
        'vitb': {'encoder': 'vitb', 'features': 128, 'out_channels': [96, 192, 384, 768]},
        'vitl': {'encoder': 'vitl', 'features': 256, 'out_channels': [256, 512, 1024, 1024]},
        'vitg': {'encoder': 'vitg', 'features': 384, 'out_channels': [1536, 1536, 1536, 1536]}
    }
    
    # Check if CUDA is available
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    # Create a figure with subplots
    fig, axes = plt.subplots(1, 5, figsize=(15, 3))
    
    # Add the original image
    axes[0].imshow(image_rgb)
    axes[0].set_title("Original RGB")
    axes[0].axis('off')
    
    # Process with each model variant
    for i, model_name in enumerate(['vits', 'vitb', 'vitl', 'vitg']):
        try:
            # Load the model
            model = DepthAnythingV2(**model_configs[model_name])
            model.to(device)
            
            # Generate depth map
            depth = model.infer_image(image)
            
            # Display the depth map
            axes[i+1].imshow(depth, cmap='plasma')
            axes[i+1].set_title(f"Depth ({model_name})")
            axes[i+1].axis('off')
            
        except Exception as e:
            print(f"Error processing with {model_name} model: {e}")
            axes[i+1].text(0.5, 0.5, f"Error: {model_name}", ha='center', va='center')
            axes[i+1].axis('off')
    
    # Save the figure
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    
    print("Depth map comparison generated successfully.")
    return True

def generate_free_space_profile(image_path, output_path="figures/free_space_profile.png"):
    """Generate a visualization of the 1D free-space analysis."""
    print("Generating free-space profile visualization...")
    
    # Load the input image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not load image from {image_path}")
        return False
    
    # Convert BGR to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Define ROI
    roi_top_frac = 0.6
    roi_bottom_frac = 1.0
    h, w = image_rgb.shape[:2]
    top_y = int(h * roi_top_frac)
    bottom_y = int(h * roi_bottom_frac)
    
    # Draw ROI on the image
    image_with_roi = image_rgb.copy()
    cv2.line(image_with_roi, (0, top_y), (w, top_y), (255, 0, 0), 2)
    cv2.line(image_with_roi, (0, bottom_y), (w, bottom_y), (255, 0, 0), 2)
    
    # Load the model
    model_config = {'encoder': 'vits', 'features': 64, 'out_channels': [48, 96, 192, 384]}
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    try:
        # Load the model
        model = DepthAnythingV2(**model_config)
        model.to(device)
        
        # Generate depth map
        depth = model.infer_image(image_rgb)
        
        # Crop depth map to ROI
        depth_roi = depth[top_y:bottom_y, :]
        
        # Compute 1D profile
        profile = np.mean(depth_roi, axis=0)
        inversion = -profile + np.max(profile)
        safest_idx = np.argmax(inversion)
        
        # Create a figure with subplots
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        
        # Original image with ROI
        axes[0].imshow(image_with_roi)
        axes[0].set_title("RGB Image with ROI")
        axes[0].axis('off')
        
        # Depth map
        axes[1].imshow(depth, cmap='plasma')
        axes[1].set_title("Depth Map")
        axes[1].axis('off')
        
        # 1D profile
        axes[2].plot(inversion)
        axes[2].axvline(x=safest_idx, color='r', linestyle='--', label='Safest Path')
        axes[2].axvline(x=len(inversion)//2, color='g', linestyle='--', label='Center')
        axes[2].set_title("1D Free-Space Profile")
        axes[2].set_xlabel("Column Index")
        axes[2].set_ylabel("Inverted Cost")
        axes[2].legend()
        
        # Save the figure
        plt.tight_layout()
        plt.savefig(output_path, dpi=300)
        plt.close()
        
        print("Free-space profile visualization generated successfully.")
        return True
        
    except Exception as e:
        print(f"Error generating free-space profile: {e}")
        return False

def generate_environments(image_paths, output_path="figures/environments.png"):
    """Generate a visualization of system performance in different environments."""
    print("Generating environments visualization...")
    
    if len(image_paths) < 4:
        print("Error: Need at least 4 images for different environments.")
        return False
    
    # Create a figure with subplots
    fig, axes = plt.subplots(4, 3, figsize=(15, 20))
    
    # Load the model
    model_config = {'encoder': 'vits', 'features': 64, 'out_channels': [48, 96, 192, 384]}
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    try:
        # Load the model
        model = DepthAnythingV2(**model_config)
        model.to(device)
        
        # Process each environment
        for i, image_path in enumerate(image_paths[:4]):
            # Load the input image
            image = cv2.imread(image_path)
            if image is None:
                print(f"Error: Could not load image from {image_path}")
                continue
            
            # Convert BGR to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Define ROI
            roi_top_frac = 0.6
            roi_bottom_frac = 1.0
            h, w = image_rgb.shape[:2]
            top_y = int(h * roi_top_frac)
            bottom_y = int(h * roi_bottom_frac)
            
            # Generate depth map
            depth = model.infer_image(image_rgb)
            
            # Compute 1D profile
            depth_roi = depth[top_y:bottom_y, :]
            profile = np.mean(depth_roi, axis=0)
            inversion = -profile + np.max(profile)
            
            # Original image
            axes[i, 0].imshow(image_rgb)
            axes[i, 0].set_title(f"Environment {i+1}")
            axes[i, 0].axis('off')
            
            # Depth map
            axes[i, 1].imshow(depth, cmap='plasma')
            axes[i, 1].set_title("Depth Map")
            axes[i, 1].axis('off')
            
            # 1D profile
            axes[i, 2].plot(inversion)
            axes[i, 2].axvline(x=np.argmax(inversion), color='r', linestyle='--')
            axes[i, 2].set_title("Free-Space Profile")
            axes[i, 2].set_xlabel("Column Index")
            axes[i, 2].set_ylabel("Inverted Cost")
        
        # Save the figure
        plt.tight_layout()
        plt.savefig(output_path, dpi=300)
        plt.close()
        
        print("Environments visualization generated successfully.")
        return True
        
    except Exception as e:
        print(f"Error generating environments visualization: {e}")
        return False

def main():
    """Main function to generate all figures."""
    # Ensure the figures directory exists
    ensure_dir("figures")
    
    # Generate system architecture diagram
    generate_system_architecture()
    
    # Check if sample images are available
    if os.path.exists("sample_images"):
        # Generate depth comparison
        sample_image = os.path.join("sample_images", "sample1.jpg")
        if os.path.exists(sample_image):
            generate_depth_comparison(sample_image)
        else:
            print(f"Warning: Sample image {sample_image} not found.")
        
        # Generate free-space profile
        generate_free_space_profile(sample_image)
        
        # Generate environments visualization
        environment_images = [
            os.path.join("sample_images", f"sample{i}.jpg") for i in range(1, 5)
        ]
        generate_environments(environment_images)
    else:
        print("Warning: sample_images directory not found.")
        print("Please create a sample_images directory with sample1.jpg, sample2.jpg, etc.")

if __name__ == "__main__":
    main()
