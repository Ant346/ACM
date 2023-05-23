**These assignments are using Rcognita package that was tested in Linux.**
**We strongly suggest you to use WSL to get it working under Windows.**

Here we provide a guide for proper installation of virtual environments in order to make your workflow robust and independent from Colab availability.

You can skip this part if you're already using some preferred virtual environment manager. Anyway, **USE SEPARATE ENVIRONMENTS FOR EVERY ASSIGNMENT** (and for every separate python project as well).

Skip Part 1 if **WSL 2** (two! this is important!) is already installed along with a Linux distribution.

-------------------------------------------------------------------------------------------------------------------

### Part 1. WSL

Here are the steps to install WSL 2 first. This is the Linux subsystem needed to run rcognita in Windows.

1.1. First, check the available Linux distributions to install:
```console
PS C:\> wsl --list --online
```
1.2. The output may be, say:
```console
	The following is a list of valid distributions that can be installed.
	Install using 'wsl --install -d <Distro>'.

	NAME                                   FRIENDLY NAME
	Ubuntu                                 Ubuntu
	Debian                                 Debian GNU/Linux
	kali-linux                             Kali Linux Rolling
	Ubuntu-18.04                           Ubuntu 18.04 LTS
	Ubuntu-20.04                           Ubuntu 20.04 LTS
	Ubuntu-22.04                           Ubuntu 22.04 LTS
	OracleLinux_8_5                        Oracle Linux 8.5
	OracleLinux_7_9                        Oracle Linux 7.9
	SUSE-Linux-Enterprise-Server-15-SP4    SUSE Linux Enterprise Server 15 SP4
	openSUSE-Leap-15.4                     openSUSE Leap 15.4
	openSUSE-Tumbleweed                    openSUSE Tumbleweed
```

1.3. Pick one, say, Ubuntu and install it:
```console
PS C:\>	wsl --install -d Ubuntu
```

Read more here: **https://ubuntu.com/tutorials/install-ubuntu-on-wsl2-on-windows-10#1-overview**

1.4. Run Linux terminal from WSL (Windows Run, type "WSL" or "Ubuntu"). Update and upgrade.

```console
foo@bar:~$ sudo apt update
foo@bar:~$ sudo apt upgrade
```	
1.5 (Optional) install z-shell.
```console
foo@bar:~$ sudo apt install zsh
```	
Read more here: **https://github.com/ohmyzsh/ohmyzsh/wiki/Installing-ZSH**

1.6 (Optional) install oh-my-zsh.
```console
foo@bar:~$ sudo apt install curl
foo@bar:~$ sudo apt install git
foo@bar:~$ sh -c "$(curl -fsSL -k https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```
Read more here: **https://ohmyz.sh/**

1.7 (Optional) Install pretty theme for oh-my-zsh.
```console
foo@bar:~$ git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
foo@bar:~$ nano ~/.zshrc
```	
And set the theme, write in `~/.zshrc`:

```console
foo@bar:~$ ZSH_THEME="powerlevel10k/powerlevel10k"
```	
Reload:
```console
foo@bar:~$ exec zsh
```	
Answer the questions in terminal as you desire.

Read more here: **https://github.com/romkatv/powerlevel10k#installation	**
	
-------------------------------------------------------------------------------------------------------------------

### Part 2. Python environment

2.1. Install dependencies.

```console
foo@bar:~$ sudo apt install build-essential libssl-dev zlib1g-dev \
foo@bar:~$ libbz2-dev libreadline-dev libsqlite3-dev curl \
foo@bar:~$ libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
```

2.2. Install pyenv. They "-k" option is to avoid issues with an antivirus.

```console
foo@bar:~$ curl -k https://pyenv.run | bash
```	
2.3. Sync pyenv with the terminal.

```console
foo@bar:~$ echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
foo@bar:~$ echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
foo@bar:~$ echo 'eval "$(pyenv init -)"' >> ~/.zshrc
foo@bar:~$ exec zsh
```	
Read more here: **https://github.com/pyenv/pyenv/wiki#suggested-build-environment**

2.4. Install Python 3.9.16 in which rcognita was tested.
```console
foo@bar:~$ pyenv install 3.9.16 
```	 
This may fail due to an antivirus. So, try this:
```console
foo@bar:~$ pyenv install -k 3.9.16
```
2.5. Check pyenv versions. Check that Python 3.9.16 is there.

```console
foo@bar:~$ pyenv versions	
```
-------------------------------------------------------------------------------------------------------------------

### Part 3. rcognita

3.1. Pick a folder where you want to clone the repo. You can do this in Explorer, say. Hint: pressing Right Click (or Shift + Right Click) should pop up a menu with an "Open Linux shell here" option. Choose it.

3.2. Clone the repo.

```console
foo@bar:~$ git clone https://gitflic.ru/project/aidynamicaction/rcognita.git
```
3.3. cd to `rcognita` directory

```console 
foo@bar:~$ cd rcognita
```

3.4. (Optional)

```console
foo@bar:~$ git checkout research-CALF
```

3.5. Create new virtual environment.

```console
foo@bar:~$ pyenv virtualenv 3.9.16 rcenv
```	
3.6. Set the default environment for the current folder.
```console
foo@bar:~$ pyenv local rcenv		
```
-------------------------------------------------------------------------------------------------------------------

### Part 4. IDE

It is better to use VScode, at least under WSL.

4.1. Run VScode via typing the following in WSL terminal:

```console
foo@bar:~$ code .
```
4.2. Go to terminal in the top menu and run one.

4.3. In the bottom subwindow (where the terminal is) press the arrow down symbol (drop-down menu) and choose Ubuntu(WSL).

4.4. Install plugins. On the top left menu, click the 4-blocks button. Type "python" in the search field. Choose "Python Extensions Pack". Click "install". Search and install "WSL". 

4.5. Restart VScode.

4.6. In the bottom menu, right corner, click on the Python version displayed and choose the rcenv environment from the pop-up list.

4.7. Install rcognita in editable mode. This is handy for development purposes when you don't need rcognita to be installed in the site-packages. Type, while in the cloned rcognita repo:

```console
foo@bar:~$ pip install -e .
```
4.8. Create a launch json file. On the top left menu, click the bug-and-arrow button. Then, "create a launch.json file". Choose "Python file"

4.9. Open the launch.json file, configure parameters as desired and press Ctrl+F5 (or just F5 to debug).

-------------------------------------------------------------------------------------------------------------------

### Part 5. Animation

When using WSL, an X server may be required.

4.1. Install Xming X server for Windows following, say, https://sourceforge.net/projects/xming/.

4.2. Type in the VScode terminal:

```console
foo@bar:~$ export DISPLAY=localhost:0.0
```
or set it up permanently in shell config:
```console
foo@bar:~$ nano ~/.zshrc
```	
Go all the way down and add a line:

```console
foo@bar:~$ export DISPLAY=localhost:0.0
```

4.3. Always make sure that Xming X server is running in Windows. This can be done via autostart.

4.4. To save animation in mp4 format, make sure ffmpeg is installed. If not, do this:

```console
foo@bar:~$ sudo apt install ffmpeg   
```	
-------------------------------------------------------------------------------------------------------------------

### Part 6. Viewing data

rcognita consists of the two general parts: `modules` and `playground`.
`playground` is where the run script, configurations and saved data are placed.
After a run, go to `multirun` folder.
The runs are organized in folders by date, controllers and systems.
Go to a desired folder and subfolder, then `0` (there may be more of these numbered subfolders if multiple threads were run).
Then, go to `gfx` to see the plots.
Animations are stored just in `0` folder.

Since rcognita also uses mlflow, you can just type in terminal (making sure you are in `playground` folder):

```console
foo@bar:~$ mlflow ui
```	
It will display a line with

```console
	Listening at: http://mlflow-server-url
```	

Press ctrl and left click on the URL displayed and see all the data in a nicely structured format.