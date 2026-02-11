Setup
Everyone Should Complete These Steps First:
Step 1: Set Up Ubuntu VM Environment

Access your Azure Sandbox Ubuntu VM (from Lab 1/Lab 2)
Update system packages:

bash   sudo apt update
   sudo apt upgrade -y
Step 2: Install Required Software

Install Python and pip:

bash   sudo apt install python3 python3-pip -y
   python3 --version  # Verify installation

Install Visual Studio Code:

bash   sudo snap install code --classic

Install Docker:

bash   sudo apt install docker.io -y
   sudo systemctl start docker
   sudo systemctl enable docker
   sudo usermod -aG docker $USER
   # Log out and back in for group changes to take effect

Install Git:

bash   sudo apt install git -y
   git --version
Step 3: Download the Dataset

Go to Kaggle or your course resources
Download All_Diets.csv
Save it to your Ubuntu VM:

bash   mkdir ~/diet-project
   cd ~/diet-project
   # Upload the CSV file here (using scp, drag-and-drop, or wget)
Step 4: Set Up GitHub Repository (Person 3 leads, everyone collaborates)

Create a GitHub account if you don't have one
Person 3 creates the repository:

Go to github.com
Click "New Repository"
Name it: cloud-diet-analysis
Make it Public or Private
Initialize with README


Add team members as collaborators:

Settings → Collaborators → Add people


Everyone clones the repository:

bash   cd ~
   git clone https://github.com/YOUR_USERNAME/cloud-diet-analysis.git
   cd cloud-diet-analysis
   git config user.name "Your Name"
   git config user.email "your.email@example.com"