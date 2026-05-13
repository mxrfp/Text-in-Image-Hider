# Image Text Injector and Decoder

## Overview
The Image Text Injector and Decoder is a specialized, Python-based steganography utility designed to embed and extract arbitrary text payloads within digital image files. By utilizing a custom Least Significant Bit (LSB) modification algorithm, the software allows users to conceal sensitive text data inside standard image arrays without introducing visual distortions detectable by the human eye. 

This tool is strictly implemented for local execution, ensuring that sensitive data manipulation remains entirely within the user's operational environment.

## Key Features
* **Lossless Data Injection:** Modifies only the least significant bits of the image's primary color channel, preserving the structural and visual integrity of the original file.
* **Automated Header Allocation:** Dynamically calculates and allocates a structural header within the first pixel row to precisely define the payload boundaries, ensuring accurate extraction.
* **Dynamic Capacity Verification:** Automatically computes the maximum bit-capacity of the target image and validates the payload length before injection to prevent buffer overflow or data corruption.
* **Memory-Efficient Matrix Operations:** Leverages the NumPy library to handle multidimensional image arrays, ensuring rapid translation between spatial pixel coordinates and binary data structures.
* **Automated Output Management:** Generates an isolated `injected_imgs` directory to safely store processed assets without overwriting the original source files.

## System Requirements
To execute this utility, the host environment must possess the following components:

* **Python:** Version 3.7 or higher.
* **Pillow (PIL):** Required for reading, rendering, and exporting image files in a lossless format.
* **NumPy:** Required for multidimensional array parsing and matrix transformations.

## Installation
1. Ensure Python is installed and added to the system PATH.
2. Clone or download the script to a dedicated local directory.
3. Install the required external dependencies via the Python Package Installer (pip):

```bash
pip install Pillow numpy
```

## Usage Guide
The application operates via a Command Line Interface (CLI) that provides a linear, user-prompted workflow. Run the script using the following command:

```bash
python <script_name>.py
```

Upon execution, the terminal will present a standard menu prompting the user to select an operational mode.

### Mode 1: Inject Text (Encoding)
1. Input `1` when prompted for the operation mode.
2. Provide the absolute or relative file path to the source image (e.g., `C:\assets\source_image.jpg`). The application automatically sanitizes the input by removing extraneous quotation marks typical of drag-and-drop operations.
3. Input the plaintext message to be embedded. The system will evaluate the text length against the available spatial data of the image.
4. Upon successful injection, the modified image is automatically exported to a newly generated `injected_imgs` directory within the script's root folder. The output file is strictly saved in the `.png` format to prevent lossy compression algorithms from destroying the LSB data.

### Mode 2: Decode Text (Extraction)
1. Input `2` when prompted for the operation mode.
2. Provide the file path to the previously processed `.png` file containing the hidden payload.
3. The algorithm will scan the first row of pixels to identify the header, calculate the structural boundaries of the payload, and extract the original plaintext to the console.

## Technical Architecture

The software utilizes a deterministic, channel-specific LSB algorithm divided into three core procedural stages: string serialization, header injection, and payload distribution.

### 1. Serialization (`str_to_bin`)
The plaintext message is broken down character by character. Each character is converted into its decimal ASCII equivalent and then serialized into a strictly padded 7-bit binary string. This standardizes the payload format and ensures precise pixel allocation.

### 2. Header Protocol (Row 0 Allocation)
The algorithm dictates that the entirety of the first row (Index 0) is reserved for metadata—specifically, the bit-length of the injected message. 
* The length of the binary payload is calculated and converted into a binary string.
* This length string is right-aligned to the end of the first pixel row. 
* The application modifies the LSB of the first color channel (typically Red) for each pixel. Preceding pixels that do not contain the length data are padded with a `0` LSB. 
* During extraction, the decoder scans this row for the first instance of a `1` LSB, which acts as the delimiter initiating the length value.

### 3. Payload Distribution (Row 1 to N)
The serialized text data is injected sequentially beginning at the second row (Index 1). 
* The algorithm iterates through the spatial coordinates of the image matrix.
* For each pixel, the LSB of the first color channel is overwritten with the corresponding bit from the payload.
* Once the binary string is completely embedded, the loop breaks, and the remaining untouched pixel data is appended directly to the output array to preserve the rest of the image.
* The extraction process reverses this logic: it reads exactly the amount of bits dictated by the header, groups them into 7-bit chunks, and deserializes them back into ASCII characters.

## Limitations and Constraints
* **Lossy Compression Compatibility:** The steganographic integrity relies on exact pixel values. Transmitting the resulting `.png` file through platforms that apply lossy compression (such as standard messaging applications or social media) will corrupt the LSB data and permanently destroy the hidden payload.
* **Storage Capacity:** The maximum payload capacity is strictly correlated to the pixel dimensions of the image minus the first row. Specifically, an image can hold `(Width * (Height - 1)) / 7` characters.
* **Channel Specificity:** The current implementation exclusively alters the `[0]` index of each pixel array. If an image is provided in grayscale or a non-standard color space, the behavior of the injection and decoding logic may become unpredictable.
