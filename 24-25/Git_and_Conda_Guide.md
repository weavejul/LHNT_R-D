# Git & Conda Guide

> There once was a team self-possessed \
Who needed some code for their tests\
They learned Git and Conda\
To run code upon-a\
And run all their trials without stress



---

## **What is Git?**
Git is a version control system that allows you to track changes in your code, collaborate with others, and manage different versions of your project efficiently. It helps developers work together without overwriting each other’s work.

## **What is Conda?**
Conda is a package and environment manager that simplifies software installation and management. With Conda, you can create isolated environments with specific dependencies and Python versions, making it easier to manage projects with different requirements.

---

## **Step-by-Step Guide**

### **1. Install Miniconda**
   - Download Miniconda (a barebones implementationn of conda) for your operating system [here](https://docs.conda.io/en/latest/miniconda.html) and follow the installation instructions.

### **2. Install Git**
   - Download and install Git from [Git's official site](https://git-scm.com/). Follow the installation instructions based on your operating system.

### **3. Clone the GitHub Repository**
   1. Open a terminal (Command Prompt on Windows, Terminal on Mac/Linux).
   2. Navigate to the folder you want to download the code into through the command line.
   3. Choose either the **SSH** or **HTTPS** method to clone the repository.

      #### **Using SSH (Recommended for GitHub users with SSH keys)**
      - Run the following command to clone a repository using SSH:
         ```bash
         git clone git@github.com:username/repository-name.git
         ```
      - **Example**:
         ```bash
         git clone git@github.com:LonghornNeurotech/LHNTDataCollection.git
         ```
      - **Explanation**:
         - `git clone`: Downloads the repository to your computer.
         - The SSH link (`git@github.com...`) allows for secure access if you've set up SSH keys with GitHub.
         - **Tip**: SSH is generally preferred as it doesn’t require re-entering credentials when interacting with GitHub after setting up SSH keys.

      #### **Using HTTPS**
      - Alternatively, you can clone the repository using HTTPS:
         ```bash
         git clone https://github.com/username/repository-name.git
         ```
      - **Example**:
         ```bash
         git clone https://github.com/LonghornNeurotech/LHNTDataCollection.git
         ```
      - **Explanation**:
         - HTTPS provides a straightforward way to clone repositories, especially for those without SSH keys set up.
         - You’ll need to enter your GitHub username and password (or a Personal Access Token) when prompted.
         - **Note**: HTTPS can be more convenient for quick access, but SSH is generally more secure and avoids repeated credential prompts.

   #### Getting the Repository Link from GitHub
      - Go to the GitHub repository page you want to clone.
      - Click the green **Code** button, then select either **SSH** or **HTTPS**.
      - Copy the link provided and replace it in the `git clone` command above.

   - Following these steps allows you to download the project files and begin collaborating smoothly.
### **4. Pull the Latest Changes from the Repository**
   - To update your local copy with the latest changes from the remote repository (e.g. if software makes changes to the code):
     ```bash
     git pull
     ```
   - **Explanation**: This command fetches and merges the latest updates from the repository into your local copy.
### **5. Create and Activate a Conda Environment**
   1. Run the following command to create a new environment:
      ```bash
      conda create -n LHNT python=3.9
      ```
      - **Explanation**: This command creates a new Conda environment called `LHNT` with Python version 3.9.
      - NOTE: *I believe we're using Python 3.9 for everything. I need to double check with Nathan.*
   2. Activate the environment:
      ```bash
      conda activate LHNT
      ```
      - **Explanation**: Activating the environment isolates your workspace, ensuring any package installed only affects this specific environment.

### **6. Install Required Packages**
   - _While in the environment_, install most required packages using:
     ```bash
     conda install numpy
     conda install matplotlib
     etc.
     ```
   - This will need to be done with a couple packages used by the data collection program. Some packages are native to a python install.
   - Some packages installatinos won't work with conda, and need to be installed into the conda environment using pip:
     ```bash
     pip install brainflow
     ```
   - **Explanation**: Conda and pip manage dependencies, so it installs and sets up packages needed for your project.

### **7. Deactivate the Conda Environment**
   - When you are done working in your conda env:
     ```bash
     conda deactivate
     ```
   - **Explanation**: This returns you to your base environment, ensuring your system remains clean and other projects are unaffected.

---

## **8. Requirements Files**

   To simplify the process of setting up your environment with all necessary packages, you can create a **requirements file**. This allows you to specify all the packages and their versions in a single file, which can be easily installed by others.

   #### **Create a Conda Environment YAML File**
   - While in your environment, export the installed packages into a YAML file with:
     ```bash
     conda env export > environment.yml
     ```
   - **Explanation**: This command saves a list of the current environment's packages and versions to a file named `environment.yml`.

   #### **Using a requirements.txt File for pip Packages**
   - If your project includes packages installed via `pip`, create a `requirements.txt` file:
     ```bash
     pip freeze > requirements.txt
     ```
   - **Explanation**: This saves the pip-installed packages to a file, which can be easily installed using `pip install -r requirements.txt`.

   #### **Installing from Requirements Files**
   - To recreate the environment, use the following commands:
     - Conda environment:
       ```bash
       conda env create -f environment.yml
       ```
     - Pip requirements:
       ```bash
       pip install -r requirements.txt
       ```
   - **Explanation**: These commands will install the specified packages and versions listed in the respective files, ensuring a consistent setup for all users.

---

Let me know if you have any questions! - Julian
