# IEEE Conference Paper: Real-Time Steering Angle Estimation

This directory contains the LaTeX source for the IEEE conference paper titled "Real-Time Steering Angle Estimation via Monocular Depth Profiling and 1D Free-Space Analysis".

## Paper Structure

The paper follows the standard IEEE conference paper format and includes the following sections:

1. **Abstract** - Summary of the paper's content and contributions
2. **Introduction** - Background, motivation, and overview of the approach
3. **Related Work** - Discussion of prior research in monocular depth estimation and free-space detection
4. **System Architecture** - Detailed description of the system components and workflow
5. **Implementation Details** - Hardware/software setup, camera calibration, and performance optimizations
6. **Experimental Results** - Evaluation of depth estimation quality, steering angle accuracy, and computational performance
7. **Discussion and Future Work** - Limitations of the current approach and directions for improvement
8. **Conclusion** - Summary of contributions and potential applications
9. **References** - Citations to related work

## Required Figures

The paper references several figures that need to be created:

1. **system_architecture.png** - A diagram showing the system architecture
   - Use the GraphViz description in `images/system_architecture.txt` to generate this figure
   - Alternatively, create a flowchart showing the data flow from camera input to steering angle output

2. **free_space_profile.png** - Visualization of the 1D free-space analysis
   - Follow the description in `images/depth_profile_example.txt`
   - Show the original RGB image, depth map, and 1D profile with the safest path marked

3. **depth_comparison.png** - Comparison of depth maps from different model variants
   - Take a single input image and process it with different Depth-Anything-V2 variants (vits, vitb, vitl, vitg)
   - Arrange the results in a grid for comparison

4. **environments.png** - System performance in different environments
   - Show examples of the system operating in various scenarios (urban, rural, indoor, low-light)
   - For each scenario, include the RGB image, depth map, and free-space profile

## Compiling the Paper

To compile the LaTeX paper, you'll need a LaTeX distribution installed (e.g., TeX Live, MiKTeX).

```bash
# Compile the paper
pdflatex real_time_steering_paper.tex
bibtex real_time_steering_paper
pdflatex real_time_steering_paper.tex
pdflatex real_time_steering_paper.tex
```

This will generate `real_time_steering_paper.pdf`, which is the final paper.

## Figure Generation

### System Architecture Diagram

To generate the system architecture diagram from the GraphViz description:

```bash
dot -Tpng images/system_architecture.txt -o figures/system_architecture.png
```

### Other Figures

The other figures should be created using screenshots and visualizations from the running system:

1. Run the system with different configurations and environments
2. Capture screenshots of the RGB input, depth maps, and free-space profiles
3. Arrange the screenshots according to the descriptions in the paper
4. Save the arranged images in the `figures` directory with the appropriate names

## Paper Submission

Before submitting the paper:

1. Ensure all figures are properly referenced and described in the text
2. Check that the paper adheres to the page limit (6-8 pages)
3. Verify that all references are properly formatted and cited
4. Remove any template text or instructions from the final version

## Contact

For questions or assistance with the paper, please contact:
- Gnanendra Naidun (gnaidun@ucsf.edu)
- Jane Smith (jsmith@stanford.edu)
