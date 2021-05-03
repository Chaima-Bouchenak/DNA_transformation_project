# ADN SEQUENCE PROCESSING using the Burrows Wheeler Transform (BWT) and the Huffman Transformation

What is the Burrows-Wheeler Transform?
The BWT is a data transformation algorithm that restructures data in such a way that the transformed message is more compressible. Technically, it is a lexicographical reversible permutation of the characters of a string. It is first of the three steps to be performed in succession while implementing the Burrows-Wheeler Data Compression algorithm that forms the basis of the Unix compression utility bzip2.

The most important application of BWT is found in biological sciences where genomes(long strings written in A, C, T, G alphabets) don’t have many runs but they do have many repeats.


How about Huffman coding ? it's a lossless data compression algorithm. The idea is to assign variable-length codes to input characters, lengths of the assigned codes are based on the frequencies of corresponding characters. The most frequent character gets the smallest code and the least frequent character gets the largest code.
The variable-length codes assigned to input characters are Prefix Codes, means the codes (bit sequences) are assigned in such a way that the code assigned to one character is not the prefix of code assigned to any other character. This is how Huffman Coding makes sure that there is no ambiguity when decoding the generated bitstream. 

And here comes our project, 
Apply the idea of the BWT and the Huffman coding algorithm using Python in order to compress genome sequences.

The user can either enter the DNA sequence manually or with a specific file 

it contains Four major processes :
* BWT transformation
* BWT retransformation
* Huffman compression
* Huffman decompression



<!-- User manuel -->
To get a local copy up and running follow these simple steps
PLEASE USE A LINUX DISCRIBUTION OPERATING SYSTEM.

### 1. Get the project on your local machine
* Clone the repository locally

  ```sh
  git clone https://github.com/Chaima-Bouchenak/DNA_transformation_project.git
  
  cd DNA_transformation_project/
  ```

### 2. Start the app
   ```sh
   cd project_scripts/
   ```
     
### 3. Run the script
```sh
   python main.py
   ```
Re run this command of each process use.
