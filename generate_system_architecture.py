#!/usr/bin/env python3
"""
Generate system architecture diagram from DOT file.
This script converts the Graphviz DOT file to a PNG image.
"""

import subprocess
import os
import sys

def generate_system_architecture():
    """Generate system architecture PNG from DOT file."""
    dot_file = 'images/system_architecture.txt'
    png_file = 'images/system_architecture.png'
    
    if not os.path.exists(dot_file):
        print(f"Error: {dot_file} not found")
        return False
    
    try:
        # Try to use Graphviz to generate the PNG
        result = subprocess.run([
            'dot', '-Tpng', dot_file, '-o', png_file
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✓ Generated {png_file} from {dot_file}")
            return True
        else:
            print(f"Error running Graphviz: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("Graphviz 'dot' command not found. Trying to install...")
        
        # Try to install Graphviz
        try:
            if sys.platform == "darwin":  # macOS
                subprocess.run(['brew', 'install', 'graphviz'], check=True)
            elif sys.platform.startswith("linux"):  # Linux
                subprocess.run(['sudo', 'apt-get', 'install', '-y', 'graphviz'], check=True)
            else:
                print("Please install Graphviz manually for your platform")
                return False
                
            # Try again after installation
            result = subprocess.run([
                'dot', '-Tpng', dot_file, '-o', png_file
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✓ Generated {png_file} from {dot_file}")
                return True
            else:
                print(f"Error running Graphviz after installation: {result.stderr}")
                return False
                
        except subprocess.CalledProcessError:
            print("Failed to install Graphviz automatically")
            return False

def create_manual_architecture_diagram():
    """Create system architecture diagram manually using matplotlib."""
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from matplotlib.patches import FancyBboxPatch, ConnectionPatch
    
    print("Creating system architecture diagram manually...")
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Define colors
    input_color = '#E3F2FD'
    depth_color = '#F3E5F5'
    analysis_color = '#E8F5E8'
    steering_color = '#FFF3E0'
    
    # Box style
    box_style = "round,pad=0.1"
    
    # Input Processing cluster
    input_box = FancyBboxPatch((0.5, 5.5), 2.5, 2, boxstyle=box_style, 
                               facecolor=input_color, edgecolor='black', linewidth=1)
    ax.add_patch(input_box)
    ax.text(1.75, 7, 'Input Processing', ha='center', va='center', fontsize=12, fontweight='bold')
    
    # Camera Input
    camera_box = FancyBboxPatch((0.7, 6.2), 2.1, 0.5, boxstyle=box_style,
                                facecolor='lightblue', edgecolor='black')
    ax.add_patch(camera_box)
    ax.text(1.75, 6.45, 'Camera Input', ha='center', va='center', fontsize=10)
    
    # ROI Selection
    roi_box = FancyBboxPatch((0.7, 5.7), 2.1, 0.4, boxstyle=box_style,
                             facecolor='lightblue', edgecolor='black')
    ax.add_patch(roi_box)
    ax.text(1.75, 5.9, 'ROI Selection', ha='center', va='center', fontsize=10)
    
    # Depth Estimation cluster
    depth_cluster = FancyBboxPatch((4, 5.5), 3, 2, boxstyle=box_style,
                                   facecolor=depth_color, edgecolor='black', linewidth=1)
    ax.add_patch(depth_cluster)
    ax.text(5.5, 7, 'Depth Estimation', ha='center', va='center', fontsize=12, fontweight='bold')
    
    # Depth Model
    model_box = FancyBboxPatch((4.2, 6.2), 2.6, 0.5, boxstyle=box_style,
                               facecolor='plum', edgecolor='black')
    ax.add_patch(model_box)
    ax.text(5.5, 6.45, 'Depth-Anything-V2\nModel', ha='center', va='center', fontsize=10)
    
    # Depth Map
    map_box = FancyBboxPatch((4.2, 5.7), 2.6, 0.4, boxstyle=box_style,
                             facecolor='plum', edgecolor='black')
    ax.add_patch(map_box)
    ax.text(5.5, 5.9, 'Depth Map', ha='center', va='center', fontsize=10)
    
    # Free-Space Analysis cluster
    analysis_cluster = FancyBboxPatch((0.5, 2.5), 6.5, 2.5, boxstyle=box_style,
                                      facecolor=analysis_color, edgecolor='black', linewidth=1)
    ax.add_patch(analysis_cluster)
    ax.text(3.75, 4.7, 'Free-Space Analysis', ha='center', va='center', fontsize=12, fontweight='bold')
    
    # Profile Generation
    profile_box = FancyBboxPatch((0.7, 3.8), 2, 0.5, boxstyle=box_style,
                                 facecolor='lightgreen', edgecolor='black')
    ax.add_patch(profile_box)
    ax.text(1.7, 4.05, '1D Profile\nGeneration', ha='center', va='center', fontsize=10)
    
    # Cost Inversion
    inversion_box = FancyBboxPatch((2.9, 3.8), 2, 0.5, boxstyle=box_style,
                                   facecolor='lightgreen', edgecolor='black')
    ax.add_patch(inversion_box)
    ax.text(3.9, 4.05, 'Cost Inversion', ha='center', va='center', fontsize=10)
    
    # Safest Path
    safest_box = FancyBboxPatch((5.1, 3.8), 2, 0.5, boxstyle=box_style,
                                facecolor='lightgreen', edgecolor='black')
    ax.add_patch(safest_box)
    ax.text(6.1, 4.05, 'Safest Path\nIdentification', ha='center', va='center', fontsize=10)
    
    # Steering Calculation cluster
    steering_cluster = FancyBboxPatch((8.5, 2.5), 5, 2.5, boxstyle=box_style,
                                      facecolor=steering_color, edgecolor='black', linewidth=1)
    ax.add_patch(steering_cluster)
    ax.text(11, 4.7, 'Steering Calculation', ha='center', va='center', fontsize=12, fontweight='bold')
    
    # Trajectory Computation
    trajectory_box = FancyBboxPatch((8.7, 3.8), 2.1, 0.5, boxstyle=box_style,
                                    facecolor='moccasin', edgecolor='black')
    ax.add_patch(trajectory_box)
    ax.text(9.75, 4.05, 'Trajectory\nComputation', ha='center', va='center', fontsize=10)
    
    # Steering Angle
    angle_box = FancyBboxPatch((11.1, 3.8), 2.1, 0.5, boxstyle=box_style,
                               facecolor='moccasin', edgecolor='black')
    ax.add_patch(angle_box)
    ax.text(12.15, 4.05, 'Steering Angle\nCalculation', ha='center', va='center', fontsize=10)
    
    # Add arrows between components
    arrows = [
        # Input flow
        ((1.75, 6.2), (1.75, 6.1)),  # Camera to ROI
        ((3, 6.45), (4.2, 6.45)),     # ROI to Depth Model
        ((5.5, 6.2), (5.5, 6.1)),     # Model to Map
        ((5.5, 5.7), (3.75, 4.7)),    # Map to Analysis (curved)
        
        # Analysis flow
        ((2.7, 4.05), (2.9, 4.05)),   # Profile to Inversion
        ((4.9, 4.05), (5.1, 4.05)),   # Inversion to Safest
        ((7.1, 4.05), (8.7, 4.05)),   # Safest to Trajectory
        ((10.8, 4.05), (11.1, 4.05)), # Trajectory to Angle
    ]
    
    for start, end in arrows:
        if start == (5.5, 5.7) and end == (3.75, 4.7):  # Curved arrow
            arrow = ConnectionPatch(start, end, "data", "data",
                                  arrowstyle="->", shrinkA=5, shrinkB=5,
                                  mutation_scale=20, fc="black", ec="black",
                                  connectionstyle="arc3,rad=0.3")
        else:
            arrow = ConnectionPatch(start, end, "data", "data",
                                  arrowstyle="->", shrinkA=5, shrinkB=5,
                                  mutation_scale=20, fc="black", ec="black")
        ax.add_patch(arrow)
    
    plt.title('System Architecture: Real-Time Steering Angle Estimation', 
              fontsize=16, fontweight='bold', pad=20)
    
    # Save the figure
    os.makedirs('images', exist_ok=True)
    plt.savefig('images/system_architecture.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Generated images/system_architecture.png manually")
    return True

def main():
    """Main function to generate system architecture diagram."""
    print("Generating system architecture diagram...")
    
    # Try Graphviz first, fall back to manual creation
    if not generate_system_architecture():
        print("Falling back to manual diagram creation...")
        create_manual_architecture_diagram()
    
    # Copy to figures directory
    import shutil
    src = 'images/system_architecture.png'
    dst = 'figures/system_architecture.png'
    
    if os.path.exists(src):
        os.makedirs('figures', exist_ok=True)
        shutil.copy2(src, dst)
        print(f"✓ Copied {src} to {dst}")

if __name__ == "__main__":
    main()
